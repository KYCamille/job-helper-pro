#!/usr/bin/env python3
"""求職小幫手 Pro — 自動檢查腳本（AGENTS.md 第 9 節「完成標準」）

用法：在專案根目錄執行  python3 scripts/check.py
全部通過會印出 ALL CHECKS PASSED，否則列出每個錯誤並以 exit code 1 結束。
只使用 Python 標準函式庫，不需要安裝任何套件。
"""
from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 每種頁面必備的 section id（AGENTS.md 第 4 節、rules/*.md）。新增頁面類型時在這裡加一行。
PAGE_RULES = {
    "job": ["summary", "requirements", "keywords", "match", "gaps", "interview", "sources"],
    "resume": ["target", "headline", "skills", "experience", "projects", "education", "changes"],
    "company": ["company-brief", "role", "dimensions", "trap", "sources"],
    "career": ["strengths-use", "impact", "direction", "limits", "alignment", "qa", "decision"],
    "interview": ["questions", "reverse", "sources"],
}
FOLDERS = {"job": "jobs", "resume": "resumes", "company": "company", "career": "career", "interview": "interview"}
DEEP_KINDS = ("company", "career", "interview")  # 適配度 ≥ 60 才產出
SLUG_RE = re.compile(r"^\d{4}-\d{2}-[a-z0-9]+(?:-[a-z0-9]+)+$")
FIT_LEVELS = [(80, "badge-high"), (60, "badge-mid"), (0, "badge-low")]
SOURCE_CODE_RE = re.compile(r"\b(OFF|NEWS|AV|REV|JD)-\d+\b")
ALIGN_MARKS = ("✅ 一致", "⚠️ 部分", "❌ 衝突", "❓ 待確認")

PII_PATTERNS = {
    "Email": re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
    "手機號碼": re.compile(r"09\d{2}[-\s]?\d{3}[-\s]?\d{3}"),
    "身分證字號": re.compile(r"\b[A-Z][12]\d{8}\b"),
}

errors: list[str] = []


def err(path: Path, msg: str) -> None:
    errors.append(f"[{path.relative_to(ROOT)}] {msg}")


class Page(HTMLParser):
    """收集 meta、id、連結、class、section 文字、data-* 數值與 qa-card 結構。"""

    CAPTURE = ("data-total", "data-trap-total", "data-signal", "data-dim")

    def __init__(self) -> None:
        super().__init__()
        self.meta: dict[str, str] = {}
        self.ids: list[str] = []
        self.links: list[str] = []
        self.scripts: list[str] = []
        self.classes: list[str] = []
        self.inline_styles = 0
        self.section_text: dict[str, list[str]] = {}
        self._sections: list[str | None] = []
        self.captured: dict[str, list[str]] = {k: [] for k in self.CAPTURE}
        self.dim_meters: list[str] = []
        self._capture: tuple[str, int] | None = None
        self._depth = 0
        self.card_slugs: list[str] = []
        self.qa_cards: dict[str, list[set[str]]] = {}
        self.fieldsets = 0
        self.radio_without_weight = 0
        self.has_subnav = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self._depth += 1
        cls = (a.get("class") or "").split()
        if tag == "meta" and "name" in a:
            self.meta[a["name"]] = a.get("content", "")
        if "id" in a:
            self.ids.append(a["id"])
        if "style" in a:
            self.inline_styles += 1
        self.classes.extend(cls)
        if "data-slug" in a:
            self.card_slugs.append(a["data-slug"])
        if tag in ("a", "link") and a.get("href"):
            self.links.append(a["href"])
        if tag == "script" and a.get("src"):
            self.scripts.append(a["src"])
        if tag == "nav" and "subnav" in cls:
            self.has_subnav = True
        if tag == "section":
            self._sections.append(a.get("id"))
        sec = self._sections[-1] if self._sections else None
        if tag == "article" and "qa-card" in cls and sec:
            self.qa_cards.setdefault(sec, []).append(set())
        elif sec in self.qa_cards and self.qa_cards[sec]:
            self.qa_cards[sec][-1].update(cls)
        if tag == "fieldset":
            self.fieldsets += 1
        if tag == "input" and a.get("type") == "radio" and "data-weight" not in a:
            self.radio_without_weight += 1
        if tag == "span" and "meter" in cls and self._capture and self._capture[0] == "data-dim":
            self.dim_meters.append(a.get("data-score", ""))
        for key in self.CAPTURE:
            if key in a:
                self._capture = (key, self._depth)
                self.captured[key].append("")

    def handle_endtag(self, tag):
        if self._capture and self._depth == self._capture[1]:
            self._capture = None
        self._depth -= 1
        if tag == "section" and self._sections:
            self._sections.pop()

    def handle_data(self, data):
        if self._sections and self._sections[-1]:
            self.section_text.setdefault(self._sections[-1], []).append(data)
        if self._capture:
            self.captured[self._capture[0]][-1] += data


def parse(path: Path) -> Page:
    p = Page()
    p.feed(path.read_text(encoding="utf-8"))
    return p


def text_of(page: Page, sid: str) -> str:
    return "".join(page.section_text.get(sid, []))


def numbers_in(s: str) -> set[str]:
    """取出「數字＋單位」，例如 12%、1.5小時、300萬，避免 15% 因為別處有 15 而漏抓。"""
    s = re.sub(r"[ \t]+", "", s.replace(",", ""))
    return set(re.findall(r"\d+(?:\.\d+)?(?:%|小時|萬|間|週|位|個|筆|人|年|倍|元|份|篇)?", s))


# ---------------------------------------------------------------- 共通檢查
def check_common(path: Path, page: Page, text: str) -> None:
    if "{{" in text:
        err(path, "還有沒替換的 {{佔位符}}")
    if page.inline_styles:
        err(path, f"有 {page.inline_styles} 個 inline style（AGENTS.md 第 7 節禁止）")
    if "<style" in text:
        err(path, "HTML 內不可有 <style>，樣式請寫在 assets/style.css")
    if not any(h.endswith("assets/style.css") for h in page.links):
        err(path, "沒有引用 assets/style.css")
    for src in page.scripts:
        if not src.endswith("assets/qa.js"):
            err(path, f"只允許引用 assets/qa.js，發現 {src}")
    for href in page.links + page.scripts:
        if href.startswith(("http://", "https://", "mailto:", "#")):
            continue
        if not (path.parent / href.split("#")[0]).resolve().exists():
            err(path, f"連結失效：{href}")


# ---------------------------------------------------------------- 各頁面類型
def check_job(path: Path, page: Page, slug: str) -> int | None:
    if not (ROOT / "raw" / "jobs" / f"{slug}.md").exists():
        err(path, f"找不到職缺原文 raw/jobs/{slug}.md")
    scores = [int(x) for x in re.findall(r"(\d+)\s*/\s*(?:40|30|15)(?!\d)", text_of(page, "match"))]
    total_m = re.search(r"(\d+)\s*/\s*100", "".join(page.captured["data-total"]))
    if len(scores) != 4 or not total_m:
        err(path, f"適配度應有 4 個面向分數與總分，找到 {len(scores)} 個分數")
        return None
    total = int(total_m.group(1))
    if sum(scores) != total:
        err(path, f"分數加總 {sum(scores)} ≠ 總分 {total}")
    for limit, s in zip((40, 30, 15, 15), scores):
        if not 0 <= s <= limit:
            err(path, f"分數 {s} 超出配分範圍 0–{limit}")
    expected = next(c for floor, c in FIT_LEVELS if total >= floor)
    if expected not in page.classes:
        err(path, f"總分 {total} 應使用 {expected}")

    for kind in ("resume",) + DEEP_KINDS:
        exists = (ROOT / FOLDERS[kind] / f"{slug}.html").exists()
        if total >= 60 and not exists:
            err(path, f"總分 ≥ 60 必須產出 {FOLDERS[kind]}/{slug}.html")
        if total < 60 and exists:
            err(path, f"總分 < 60 不應產出 {FOLDERS[kind]}/{slug}.html（AGENTS.md 第 8 節）")
    if total >= 60:
        raw = (ROOT / "raw" / "jobs" / f"{slug}.md").read_text(encoding="utf-8")
        m = re.search(r"公司資料：(raw/companies/[a-z0-9-]+\.md)", raw)
        if not m or not (ROOT / m.group(1)).exists():
            err(path, "raw/jobs 檔案缺少有效的「公司資料：raw/companies/<公司>.md」")
    return total


