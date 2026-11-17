# AGENTS.md — 求職小幫手 Pro（Job Helper Pro）員工手冊

> 給所有 AI Agent（Claude Code、Codex、Antigravity、OpenCode……）的專案規則。
> **每次開工前先完整讀完這份文件**，再動任何檔案。看不懂或規則沒寫到的情況，先問人，不要猜。

---

## 1. 專案目的

「求職小幫手 Pro」是一個部署在 GitHub Pages 的靜態網站，是「求職小幫手」的進階版。它用一套**固定的流程與格式**，從三個視角看同一則職缺：

| 視角 | 問的問題 | 頁面 | 細則 |
|---|---|---|---|
| 我 → 職缺 | 我符合嗎？履歷怎麼改？ | `jobs/`、`resumes/` | 本檔第 4–6 節 |
| 公司 → 職缺 | 公司為什麼現在開這個缺？這是不是屎缺？ | `company/` | `rules/company-diagnosis.md` |
| 職缺 → 我的未來 | 它會把我帶到哪裡？符合我的願景嗎？ | `career/` | `rules/career-fit.md` |
| 面試現場 | 會被問什麼？我該反問什麼？ | `interview/` | `rules/interview.md` |
| 面試之後 | 先前的推敲對不對？還有什麼隱藏的？我的話語權多大、怎麼談？ | `reality/` | `rules/reality-check.md` |

網站的每一頁都是這套流程的產物。這個專案的重點不是「做出一個網頁」，而是**讓任何 AI 拿到一則新職缺，就能照同一套規則，在幾分鐘內產出一組格式一致、經得起檢查的新頁面**。

**讀者**：求職者本人（決定要不要投、怎麼改履歷、怎麼談條件），以及協助求職的朋友或老師（快速看懂判斷依據）。

> **漸進式閱讀**：本檔是總則，每次都要讀。`rules/` 底下的細則**只在做到對應步驟時才讀**，避免一次塞入太多規則。

---

## 2. 資料夾結構（哪些可以動、哪些不能動）

```
job-helper-pro/
├── AGENTS.md              ← 本手冊：總則（修改需經使用者同意）
├── rules/                 ← 細則：做到該步驟時才讀
│   ├── company-diagnosis.md   公司與職缺診斷、屎缺判定
│   ├── career-fit.md          職涯適配與願景問答
│   ├── interview.md           模擬面試與反問題
│   └── reality-check.md       面試後的現實度匹配與談判
├── CLAUDE.md              ← Claude Code 入口，只放 @AGENTS.md 與 Claude 專屬補充
├── README.md              ← 給人看的專案簡介
├── index.html             ← 首頁：流程說明 + 所有職缺卡片清單
├── guide.html             ← 「如何新增內容」說明頁（AGENTS.md 的網頁版摘要）
├── assets/
│   ├── style.css          ← 全站唯一的樣式表（不要另外新增 CSS 檔）
│   ├── qa.js              ← 量性問卷
│   ├── qual.js            ← 質性互動訪談
│   └── reality.js         ← 面試紀錄上傳與比對（只在瀏覽器內讀取）
├── profile/
│   ├── profile.md         ← 求職者主履歷（唯一事實來源，AI 只能讀，不能改）
│   └── vision.md          ← 職涯願景與價值排序（使用者自己寫，AI 只能讀）
├── raw/
│   ├── jobs/<slug>.md     ← 職缺原文（使用者貼上的 JD，AI 只能讀，不能改）
│   ├── companies/<公司>.md ← 公司資料蒐集紀錄（新聞、官網、影音、評價，附來源代碼）
│   ├── qa/<slug>.md        ← 質性訪談紀錄（公開版只放虛構範例）
│   └── interviews/<slug>-r<n>.md ← 面試紀錄（公開版只放虛構範例）
├── jobs/<slug>.html       ← 職缺解析頁（AI 產出）
├── resumes/<slug>.html    ← 客製化履歷頁（AI 產出）
├── company/<slug>.html    ← 公司與職缺診斷頁（AI 產出）
├── career/<slug>.html     ← 職涯適配頁（AI 產出）
├── interview/<slug>.html  ← 面試攻略頁（AI 產出）
├── reality/<slug>.html    ← 現實度匹配頁（面試後才產出）
├── templates/             ← 五種頁面模板（新增頁面一律從這裡複製）
│   ├── job.html  resume.html  company.html  career.html  interview.html  reality.html
├── scripts/
│   └── check.py           ← 自動檢查腳本（完成標準的依據）
├── .claude/skills/        ← 可重複使用的標準作業流程（SKILL.md）
│   ├── analyze-job/  tailor-resume/
│   └── diagnose-company/  career-fit/  interview-prep/  reality-check/
└── private/               ← 真實個資放這裡；已在 .gitignore，永遠不會上傳
```

