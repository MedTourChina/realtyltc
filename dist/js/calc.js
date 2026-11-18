/* The three calculators. Everything runs locally; nothing is transmitted,
   stored or logged. No network calls appear anywhere in this file. */
(function () {
  'use strict';

  var money = function (n) {
    if (!isFinite(n)) return '—';
    return '¥' + Math.round(n).toLocaleString('en-US');
  };

  var short = function (n) {
    if (!isFinite(n)) return '—';
    var abs = Math.abs(n);
    var sign = n < 0 ? '−' : '';
    if (abs >= 1000000) return sign + '¥' + (abs / 1000000).toFixed(2).replace(/\.?0+$/, '') + 'M';
    if (abs >= 1000) return sign + '¥' + Math.round(abs / 1000) + 'k';
    return sign + '¥' + Math.round(abs);
  };

  var pctOf = function (part, base) {
    if (!base) return '—';
    return ((part / base) * 100).toFixed(1) + '% of price';
  };

  var num = function (el, fallback) {
    var v = parseFloat(el && el.value);
    return isFinite(v) ? v : fallback;
  };

  /* ------------------------------------------------------------ eligibility */

  var quiz = document.querySelector('[data-quiz="eligibility"]');
  if (quiz) {
    var run = quiz.querySelector('[data-quiz-run]');
    var out = quiz.querySelector('[data-quiz-result]');

    var answers = function () {
      var a = {};
      ['permit', 'tenure', 'city', 'existing', 'type'].forEach(function (name) {
        var checked = quiz.querySelector('input[name="' + name + '"]:checked');
        a[name] = checked ? checked.value : null;
      });
      return a;
    };

    var evaluate = function (a) {
      var blockers = [];
      var cautions = [];

      if (a.permit === 'other') {
        blockers.push('Your permit is for tourism or business. The entitlement requires a work or study residence permit — this has to change before anything else matters.');
      } else if (a.permit === 'family') {
        blockers.push('A family-reunion permit is not a work or study permit. Buying is generally assessed against employment or enrolment records you do not have.');
      }

      if (a.tenure === 'short') {
        cautions.push('You cannot yet document twelve months. This is usually a matter of waiting, not of structuring.');
      } else if (a.tenure === 'gap') {
        cautions.push('Gaps between employers are the most common reason a registration stalls. Ask the district bureau whether your specific history is continuous enough.');
      }

      if (a.city === 'other') {
        blockers.push('The purchase must be in the city where your employment or study is registered. A different city is not available to you under the individual route.');
      } else if (a.city === 'unsure') {
        cautions.push('If your employer is registered elsewhere but you work here, the city requirement may fail. Confirm the registered address on your employment contract.');
      }

      if (a.existing === 'spouse') {
        blockers.push('A spouse who already owns residential property in China ordinarily uses the household entitlement. This is assessed on records, not on intentions.');
      } else if (a.existing === 'self') {
        blockers.push('You already hold residential property in China. The entitlement is one self-use home, and it has been used.');
      }

      if (a.type === 'commercial') {
        blockers.push('40- and 50-year commercial stock is generally closed to foreign individual buyers, and it is a different asset class even where it is available.');
      } else if (a.type === 'unsure') {
        cautions.push('Establish the registered use before anything else. Ask for the 用途 field on the title certificate — one character changes the asset class.');
      }

      var verdict, tone;
      if (blockers.length) {
        verdict = 'Not available as things stand';
        tone = 'result-no';
      } else if (a.tenure === 'short') {
        verdict = 'Not yet';
        tone = 'result-maybe';
      } else if (cautions.length) {
        verdict = 'Likely, with conditions to confirm';
        tone = 'result-maybe';
      } else {
        verdict = 'Likely eligible';
        tone = 'result-yes';
      }

      return { verdict: verdict, tone: tone, blockers: blockers, cautions: cautions };
    };

    var render = function (r) {
      var html = '<div class="verdict ' + r.tone + '">' + r.verdict + '</div>';

      if (r.blockers.length) {
        html += '<p class="quiz-sub">What blocks it</p><ul class="risk-list">';
        r.blockers.forEach(function (b) { html += '<li>' + b + '</li>'; });
        html += '</ul>';
      }

      if (r.cautions.length) {
        html += '<p class="quiz-sub">What still needs confirming</p><ul class="risk-list">';
        r.cautions.forEach(function (c) { html += '<li>' + c + '</li>'; });
        html += '</ul>';
      }

      html += '<p class="quiz-sub">The next step</p>';
      html += '<p>This is an indicative position, not a permission. Take your documents to the district housing bureau and ask for a written materials checklist — the wording is on the verification page.</p>';
      html += '<p><a class="btn btn-primary" href="/verify/">How to verify it in person</a></p>';

      out.hidden = false;
      out.innerHTML = html;
    };

    run.addEventListener('click', function () {
      var a = answers();
      var missing = Object.keys(a).filter(function (k) { return !a[k]; });
      if (missing.length) {
        out.hidden = false;
        out.innerHTML = '<div class="verdict result-maybe">Answer all five questions first</div>' +
          '<p class="quiz-sub">' + missing.length + ' left. Each one is a fact the housing bureau will establish, so none can be skipped.</p>';
        return;
      }
      render(evaluate(a));
    });
  }

  /* ---------------------------------------------------------- purchase cost */

  var cost = document.querySelector('[data-calc="cost"]');
  if (cost) {
    var get = function (name) { return cost.querySelector('[data-in="' + name + '"]'); };
    var put = function (name, value) {
      var el = cost.querySelector('[data-out="' + name + '"]');
      if (el) el.textContent = value;
    };

    var computeCost = function () {
      var price = Math.max(num(get('price'), 0), 0);
      var area = Math.max(num(get('area'), 0), 0);
      var home = get('home').value;
      var use = get('use').value;
      var agencyRate = Math.max(num(get('agency'), 1), 0) / 100;
      var sellerOnBuyer = get('seller').value === 'buyer';

      var deedRate;
      if (use === 'commercial' || home === 'third') deedRate = 0.03;
      else if (area <= 140) deedRate = 0.01;
      else deedRate = home === 'first' ? 0.015 : 0.02;

      var deed = price * deedRate;
      var agency = price * agencyRate;
      var notary = Math.max(price * 0.0015, 1000);
      var reg = 80;
      var legal = 20000;
      var sellerTax = sellerOnBuyer ? price * 0.063 : 0;
      var extra = deed + agency + notary + reg + legal + sellerTax;

      put('total', short(extra) + '  ·  ' + pctOf(extra, price));
      put('deed', money(deed) + '  (' + (deedRate * 100).toFixed(1) + '%)');
      put('agency', money(agency));
      put('notary', money(notary));
      put('reg', money(reg));
      put('legal', money(legal));
      put('sellerTax', sellerOnBuyer ? money(sellerTax) + '  (5.3% VAT + 1% income tax)' : 'Seller bears');
      put('grand', money(price + extra));

      var note = 'Deed tax is charged on the whole price at the rate for your band. ';
      if (area > 140) note += 'At ' + area + 'm² you are above the 140m² threshold, so the higher rate applies to the entire price, not just the excess. ';
      else if (area >= 135) note += 'At ' + area + 'm² you are close to the 140m² threshold — a unit a few square metres smaller would be materially cheaper to close. ';
      if (use === 'commercial') note += 'Commercial stock is charged at the statutory 3% with no first-home reduction. ';
      if (sellerOnBuyer) note += 'You have elected to absorb the seller-side taxes; confirm this in the contract rather than at completion.';
      put('note', note.trim());
    };

    cost.querySelectorAll('[data-in]').forEach(function (el) {
      el.addEventListener('input', computeCost);
      el.addEventListener('change', computeCost);
    });
    computeCost();
  }

  /* ------------------------------------------------------------ rent vs buy */

  var rb = document.querySelector('[data-calc="rentbuy"]');
  if (rb) {
    var rget = function (name) { return rb.querySelector('[data-in="' + name + '"]'); };
    var rput = function (name, value) {
      var el = rb.querySelector('[data-out="' + name + '"]');
      if (el) el.textContent = value;
    };

    var amortise = function (principal, annualRate, months) {
      var r = annualRate / 100 / 12;
      if (r <= 0) return principal / months;
      var k = Math.pow(1 + r, months);
      return (principal * r * k) / (k - 1);
    };

    var balanceAfter = function (principal, annualRate, months, paid) {
      var r = annualRate / 100 / 12;
      if (r <= 0) return Math.max(principal - (principal / months) * paid, 0);
      var k = Math.pow(1 + r, paid);
      var pmt = amortise(principal, annualRate, months);
      return Math.max(principal * k - pmt * ((k - 1) / r), 0);
    };

    var computeRb = function () {
      var price = Math.max(num(rget('price'), 0), 0);
      var rent = Math.max(num(rget('rent'), 0), 0);
      var downPct = Math.min(Math.max(num(rget('down'), 40), 5), 100);
      var rate = Math.max(num(rget('rate'), 3.2), 0);
      var years = Math.min(Math.max(Math.round(num(rget('years'), 7)), 1), 30);
      var growth = num(rget('growth'), 0) / 100;

      var down = price * (downPct / 100);
      var loan = price - down;
      var termMonths = 300;
      var monthly = amortise(loan, rate, termMonths);
      var purchaseCost = price * 0.04;
      var saleCostRate = 0.04;

      var paidMonths = Math.min(years * 12, termMonths);
      var totalPayments = monthly * paidMonths;
      var remaining = balanceAfter(loan, rate, termMonths, paidMonths);

      var futureValue = price * Math.pow(1 + growth, years);
      var saleProceeds = futureValue * (1 - saleCostRate);
      var equity = saleProceeds - remaining;

      var cashOut = down + purchaseCost + totalPayments;
      var buyNet = equity - cashOut;

      var rentPaid = 0;
      for (var y = 0; y < years; y++) {
        rentPaid += rent * 12 * Math.pow(1.03, y);
      }
      var deposit = down + purchaseCost;
      var depositFuture = deposit * Math.pow(1.04, years);
      var rentNet = depositFuture - deposit - rentPaid;

      var delta = buyNet - rentNet;

      rput('horizon', String(years));
      rput('delta', short(Math.round(delta)));
      rput('buyOut', money(cashOut));
      rput('buyEquity', money(equity));
      rput('rentPaid', money(rentPaid));
      rput('rentInvest', money(depositFuture - deposit));

      var verdict, note;
      if (delta > 0) {
        verdict = 'Buying is ahead by ' + short(Math.round(delta));
        note = 'Over ' + years + ' years, under these assumptions, buying leaves you better off. Change the growth assumption first — it is the input nobody can forecast.';
      } else {
        verdict = 'Renting is ahead by ' + short(Math.round(-delta));
        note = 'Over ' + years + ' years, renting and investing the deposit leaves you better off. This is the common result at a 1.6% yield with a flat price, which is why the arithmetic has to be run rather than assumed.';
      }
      rput('verdict', verdict);
      rput('note', note);
    };

    rb.querySelectorAll('[data-in]').forEach(function (el) {
      el.addEventListener('input', computeRb);
      el.addEventListener('change', computeRb);
    });
    computeRb();
  }
})();