def check_resume(path: Path, page: Page, profile_numbers: set[str]) -> None:
    for sid in ("headline", "skills", "experience", "projects", "education"):
        for n in sorted(numbers_in(text_of(page, sid)) - profile_numbers):
            err(path, f"區塊 {sid} 出現 profile.md 沒有的數字「{n}」（可能是捏造或灌水）")


def company_file_for(page: Page) -> Path | None:
    for href in page.links:
        if "raw/companies/" in href:
            return (ROOT / "raw" / "companies" / Path(href).name)
    return None


def check_company(path: Path, page: Page) -> None:
    cf = company_file_for(page)
    if not cf or not cf.exists():
        err(path, "sources 區塊必須連到 raw/companies/<公司>.md")
        return
    raw = cf.read_text(encoding="utf-8")
    records = re.findall(r"^- \[((OFF|NEWS|AV|REV|JD)-\d+)\]", raw, flags=re.M)
    if len(records) < 6:
        err(cf, f"公司資料至少 6 筆，目前 {len(records)} 筆（rules/company-diagnosis.md §2.2）")
    if len({t for _, t in records}) < 3:
        err(cf, "公司資料至少要涵蓋 3 種來源類型")
    known = {c for c, _ in records}
    body = "".join(t for sid, ts in page.section_text.items() if sid != "sources" for t in ts)
    for code in sorted({m.group(0) for m in SOURCE_CODE_RE.finditer(body)} - known):
        err(path, f"引用了公司資料中不存在的來源代碼 {code}（可能是捏造）")

    # 五大維度：5 個、1–5 分、量表與文字一致
    dims = page.captured["data-dim"]
    if len(dims) != 5:
        err(path, f"五大維度應有 5 項，找到 {len(dims)} 項")
    for txt, meter in zip(dims, page.dim_meters):
        m = re.search(r"(\d)\s*/\s*5", txt)
        if not m or not 1 <= int(m.group(1)) <= 5 or meter != m.group(1):
            err(path, f"維度分數需為 1–5 且量表 data-score 一致（文字「{txt.strip()}」、量表 {meter}）")

    # 屎缺機率：基準 + 訊號加總 = 總機率，限制 5–95
    signals = [int(s.replace("−", "-").replace("+", "").strip()) for s in page.captured["data-signal"]]
    tot = re.search(r"(\d+)\s*%", "".join(page.captured["data-trap-total"]))
    if not signals or signals[0] != 20:
        err(path, "屎缺訊號表第一列必須是基準 +20")
    if not tot:
        err(path, "找不到屎缺機率總計（data-trap-total）")
        return
    prob = int(tot.group(1))
    expected = max(5, min(95, sum(signals)))
    if prob != expected:
        err(path, f"屎缺機率 {prob}% ≠ 訊號加總 {expected}%")
    level = "prob-low" if prob < 40 else "prob-mid" if prob <= 60 else "prob-high"
    badge = "badge-high" if prob < 40 else "badge-mid" if prob <= 60 else "badge-low"
    if level not in page.classes or badge not in page.classes:
        err(path, f"機率 {prob}% 應使用 {level} 與 {badge}")
    has_type = "trap-type" in page.ids
    if prob > 60 and not has_type:
        err(path, "屎缺機率 > 60% 必須有 trap-type 區塊")
    if prob <= 60 and has_type:
        err(path, "屎缺機率 ≤ 60% 不可有 trap-type 區塊")
    if has_type and "hit" not in page.classes:
        err(path, "trap-type 矩陣必須用 .hit 標出判定的類型")