| 路徑 | AI 可以 | AI 不可以 |
|---|---|---|
| `profile/`、`raw/jobs/` | 讀取 | 修改、刪除（這是「事實來源」） |
| `raw/companies/` | 新增蒐集到的資料（必附來源） | 刪除或改寫既有紀錄 |
| `raw/qa/`、`raw/interviews/` | 讀取 | 修改（這是使用者的原話與現場紀錄） |
| `jobs/`、`resumes/`、`company/`、`career/`、`interview/`、`reality/` | 新增、修改 | 刪除既有頁面（除非使用者明確要求） |
| `index.html` | 在卡片清單新增／更新卡片 | 改動版面結構、刪掉別人的卡片 |
| `assets/style.css` | 新增元件樣式（附註解） | 修改既有色彩 token、刪除既有 class |
| `templates/`、`AGENTS.md`、`rules/`、`scripts/` | 提出修改建議 | 未經同意直接修改 |
| `private/` | 讀取（使用者要求時） | 把內容複製到任何會被上傳的檔案 |

---

## 3. 命名規則

- **slug 格式**：`YYYY-MM-公司英文代稱-職位英文代稱`，全小寫、只用 `a-z 0-9 -`。
  - 例：`2026-11-lumen-data-analyst`、`2026-11-qingsong-ai-product-specialist`
  - `YYYY-MM` 是**收到職缺的月份**，不是截止日。
- 同一個職缺的所有檔案**必須共用同一個 slug**：
  - `raw/jobs/<slug>.md` → `jobs/` → `resumes/` → `company/` → `career/` → `interview/` → `reality/`
- 面試紀錄：`raw/interviews/<slug>-r1.md`、`-r2.md`……（第幾輪）
- 公司資料檔用公司英文代稱：`raw/companies/lumen.md`（同一間公司的多個職缺共用）。
- 每個 `raw/jobs/<slug>.md` 開頭要有一行 `- 公司資料：raw/companies/<公司>.md`。
- 同公司同職位第二次出現時，在結尾加 `-v2`。
- 圖片（若有）放 `assets/img/<slug>-說明.png`，寬度不超過 1200px。

---

## 4. 頁面類型與必備區塊

所有頁面都從 `templates/` 複製，**不可刪除必備區塊**，也不可改 `id`。`scripts/check.py` 會逐一檢查這些 `id`。

| 頁面 | 必備區塊 id | 細則 |
|---|---|---|
| `jobs/` | 見 4.1 | 本檔 |
| `resumes/` | 見 4.2 | 本檔 |
| `company/` | `company-brief` `role` `dimensions` `trap` （`trap-type`） `sources` | `rules/company-diagnosis.md` |
| `career/` | `strengths-use` `impact` `direction` `limits` `alignment` `qa` `qual` `qual-analysis` `decision` | `rules/career-fit.md` |
| `interview/` | `questions` `reverse` `sources` | `rules/interview.md` |
| `reality/` | `record` `intake` `verify` `rescore` `hidden` `scenarios` `leverage` `negotiation` `sources` | `rules/reality-check.md` |

同一 slug 的頁面頂端都要有相同的分頁列 `<nav class="subnav">`（解析／履歷／公司診斷／職涯適配／面試攻略／現實度匹配），目前頁面加 `aria-current="page"`；還沒面試的職缺，「現實度匹配」用 `<span class="off">` 顯示為未開放。

### 4.1 職缺解析頁 `jobs/<slug>.html`

