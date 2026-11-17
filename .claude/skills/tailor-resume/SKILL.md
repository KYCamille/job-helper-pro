---
name: tailor-resume
description: 依據已完成的職缺解析頁，把主履歷客製化成針對該職缺的版本，產出 resumes/<slug>.html。當使用者說「幫我改履歷」「客製化履歷」「針對這個職缺調整履歷」時使用。
---

# tailor-resume：履歷客製化標準作業流程

對應 AGENTS.md 第 8 節工作流程的 ④ 客製化。

## 輸入
- `jobs/<slug>.html`：已完成的職缺解析頁（沒有就先跑 `analyze-job`）
- `profile/profile.md`：主履歷，**唯一的事實來源**

## 步驟
1. **讀規則**：重讀 AGENTS.md 第 4.2、5 節（誠實原則）。
2. **複製模板**：`templates/resume.html` → `resumes/<slug>.html`。
3. **挑素材**：從職缺頁的 `keywords` 與 `requirements` 出發，在 profile.md 中找出每個關鍵字對應的經歷句子。找不到的關鍵字**不放進履歷**。
4. **改寫**：
   - 個人摘要第一句要放入最重要的 1–2 個關鍵字。
   - 經歷條目改成「動詞 + 做了什麼 + 量化結果」；數字照抄 profile.md，不可改動。
   - 用 JD 的用語替換同義詞（例：profile 寫「做報表」，JD 寫「建立 Dashboard」→ 可改成「建立 Dashboard」，因為事實相同）。
5. **排序**：技能與經歷條目依職缺相關度排序。
6. **刪減**：與職缺無關的專案刪掉，專案最多 3 個。
7. **記錄改動**：每一處改寫都要在 `changes` 表格留下「原句／新句／理由」，理由要指出對應的 JD 關鍵字。

## 誠實自查（每一條都要能回答「是」）
- [ ] 每個數字都能在 profile.md 找到一模一樣的值
- [ ] 每個技能都出現在 profile.md
- [ ] 沒有新增公司、職稱、證照、年資
- [ ] 職缺要求但我沒有的技能，只出現在職缺頁 `gaps`，沒出現在履歷

## 完成前
- 執行 `python3 scripts/check.py`
- 建議使用者開新對話做第 ⑥ 步審查（只給 profile.md、raw JD、這兩個產出頁）
