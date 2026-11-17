---
name: analyze-job
description: 解析一則職缺描述（JD），依 AGENTS.md 的評分表與模板產出 jobs/<slug>.html。當使用者說「解析新職缺」「分析這個職缺」「這份工作適不適合我」時使用。
---

# analyze-job：職缺解析標準作業流程

對應 AGENTS.md 第 8 節工作流程的 ② 解析、③ 評分。

## 輸入
- `raw/jobs/<slug>.md`：職缺原文（必須已存在，沒有就停下請使用者提供）
- `profile/profile.md`：求職者主履歷

## 步驟
1. **讀規則**：重讀 AGENTS.md 第 4.1、5、6、7 節。
2. **複製模板**：`templates/job.html` → `jobs/<slug>.html`，把所有 `{{...}}` 佔位符換掉。
3. **拆條件**：逐句讀 JD，把每個要求歸到「必備」或「加分」。
   - JD 用「必須／需具備／至少」→ 必備；「尤佳／加分／熟悉者優先」→ 加分。
   - 每一條後面用 `<small>` 標出 JD 原文關鍵片段，方便審查對照。
4. **抽關鍵字**：5–12 個，優先挑 JD 重複出現、或寫在職稱裡的詞。
5. **評分**：依 AGENTS.md 第 6 節四個面向打分，每個分數都寫一句依據（引用 profile.md 的具體段落）。
   - 計算總分 → 決定等級與 badge class（`badge-high` / `badge-mid` / `badge-low`）。
6. **落差與補強**：每個「必備但主履歷沒有」的項目都要列出，給一週內可完成的具體行動（例：「完成 Google 的 GA4 免費課程並取得證書」，不要寫「加強 GA4」）。
7. **面試準備**：3–5 題，每題的「回答方向」要指向 profile.md 裡的某段經歷或專案。
8. **資料來源**：連結 `../raw/jobs/<slug>.md`，寫上解析日期。

## 完成前自我檢查
- [ ] 7 個區塊 id 都在：`summary` `requirements` `keywords` `match` `gaps` `interview` `sources`
- [ ] 四個面向分數加總 = 總分，等級與 badge 一致
- [ ] 沒有任何 inline style、寫死的色碼
- [ ] 執行 `python3 scripts/check.py`

## 停止條件
- JD 缺少職稱或職責描述 → 停下回報。
- profile.md 無法判斷某項能力（例：沒寫英文程度，但 JD 要求多益 750）→ 在 `gaps` 標示「待確認」，並在回覆中問使用者，不要自行假設。
