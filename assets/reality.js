/* 求職小幫手 Pro — 面試紀錄上傳與比對（rules/reality-check.md §2.3）
   讀入 .txt／.md 或貼上的文字，找出提到各「待確認」項目的句子，讓使用者逐項判定後匯出 Markdown。
   檔案只在瀏覽器內用 FileReader 讀取，不會上傳到任何伺服器。 */
(function () {
  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }

  document.querySelectorAll('.intake').forEach(function (root) {
    var job = root.dataset.job || location.pathname;
    var key = 'intake:' + job;
    var fileInput = root.querySelector('input[type="file"]');
    var text = root.querySelector('.intake-text');
    var items = Array.prototype.slice.call(root.querySelectorAll('.intake-items > li'));
    var status = root.querySelector('.intake-status');
    var out = root.querySelector('.intake-out');

    function load() { try { return JSON.parse(localStorage.getItem(key) || '{}'); } catch (e) { return {}; } }
    function save() {
      var data = { text: text.value, marks: {}, evidence: {} };
      items.forEach(function (li) {
        var id = li.dataset.item;
        var c = li.querySelector('input[type="radio"]:checked');
        if (c) data.marks[id] = c.value;
        data.evidence[id] = li.querySelector('.evidence').value;
      });
      try { localStorage.setItem(key, JSON.stringify(data)); } catch (e) {}
    }

    var saved = load();
    if (saved.text) text.value = saved.text;
    items.forEach(function (li) {
      var id = li.dataset.item;
      if (saved.marks && saved.marks[id]) {
        var r = li.querySelector('input[value="' + saved.marks[id] + '"]');
        if (r) r.checked = true;
      }
      if (saved.evidence && saved.evidence[id]) li.querySelector('.evidence').value = saved.evidence[id];
    });
    root.addEventListener('change', save);
    root.addEventListener('input', save);

    fileInput && fileInput.addEventListener('change', function () {
      var f = fileInput.files && fileInput.files[0];
      if (!f) return;
      if (f.size > 2 * 1024 * 1024) { status.textContent = '檔案太大（上限 2MB），請改貼上重點文字。'; return; }
      var reader = new FileReader();
      reader.onload = function () { text.value = String(reader.result || ''); save(); scan(); };
      reader.readAsText(f, 'utf-8');
    });

    function sentences(s) {
      return s.split(/[\n。！？!?]+/).map(function (x) { return x.replace(/^[\s>*#-]+/, '').trim(); }).filter(function (x) { return x.length > 1; });
    }

    function scan() {
      var ss = sentences(text.value);
      var found = 0;
      items.forEach(function (li) {
        var hits = li.querySelector('.hits');
        hits.textContent = '';
        var rx;
        try { rx = new RegExp(li.dataset.keywords); } catch (e) { return; }
        var match = ss.filter(function (s) { return rx.test(s); }).slice(0, 3);
        if (match.length) {
          found++;
          hits.appendChild(el('div', 'label', '紀錄中可能相關的段落：'));
          var ul = el('ul');
          match.forEach(function (m) { ul.appendChild(el('li', null, '「' + m + '」')); });
          hits.appendChild(ul);
        } else {
          hits.appendChild(el('div', 'label', '紀錄中沒有找到相關段落 → 可能要在下一輪追問。'));
        }
      });
      status.textContent = '共 ' + items.length + ' 個待確認項目，紀錄中找到 ' + found + ' 項的相關段落。請逐項判定並補上依據。';
    }

    root.querySelector('[data-act="scan"]').addEventListener('click', function () {
      if (!text.value.trim()) { status.textContent = '請先上傳檔案或貼上面試紀錄。'; return; }
      scan();
    });

    root.querySelector('[data-act="export"]').addEventListener('click', function () {
      var md = '# 現實度比對紀錄｜' + (root.dataset.title || job) + '\n\n- slug：' + job + '\n- 日期：' + new Date().toISOString().slice(0, 10) +
        '\n- 交給 AI：請依 rules/reality-check.md 產出完整的現實度匹配分析（真實面試請存 private/）。\n\n## 待確認項目判定\n\n| 項目 | 判定 | 依據 |\n|---|---|---|\n';
      items.forEach(function (li) {
        var c = li.querySelector('input[type="radio"]:checked');
        var name = li.querySelector('strong').textContent.replace(/\|/g, '／');
        md += '| ' + name + ' | ' + (c ? c.value : '（未判定）') + ' | ' + (li.querySelector('.evidence').value || '').replace(/\|/g, '／') + ' |\n';
      });
      md += '\n## 面試紀錄原文\n\n' + text.value + '\n';
      out.querySelector('textarea').value = md;
      out.classList.add('show');
    });

    out.querySelector('[data-act="copy"]').addEventListener('click', function () {
      var ta = out.querySelector('textarea'); ta.select();
      try { navigator.clipboard.writeText(ta.value); } catch (e) { document.execCommand('copy'); }
    });
    out.querySelector('[data-act="download"]').addEventListener('click', function () {
      var blob = new Blob([out.querySelector('textarea').value], { type: 'text/markdown' });
      var a = el('a'); a.href = URL.createObjectURL(blob); a.download = job + '-reality.md'; a.click();
      setTimeout(function () { URL.revokeObjectURL(a.href); }, 1000);
    });
  });
})();