| 區塊 `id` | 標題 | 內容規則 |
|---|---|---|
| `summary` | 職缺摘要 | 公司、職稱、地點、工作型態、薪資（JD 沒寫就寫「未揭露」）、一句話說明這份工作在做什麼 |
| `requirements` | 條件拆解 | 分「必備」與「加分」兩欄，每條都要能在 JD 原文找到依據 |
| `keywords` | 關鍵字 | 5–12 個 ATS 關鍵字，使用 `<span class="tag">` |
| `match` | 適配度評分 | 依第 6 節評分表打分，表格呈現四個面向 + 總分 + 等級 |
| `gaps` | 落差與補強 | 每個落差給「短期可做的補強」（一週內可完成的具體行動） |
| `interview` | 面試準備 | 3–5 題可能被問的問題，每題附「回答方向」並對應主履歷中的一段經歷 |
| `sources` | 資料來源 | 連到 `raw/jobs/<slug>.md`，並註明解析日期 |

頁首必須有：麵包屑（首頁 › 職缺解析）、`<span class="badge badge-high|badge-mid|badge-low">`、以及「→ 看客製化履歷」按鈕連到對應的 `resumes/<slug>.html`。

### 4.2 客製化履歷頁 `resumes/<slug>.html`

| 區塊 `id` | 標題 | 內容規則 |
|---|---|---|
| `target` | 投遞目標 | 職稱 + 公司 + 連回 `jobs/<slug>.html` |
| `headline` | 個人摘要 | 2–3 句，第一句就要包含職缺最重要的 1–2 個關鍵字 |
| `skills` | 技能 | 依職缺相關度排序，最相關的放前面 |
| `experience` | 工作經歷 | 每條成果用「動詞 + 做了什麼 + 量化結果」格式 |
| `projects` | 專案 | 最多 3 個，只挑跟職缺相關的 |
| `education` | 學歷 | 照抄主履歷，不改寫 |
| `changes` | 改了什麼、為什麼 | 表格：原句（主履歷）／新句／理由（對應哪個 JD 關鍵字） |

---

## 5. 誠實原則（最重要，違反就是失敗）

1. **不得捏造**：客製化履歷的每一個事實（公司、職稱、年資、數字、技能、證照）都必須能在 `profile/profile.md` 找到。可以改寫措辭、調整順序、刪減，但**不能新增主履歷沒有的事實**。
2. **數字不灌水**：主履歷寫「提升 12%」，就不能寫成「提升 15%」或「大幅提升」以外的更強說法。
3. **不會的就說不會**：主履歷沒有的技能，只能出現在職缺頁的 `gaps` 區塊，不能出現在履歷的 `skills`。
4. **評分要有理由**：適配度每一個分數旁邊都要寫一句依據。
5. 遇到主履歷資訊不足、無法判斷的情況 → **停下來列出問題問使用者**，不要用常識補齊。

---

## 6. 適配度評分表（所有職缺用同一把尺）

| 面向 | 配分 | 怎麼給分 |
|---|---|---|
| 硬技能 | 40 | 必備硬技能符合比例 × 35（四捨五入）＋ 加分技能每項 +1～2，最多 +5 |
| 相關經驗 | 30 | 先看 JD 職責有幾項做過（比例 × 30），年資不足每差 1 年再扣 8 分（最低 0 分） |
| 產業／領域 | 15 | 同產業 15、相近產業 8–12、不同產業 0–7 |
| 軟實力與工作型態 | 15 | 溝通、跨部門、語言、遠端／出差等 JD 明列項目 |

| 總分 | 等級 | badge class |
|---|---|---|
| 80–100 | 高度適合，建議優先投遞 | `badge-high` |
| 60–79 | 可以嘗試，先做 `gaps` 的補強 | `badge-mid` |
| 0–59 | 需要補強，暫不建議投遞 | `badge-low` |

---

## 7. 網頁風格

- **調性**：專業、冷靜、像一份整理好的顧問報告；不要花俏動畫、不要 emoji 標題。
- **字體**：`Noto Sans TC`（Google Fonts），英文與數字同字體。
- **色彩**：只用 `assets/style.css` 裡 `:root` 定義的 token（`--bg`、`--surface`、`--text`、`--muted`、`--accent`、`--good`、`--warn`、`--bad`、`--line`）。**不可在 HTML 裡寫死色碼或 inline style**。支援深色模式（已在 CSS 處理）。
- **元件**：只用 CSS 已定義的 class：`.card`、`.badge`、`.tag`、`.btn`、`.score-table`、`.two-col`、`.callout`、`.breadcrumb`、`.flow`、`.subnav`、`.meter`、`.qa-card`、`.qa-form`、`.matrix`、`.qual`、`.intake`、`.delta`。需要新元件時，先在 `style.css` 末端新增並加註解。
- **版面**：內容最寬 880px；手機寬度（375px）不能出現水平捲動。
- **語言**：繁體中文、台灣用語；技術名詞保留英文（SQL、Python、ATS）。全形標點。

