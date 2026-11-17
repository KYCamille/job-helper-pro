---
name: reality-check
description: 面試後，依面試紀錄驗證先前的推敲、重新評分適配度與屎缺機率，分析隱藏優缺點、未來狀況、話語權與談薪策略，產出 reality/<slug>.html。當使用者說「面試完了」「幫我對照面試」「我該怎麼談薪水」「這個 offer 該不該接」時使用。
---

# reality-check：現實度匹配

對應 AGENTS.md 工作流程 ⑧，完整規則在 `rules/reality-check.md`。

## 步驟
1. 讀 `rules/reality-check.md`，以及同 slug 的 jobs、company、career、interview 頁與 `profile/vision.md`。
2. 確認面試紀錄存在（`raw/interviews/` 或真實的 `private/interviews/`），每點都有 IV 代碼；沒有代碼先幫使用者補上，並請使用者確認。
3. **驗證表**：把 company 頁的「待確認」、career 頁的 ❓、interview 頁的反問題全部列出，逐項判定 ✅／❌／➖ 並引用 IV 代碼。
4. **重新評分**：屎缺訊號表從頭重算（新證據可以加入或移除訊號），適配度、願景對齊、職涯成長性一起更新。
5. **隱藏優缺點**：只寫面試中才知道的事，各至少 3 點。
6. **未來狀況**：1 個月／3 個月／6 個月／1 年＋最壞情況。
7. **話語權**：5 因子各 1–5 分，算平均。
8. **談判**：底線 ≤ 目標 ≤ 開價（依 vision.md 與面試聽到的範圍），薪資以外的條件，至少 5 條技巧與話術。
9. 真實面試 → 輸出到 `private/reality/`；虛構範例 → `reality/`。
10. 執行 `python3 scripts/check.py`。

## 自我檢查
- [ ] 沒有引用紀錄裡不存在的 IV 代碼
- [ ] 沒有因為「氣氛好」就調降屎缺機率
- [ ] 話語權平均與各因子一致
- [ ] 開價有理由，不是單純喊高