def check_career(path: Path, page: Page) -> None:
    align = text_of(page, "alignment")
    rows = align.count("✅") + align.count("⚠️") + align.count("❌") + align.count("❓")
    if rows < 5:
        err(path, f"願景對齊表至少要比對 5 項，目前 {rows} 項")
    if page.fieldsets < 8:
        err(path, f"釐清問答至少 8 題，目前 {page.fieldsets} 題")
    if page.radio_without_weight:
        err(path, f"有 {page.radio_without_weight} 個選項缺少 data-weight")
    if not any(s.endswith("assets/qa.js") for s in page.scripts):
        err(path, "職涯頁必須引用 assets/qa.js")


def check_interview(path: Path, page: Page) -> None:
    qs = page.qa_cards.get("questions", [])
    if len(qs) != 10:
        err(path, f"模擬面試題必須剛好 10 題，目前 {len(qs)} 題")
    for i, c in enumerate(qs, 1):
        missing = {"assess", "answer", "keys"} - c
        if missing:
            err(path, f"Q{i} 缺少 {', '.join(sorted(missing))}")
    rs = page.qa_cards.get("reverse", [])
    if len(rs) < 5:
        err(path, f"反問題至少 5 題，目前 {len(rs)} 題")
    for i, c in enumerate(rs, 1):
        missing = {"purpose", "good", "red"} - c
        if missing:
            err(path, f"R{i} 缺少 {', '.join(sorted(missing))}")
    html = path.read_text(encoding="utf-8")
    rev_html = html[html.find('id="reverse"'):html.find('id="sources"')]
    tags = set(re.findall(r'<span class="tag">([^<]+)</span>', rev_html))
    for facet in ("職缺真實狀況", "成功標準", "資源與授權", "成長路徑", "自己的立基點"):
        if facet not in tags:
            err(path, f"反問題缺少「{facet}」面向")


