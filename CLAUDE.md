@AGENTS.md

# Claude Code 專屬補充

- 本專案的總則在上方引入的 AGENTS.md；做到工作流程 ③-A／③-B／③-C 時，再讀 `rules/` 底下對應的細則檔。
- 可用 Skills（位於 `.claude/skills/`）：
  - `analyze-job`：② 解析與評分 → `jobs/<slug>.html`
  - `diagnose-company`：③-A 公司診斷與屎缺判定 → `company/<slug>.html`（需要 WebSearch）
  - `career-fit`：③-B 職涯適配與願景問答 → `career/<slug>.html`
  - `interview-prep`：③-C 模擬面試與反問題 → `interview/<slug>.html`
  - `reality-check`：⑧ 面試後的現實度匹配、話語權與談薪策略 → `reality/<slug>.html`
  - `tailor-resume`：④ 客製化履歷 → `resumes/<slug>.html`
- ③-A 與 ③-B 互不依賴，可以用 subagent 平行執行；③-C 要等兩者完成。
- 完成標準一律以 `python3 scripts/check.py` 的輸出為準；不要只說「我檢查過了」。
- 工作流程 ⑥「審查」請用 subagent 或新對話執行，只給它事實來源（profile、raw）與產出頁，不要讓寫的人審自己的作品。
- 對真實公司做診斷時，輸出只放 `private/`，不要 commit。
- 未經使用者同意，不要 `git push`。