---

## 8. 工作流程（Graph）

新增一則職缺時，依序走完下列節點。**哪一關沒過，就退回最近的那一關修，不要整份重來。**

```
                          ┌→ ③-A 公司診斷 ─┐
① 收件 → ② 解析與評分 ──┼→ ③-B 職涯適配 ─┼→ ③-C 面試攻略 → ④ 客製化履歷 → ⑤ 自動檢查 → ⑥ 審查 → ⑦ 上架
                          └────────────────┘         ↑_____________________________|        ↑______|
```

- ③-A 與 ③-B 互不依賴，可以平行做；③-C 必須等 ③-A、③-B 完成（反問題來自它們的「待確認」）。
- **⑧ 現實度匹配**：面試後才觸發。使用者把面試紀錄放進 `raw/interviews/`（真實紀錄放 `private/interviews/`）並說「面試完了，幫我做現實度匹配 <slug>」→ 讀 `rules/reality-check.md` → 產出 `reality/<slug>.html` → 回到 ⑤ 檢查 → ⑦ 上架。每多一輪面試就更新一次。
- **總分 < 60** 的職缺：只做 ① ② ⑤ ⑦，不做 ③ ④（不值得花時間深挖）。使用者明確要求時例外。

| 節點 | 做什麼 | 產出 | 使用的 Skill |
|---|---|---|---|
| ① 收件 | 把 JD 原文存成 `raw/jobs/<slug>.md`（使用者提供，含來源網址與收件日期） | raw 檔 | — |
| ② 解析與評分 | 從模板建立職缺頁，依第 6 節打分，填全部區塊 | `jobs/<slug>.html` | `analyze-job` |
| ③-A 公司診斷 | 讀 `rules/company-diagnosis.md`，先蒐集資料到 `raw/companies/`，再分析角色、五維度、屎缺機率 | `company/<slug>.html` | `diagnose-company` |
| ③-B 職涯適配 | 讀 `rules/career-fit.md`，對照 `vision.md` 分析；需要時先做願景問答 | `career/<slug>.html` | `career-fit` |
| ③-C 面試攻略 | 讀 `rules/interview.md`，出 10 題模擬題＋至少 5 題反問 | `interview/<slug>.html` | `interview-prep` |
| ⑧ 現實度匹配 | 面試後。讀 `rules/reality-check.md`，驗證推敲、重新評分、隱藏優缺點、話語權與談判策略 | `reality/<slug>.html` | `reality-check` |
| ④ 客製化 | 從模板建立履歷頁，遵守第 5 節誠實原則。**總分 < 60 時跳過此步**，職缺頁按鈕改為「未產出履歷」 | `resumes/<slug>.html` | `tailor-resume` |
| ⑤ 自動檢查 | 執行 `python3 scripts/check.py`，必須 0 錯誤 | 檢查報告 | — |
| ⑥ 審查 | **開新的對話**，只給 `profile.md`、raw JD、產出頁，請它逐條找捏造或誇大 | 審查意見 | — |
| ⑦ 上架 | 在 `index.html` 卡片清單**最上方**新增卡片、git commit、push | 網站更新 | — |

---

## 9. 每次交辦的五件事（Loop 規格）

| | 內容 |
|---|---|
| 🎯 目標 | 一則新職缺 → 五個頁面（總分 < 60 則只有 `jobs/`）+ 首頁卡片 |
| 🚧 限制 | 不改 `profile/`、`raw/jobs/`、`templates/`、`rules/`；不捏造；公司資料必附來源；不在 HTML 寫 inline style |
| ✅ 完成標準 | `python3 scripts/check.py` 顯示 `ALL CHECKS PASSED`，且第 ⑥ 步審查沒有「捏造」或「無來源推論」類問題 |
| 🛑 停止條件 | 同一個檢查錯誤修 **3 輪**仍沒過就停下回報；JD、主履歷或公司資料不足就停下提問；**沒有上網工具時不可自行編寫公司近況** |
| ⏰ 觸發 | 使用者在 `raw/jobs/` 新增檔案並說「解析新職缺 <slug>」 |

