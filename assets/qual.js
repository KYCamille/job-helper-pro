/* 求職小幫手 Pro — 質性互動訪談（rules/career-fit.md §5.3）
   一次一題、依回答內容選擇追問、最後歸納主題並匯出 Markdown。
   所有資料只存在使用者自己的瀏覽器（localStorage），不會送到任何伺服器。 */
(function () {
  var DEFAULT_THEMES = {
    '成長': '成長|學|進步|能力|經驗|挑戰',
    '穩定': '穩定|裁員|縮編|倒閉|安全感|長久|保障|資金|房貸',
    '薪資': '薪|錢|待遇|收入|加薪|月薪|房貸|持平',
    '主管與團隊': '主管|帶人|指導|討論|同事|團隊|沒人|一個人',
    '工時與生活': '加班|工時|下班|累|休息|生活|家人|假日',
    'AI 與技術': 'AI|生成式|Prompt|模型|自動化|工具',
    '影響力': '影響|被採用|決策|成果|價值|意義',
    '職涯方向': '未來|三年|五年|轉職|方向|目標|產品經理|主管'
  };

  // 帶有情緒或強調的回答，代表使用者真的在意該題的主題（加權 +2）
  var EMOTION = /怕|擔心|焦慮|不安|慌|撐不|在意|最想|很重要|不能|底線|可惜|開心|成就感/;

  function store(key) {
    return {
      get: function () { try { return JSON.parse(localStorage.getItem(key) || '{}'); } catch (e) { return {}; } },
      set: function (v) { try { localStorage.setItem(key, JSON.stringify(v)); } catch (e) {} },
      clear: function () { try { localStorage.removeItem(key); } catch (e) {} }
    };
  }

  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }

  document.querySelectorAll('.qual').forEach(function (root) {
    var job = root.dataset.job || location.pathname;
    var st = store('qual:' + job);
    var themes = DEFAULT_THEMES;
    try { if (root.dataset.themes) themes = JSON.parse(root.dataset.themes); } catch (e) {}
    var risks = (root.dataset.risks || '').split(',').map(function (s) { return s.trim(); }).filter(Boolean);
    var qs = Array.prototype.slice.call(root.querySelectorAll('.qual-q'));
    var progress = root.querySelector('.qual-progress');
    var btnPrev = root.querySelector('[data-act="prev"]');
    var btnNext = root.querySelector('[data-act="next"]');
    var out = root.querySelector('.qual-out');
    var state = st.get();
    state.answers = state.answers || {};
    state.follow = state.follow || {};
    var idx = Math.min(state.idx || 0, qs.length - 1);

    function save() { state.idx = idx; st.set(state); }

    function pickFollowup(q, text) {
      if (text.replace(/\s/g, '').length < 30) return '可以多說一點嗎？例如一個具體的情境，或你為什麼會這樣想。';
      var rules = [];
      try { rules = JSON.parse(q.dataset.followups || '[]'); } catch (e) {}
      for (var i = 0; i < rules.length; i++) {
        if (rules[i]['if'] && new RegExp(rules[i]['if']).test(text)) return rules[i].ask;
      }
      for (var j = 0; j < rules.length; j++) if (rules[j]['default']) return rules[j]['default'];
      return '可以舉一個具體的例子嗎？';
    }

    function renderFollow(q, i) {
      var box = q.querySelector('.qual-follow');
      if (box) box.remove();
      var f = state.follow[i];
      if (!f) return;
      box = el('div', 'qual-follow');
      box.appendChild(el('label', null, '追問：' + f.ask));
      var ta = el('textarea');
      ta.rows = 3;
      ta.value = f.answer || '';
      ta.addEventListener('input', function () { f.answer = ta.value; save(); });
      box.appendChild(ta);
      q.appendChild(box);
    }

    function show() {
      qs.forEach(function (q, i) {
        q.classList.toggle('active', i === idx);
        var ta = q.querySelector('textarea');
        if (ta && state.answers[i] != null && !ta.value) ta.value = state.answers[i];
        renderFollow(q, i);
      });
      if (progress) progress.textContent = '第 ' + (idx + 1) + ' / ' + qs.length + ' 題';
      if (btnPrev) btnPrev.disabled = idx === 0;
      save();
    }

    qs.forEach(function (q, i) {
      var ta = q.querySelector('textarea');
      ta.addEventListener('input', function () { state.answers[i] = ta.value; save(); });
    });

    btnPrev && btnPrev.addEventListener('click', function () { if (idx > 0) { idx--; show(); } });
    btnNext && btnNext.addEventListener('click', function () {
      var q = qs[idx];
      var text = (q.querySelector('textarea').value || '').trim();
      if (!text) { q.querySelector('textarea').focus(); return; }
      if (!state.follow[idx]) {           // 第一次按：先追問
        state.follow[idx] = { ask: pickFollowup(q, text), answer: '' };
        show();
        q.querySelector('.qual-follow textarea').focus();
        return;
      }
      if (idx < qs.length - 1) { idx++; show(); return; }
      summarize();
    });

    root.querySelector('[data-act="reset"]') && root.querySelector('[data-act="reset"]').addEventListener('click', function () {
      st.clear(); state = { answers: {}, follow: {} }; idx = 0;
      qs.forEach(function (q) { q.querySelector('textarea').value = ''; });
      if (out) out.classList.remove('show');
      show();
    });

    function allText() {
      var t = '';
      qs.forEach(function (q, i) {
        t += (state.answers[i] || '') + '\n' + ((state.follow[i] && state.follow[i].answer) || '') + '\n';
      });
      return t;
    }

    function summarize() {
      var text = allText();
      var tally = {};
      Object.keys(themes).forEach(function (k) {
        var m = text.match(new RegExp(themes[k], 'g'));
        tally[k] = m ? m.length : 0;
      });
      qs.forEach(function (q, i) {
        var t = (state.answers[i] || '') + ((state.follow[i] && state.follow[i].answer) || '');
        var th = q.dataset.theme;
        if (th && EMOTION.test(t)) tally[th] = (tally[th] || 0) + 2;
      });
      var counts = Object.keys(tally).map(function (k) { return { theme: k, n: tally[k] }; })
        .filter(function (x) { return x.n > 0; }).sort(function (a, b) { return b.n - a.n; });
      var top = counts.slice(0, 3).map(function (x) { return x.theme; });
      var overlap = top.filter(function (t) { return risks.indexOf(t) >= 0; });
      var silent = risks.filter(function (r) { return !counts.some(function (c) { return c.theme === r; }); });

      var box = out.querySelector('[data-summary]');
      box.textContent = '';
      box.appendChild(el('p', null, '你最在意的主題（提及次數＋情緒強度）：' + (counts.length ? counts.slice(0, 5).map(function (c) { return c.theme + '（' + c.n + '）'; }).join('、') : '（未偵測到明顯主題）')));
      if (overlap.length) box.appendChild(el('p', null, '⚠️ 你最在意的「' + overlap.join('、') + '」，正好是這個職缺的風險點，請回頭看公司診斷，並在面試中優先確認。'));
      else if (top.length) box.appendChild(el('p', null, '✅ 你最在意的事，不在這個職缺的主要風險清單上。'));
      if (silent.length) box.appendChild(el('p', null, '❓ 你完全沒提到「' + silent.join('、') + '」，但這是這個職缺的風險，建議想一想自己能不能接受。'));

      var md = '# 質性訪談紀錄｜' + (root.dataset.title || job) + '\n\n- slug：' + job + '\n- 日期：' + new Date().toISOString().slice(0, 10) + '\n- 交給 AI：請依 rules/career-fit.md §5.3 分析這份紀錄，有矛盾或模糊處先問我。\n\n';
      qs.forEach(function (q, i) {
        md += '## Q' + (i + 1) + '. ' + q.querySelector('label').textContent.trim() + '\n\n> ' + (state.answers[i] || '').replace(/\n/g, '\n> ') + '\n\n';
        if (state.follow[i]) md += '**追問：' + state.follow[i].ask + '**\n\n> ' + (state.follow[i].answer || '（未回答）').replace(/\n/g, '\n> ') + '\n\n';
      });
      md += '## 網頁初步歸納\n\n- 最常提到：' + counts.map(function (c) { return c.theme + '（' + c.n + '）'; }).join('、') + '\n- 與職缺風險重疊：' + (overlap.join('、') || '無') + '\n- 未提到的風險：' + (silent.join('、') || '無') + '\n';
      out.querySelector('textarea').value = md;
      out.classList.add('show');
      out.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    out && out.querySelector('[data-act="copy"]').addEventListener('click', function () {
      var ta = out.querySelector('textarea'); ta.select();
      try { navigator.clipboard.writeText(ta.value); } catch (e) { document.execCommand('copy'); }
    });
    out && out.querySelector('[data-act="download"]').addEventListener('click', function () {
      var blob = new Blob([out.querySelector('textarea').value], { type: 'text/markdown' });
      var a = el('a'); a.href = URL.createObjectURL(blob); a.download = job + '-qual.md'; a.click();
      setTimeout(function () { URL.revokeObjectURL(a.href); }, 1000);
    });

    show();
  });
})();
