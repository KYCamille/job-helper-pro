---
name: interview-prep
description: 依職缺、公司診斷與職涯分析，產出 10 題模擬面試題（考評核心、建議回答、掌握關鍵）與至少 5 題反問，存成 interview/<slug>.html。當使用者說「準備面試」「模擬面試」「我該問面試官什麼」時使用。
---

# interview-prep：面試攻略

對應 AGENTS.md 工作流程 ③-C，完整規則在 `rules/interview.md`。必須在 company 與 career 頁完成後才做。

## 步驟
1. 讀 `rules/interview.md`，以及同 slug 的 jobs、company、career 頁。
2. 依類別配比出 **剛好 10 題**：動機 1–2、專業 3–4、情境 2、落差 1–2、抗壓合作 1。
3. 每題寫 `.assess`（考評核心）、`.answer`（STAR，只用 profile.md 事實）、`.keys`（2–3 個重點／地雷）。
4. 反問題 **≥ 5 題**，涵蓋：職缺真實狀況、成功標準、資源與授權、成長路徑、自己的立基點。
5. company 頁的「待確認」訊號、career 頁的 ❓ 項目，每一個都要對應到一題反問（在 `.red` 寫出對應代號）。
6. 執行 `python3 scripts/check.py`。