---

## 10. Git 規則

- 每完成一則職缺 = 一個 commit，訊息格式：`add: <slug> 職缺分析五件組`
- 修改既有頁面：`fix: <slug> <改了什麼>`；改樣式或規則：`style:`、`docs:`
- commit 前一定要先跑 `python3 scripts/check.py`。
- 不要 commit `private/`、`.DS_Store`、任何含真實電話／Email／身分證字號的檔案。

---

## 11. 隱私規則

- 網站是**公開**的。公開版本只能放**範例求職者**或已去識別化的資料。
- 真實履歷放 `private/profile.md`；要用真實資料產出時，結果也只存在 `private/`，不放進 `jobs/`、`resumes/`。
- `scripts/check.py` 會掃描電話號碼、Email、身分證字號格式，發現就報錯。
- **對真實公司的「屎缺」判斷一律不公開**：只存 `private/`。判斷可能有誤，公開可能造成名譽爭議。公開網站只放虛構公司範例。
- 願景問答與質性訪談的紀錄（`private/qa/`）屬於個人隱私，不 commit。
- **真實面試紀錄（`private/interviews/`）一律不公開**：裡面有面試官與公司內部資訊。
- 網頁上的互動工具（問卷、訪談、上傳紀錄）只在使用者的瀏覽器內運作，不會把資料送到任何伺服器；新增任何 JS 時都必須維持這個原則。

---

## 12. 交辦範例（可以直接複製使用）

**新增職缺**
> 請先讀 AGENTS.md。我在 `raw/jobs/2026-12-xxx-marketing-analyst.md` 放了新職缺，
> 請依第 8 節流程完成 ②–⑤，跑完 check.py 把結果貼給我，先不要 commit。

**只做公司診斷（真實公司，不公開）**
> 請先讀 AGENTS.md 與 rules/company-diagnosis.md。幫我上網蒐集「＿＿公司」近 18 個月的新聞、官網、影音與員工評價，
> 存到 private/companies/，再對我貼的這份 JD 做屎缺判定，結果存在 private/company/，不要 commit。

**願景問答**
> 請先讀 rules/career-fit.md 第 5 節。一次問我一題，幫我釐清職涯願景，問完整理成 vision.md 草稿給我確認。

**面試後的現實度匹配（真實面試，不公開）**
> 請先讀 AGENTS.md 與 rules/reality-check.md。我把第一輪面試紀錄放在 private/interviews/<slug>-r1.md，
> 幫我驗證先前的推敲、重新評分、分析隱藏優缺點與我的話語權，並擬好談薪策略，結果存在 private/reality/，不要 commit。

**質性訪談深度分析**
> 請依 rules/career-fit.md §5.3 分析 private/qa/<slug>.md。有矛盾或模糊的地方先問我，不要自己補答案。

**修改既有履歷**
> 請先讀 AGENTS.md。`resumes/2026-11-lumen-data-analyst.html` 的個人摘要太長，
> 縮到 2 句，`changes` 表格要同步更新，改完跑 check.py。

**擴充新頁面類型（例如「求職信」）**
> 請先讀 AGENTS.md。我想新增「求職信」頁面類型。先不要建檔，
> 請提出：模板區塊與 id、命名規則、check.py 要加的檢查、AGENTS.md 要改的段落，給我確認後再動手。

---

## 13. 擴充方式

要新增一種頁面類型（求職信、面試紀錄、公司研究……）時，**四個地方要一起改**，缺一不可：

1. `templates/<type>.html` — 新模板，定義必備區塊 `id`
2. `AGENTS.md` 第 4 節的頁面總表 ＋ `rules/<type>.md` 細則
3. `scripts/check.py` 的 `PAGE_RULES` — 加上新類型的必備 `id`
4. `guide.html` — 更新給人看的說明

---

*最後更新：2026-11-17　維護者：專案擁有者（修改本手冊前請先和擁有者討論）*
