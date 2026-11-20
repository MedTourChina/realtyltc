/* The decision sheet: a five-layer go/no-go checklist.
   State lives in this browser's localStorage only — nothing is sent anywhere,
   because there is no server to send it to. */
(function () {
  'use strict';

  var sheet = document.querySelector('[data-sheet]');
  if (!sheet) return;

  var KEY = 'ltc-decision-sheet-v1';
  var boxes = Array.prototype.slice.call(sheet.querySelectorAll('input[type="checkbox"]'));
  var progressEl = sheet.querySelector('[data-progress]');
  var barEl = sheet.querySelector('[data-bar]');
  var verdictEl = sheet.querySelector('[data-verdict]');
  var layerEls = Array.prototype.slice.call(sheet.querySelectorAll('[data-layer]'));

  function load() {
    try {
      return JSON.parse(window.localStorage.getItem(KEY) || '{}');
    } catch (e) {
      return {};
    }
  }

  function save(state) {
    try {
      window.localStorage.setItem(KEY, JSON.stringify(state));
    } catch (e) {
      /* private mode or storage disabled: the sheet still works, it just
         will not remember between visits. */
    }
  }

  function layerState(layerId) {
    var el = layerEls.find(function (n) {
      return n.getAttribute('data-layer') === layerId;
    });
    if (!el) return { total: 0, done: 0, stops: 0, slug: '', name: '' };
    var checks = Array.prototype.slice.call(el.querySelectorAll('[data-check]'));
    var stops = Array.prototype.slice.call(el.querySelectorAll('[data-stop]'));
    return {
      total: checks.length,
      done: checks.filter(function (c) { return c.checked; }).length,
      stops: stops.filter(function (c) { return c.checked; }).length,
      slug: el.getAttribute('data-slug') || '',
      name: el.getAttribute('data-name') || ('layer ' + layerId),
    };
  }

  function render() {
    var ids = layerEls.map(function (n) { return n.getAttribute('data-layer'); });
    var cleared = 0;
    var stopAt = null;

    ids.forEach(function (id) {
      var s = layerState(id);
      if (s.stops > 0 && stopAt === null) stopAt = s;
      if (s.total > 0 && s.done === s.total) cleared += 1;
    });

    if (progressEl) {
      progressEl.textContent = cleared + ' of ' + ids.length + ' layers cleared';
    }
    if (barEl) {
      barEl.style.width = Math.round((cleared / ids.length) * 100) + '%';
    }

    if (!verdictEl) return;

    var total = boxes.filter(function (b) { return b.checked; }).length;

    if (stopAt) {
      verdictEl.hidden = false;
      verdictEl.className = 'sheet-verdict verdict-stop';
      verdictEl.innerHTML =
        '<strong>Stop at layer ' + stopAt.name + '.</strong> You have ticked a stop condition. ' +
        'That is the cheapest outcome this sheet can give you — the purchase ends before any money is committed. ' +
        (stopAt.slug
          ? '<a href="/framework/' + stopAt.slug + '/">Re-read layer ' + stopAt.name + '</a>.'
          : '');
      return;
    }

    if (total === 0) {
      verdictEl.hidden = true;
      return;
    }

    verdictEl.hidden = false;
    if (cleared === ids.length) {
      verdictEl.className = 'sheet-verdict verdict-go';
      verdictEl.innerHTML =
        '<strong>All five layers cleared.</strong> You have a decision, not a set of assumptions. ' +
        'Take the completed sheet to your lawyer and ask them to challenge any line you were unsure about.';
    } else {
      verdictEl.className = 'sheet-verdict verdict-partial';
      verdictEl.innerHTML =
        '<strong>' + cleared + ' of ' + ids.length + ' layers cleared.</strong> ' +
        'Keep going in order — the remaining layers are cheaper to fail now than after a deposit.';
    }
  }

  var state = load();
  boxes.forEach(function (box) {
    var id = box.getAttribute('data-check') || box.getAttribute('data-stop');
    if (state[id]) box.checked = true;
    box.addEventListener('change', function () {
      state[id] = box.checked;
      save(state);
      render();
    });
  });

  var reset = sheet.querySelector('[data-sheet-reset]');
  if (reset) {
    reset.addEventListener('click', function () {
      boxes.forEach(function (b) { b.checked = false; });
      state = {};
      save(state);
      render();
    });
  }

  render();
})();
