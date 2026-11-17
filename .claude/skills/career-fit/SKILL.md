---
name: career-fit
description: 分析職缺對求職者長期職涯的正面發揮、影響、方向與侷限，並以問答協助釐清願景，產出 career/<slug>.html。當使用者說「這份工作適合我的未來嗎」「幫我想職涯」「問我問題幫我釐清」時使用。
---

# career-fit：職涯適配分析

對應 AGENTS.md 工作流程 ③-B，完整規則在 `rules/career-fit.md`。

## 步驟
1. 讀 `rules/career-fit.md`、`profile/profile.md`、`profile/vision.md`。
2. `vision.md` 不足 → 先做願景問答：**一次一題**、8–10 題、不誘導，問完寫草稿給使用者確認。紀錄存 `private/qa/<slug>.md`。
3. 依序寫 `strengths-use`、`impact`、`direction`、`limits`，每點引用 profile 編號或 company 頁代碼。
4. `alignment` 表：vision.md 每個項目逐一比對，只能用 ✅ ⚠️ ❌ ❓。
5. `qa` 區塊：為**這個職缺**量身設計 8 題單選題（選項帶 data-weight），使用 `assets/qa.js`。
6. `decision`：建議＋關鍵理由＋進場前必確認的一件事。
7. 把所有 ❓ 交給 interview-prep 轉成反問題。
8. 執行 `python3 scripts/check.py`。