def check_index(job_scores: dict[str, int | None]) -> None:
    path = ROOT / "index.html"
    page = parse(path)
    check_common(path, page, path.read_text(encoding="utf-8"))
    for slug in job_scores:
        if slug not in page.card_slugs:
            err(path, f"首頁缺少職缺卡片 data-slug=\"{slug}\"")
    for slug in page.card_slugs:
        if slug not in job_scores:
            err(path, f"首頁卡片 {slug} 沒有對應的 jobs/{slug}.html")


def check_pii() -> None:
    for p in ROOT.rglob("*"):
        if not p.is_file() or p.suffix not in {".html", ".md", ".css", ".js", ".json"}:
            continue
        if {"private", ".git"} & set(p.relative_to(ROOT).parts):
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        for label, rx in PII_PATTERNS.items():
            for m in rx.findall(text):
                if label == "Email" and m.endswith(("@anthropic.com", "@example.com")):
                    continue
                err(p, f"疑似{label}：{m}（公開檔案不可放個資）")


def main() -> int:
    profile_numbers = numbers_in((ROOT / "profile" / "profile.md").read_text(encoding="utf-8"))
    if not (ROOT / "profile" / "vision.md").exists():
        err(ROOT / "profile", "缺少 profile/vision.md（rules/career-fit.md §2）")
    job_scores: dict[str, int | None] = {}
    counts: dict[str, int] = {}

    for kind, folder in FOLDERS.items():
        pages = sorted((ROOT / folder).glob("*.html"))
        counts[kind] = len(pages)
        for path in pages:
            slug = path.stem
            text = path.read_text(encoding="utf-8")
            page = parse(path)
            if not SLUG_RE.match(slug):
                err(path, "檔名不符合 YYYY-MM-company-role 格式")
            if page.meta.get("page-type") != kind:
                err(path, f"meta page-type 應為 {kind}")
            if page.meta.get("slug") != slug:
                err(path, f"meta slug「{page.meta.get('slug')}」與檔名不一致")
            if not page.has_subnav:
                err(path, "缺少分頁列 <nav class=\"subnav\">")
            for sid in PAGE_RULES[kind]:
                if sid not in page.ids:
                    err(path, f"缺少必備區塊 id=\"{sid}\"")
            if kind != "job" and not (ROOT / "jobs" / f"{slug}.html").exists():
                err(path, f"找不到對應的職缺頁 jobs/{slug}.html")
            check_common(path, page, text)
            if kind == "job":
                job_scores[slug] = check_job(path, page, slug)
            elif kind == "resume":
                check_resume(path, page, profile_numbers)
            elif kind == "company":
                check_company(path, page)
            elif kind == "career":
                check_career(path, page)
            elif kind == "interview":
                check_interview(path, page)

    for raw in sorted((ROOT / "raw" / "jobs").glob("*.md")):
        if not (ROOT / "jobs" / f"{raw.stem}.html").exists():
            err(raw, "有職缺原文但還沒有解析頁（流程停在 ① 收件）")

    guide = ROOT / "guide.html"
    check_common(guide, parse(guide), guide.read_text(encoding="utf-8"))
    check_index(job_scores)
    check_pii()

    print("檢查範圍：" + "、".join(f"{FOLDERS[k]} {v} 頁" for k, v in counts.items()) + "、首頁、說明頁")
    if errors:
        print(f"\n❌ 發現 {len(errors)} 個問題：")
        for e in errors:
            print("  -", e)
        return 1
    print("✅ ALL CHECKS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
