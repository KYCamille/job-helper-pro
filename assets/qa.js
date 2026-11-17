/* 求職小幫手 Pro — 職涯願景互動問答（rules/career-fit.md §5.2）
   每個 <input> 帶 data-weight（+2 ~ -2）。答案只存在本機瀏覽器。 */
(function () {
  document.querySelectorAll('form.qa-form').forEach(function (form) {
    var key = 'qa:' + (form.dataset.job || location.pathname);
    var result = document.getElementById(form.dataset.result);
    var store = {
      get: function () { try { return JSON.parse(localStorage.getItem(key) || '{}'); } catch (e) { return {}; } },
      set: function (v) { try { localStorage.setItem(key, JSON.stringify(v)); } catch (e) {} },
      clear: function () { try { localStorage.removeItem(key); } catch (e) {} }
    };

    var saved = store.get();
    Object.keys(saved).forEach(function (name) {
      var el = form.querySelector('input[name="' + name + '"][value="' + saved[name] + '"]');
      if (el) el.checked = true;
    });

    function evaluate() {
      var sets = form.querySelectorAll('fieldset');
      var answered = 0, score = 0, max = 0, conflicts = [];
      sets.forEach(function (fs) {
        var picked = fs.querySelector('input:checked');
        max += 2;
        if (!picked) return;
        answered++;
        var w = Number(picked.dataset.weight || 0);
        score += w;
        if (w < 0) conflicts.push(fs.querySelector('legend').textContent.replace(/^\d+\.\s*/, ''));
      });
      return { answered: answered, total: sets.length, score: score, max: max, conflicts: conflicts };
    }

    function render() {
      if (!result) return;
      var r = evaluate();
      var out = result.querySelector('[data-out]');
      if (r.answered < r.total) {
        out.innerHTML = '還有 <strong>' + (r.total - r.answered) + '</strong> 題沒回答。';
        result.classList.add('show');
        return;
      }
      var pct = Math.round((r.score + r.max) / (2 * r.max) * 100);
      var level = pct >= 70 ? ['badge-high', '方向一致，值得積極爭取']
                : pct >= 50 ? ['badge-mid', '部分一致，先在面試中確認衝突點']
                : ['badge-low', '和你的願景衝突較多，建議再想想'];
      var html = '<p><span class="badge ' + level[0] + '">願景對齊 ' + pct + '%</span>　' + level[1] + '</p>';
      if (r.conflicts.length) {
        html += '<p>需要特別確認的地方：</p><ul>' + r.conflicts.map(function (c) { return '<li>' + c + '</li>'; }).join('') + '</ul>';
      }
      out.innerHTML = html;
      result.classList.add('show');
    }

    form.addEventListener('change', function () {
      var data = {};
      form.querySelectorAll('input:checked').forEach(function (el) { data[el.name] = el.value; });
      store.set(data);
    });
    form.addEventListener('submit', function (e) { e.preventDefault(); render(); });
    form.addEventListener('reset', function () { store.clear(); if (result) result.classList.remove('show'); });
  });
})();
