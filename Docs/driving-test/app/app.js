/* G1 Practice. Plain ES5 so it runs on older tablets. Data comes from window.G1 (built by build.py). */
(function () {
  'use strict';

  var D = window.G1;
  var app = document.getElementById('app');
  var LETTERS = 'ABCD';
  var HALF_KEYS = ['signs', 'rules'];
  var CAT = {};
  var TYPELABEL = {};
  D.cats.forEach(function (c) { CAT[c.id] = c; });
  HALF_KEYS.forEach(function (h) {
    D.types[h].forEach(function (t) { TYPELABEL[t.key] = t.label; });
  });

  // ------------------------------------------------------------ saved progress (this device only)
  var KEY = 'g1-practice-v1';
  // No-save (guest) mode: nothing is read from or written to the browser. Turned on by the
  // g1-practice-no-save.html build (window.G1_NOSAVE) or by adding ?nosave to the address.
  var NOSAVE = window.G1_NOSAVE === true || /[?&]nosave\b/.test(location.search);
  var store = loadStore();

  function loadStore() {
    var s = null;
    if (!NOSAVE) {
      try { s = JSON.parse(localStorage.getItem(KEY) || 'null'); } catch (e) { s = null; }
    }
    s = s || {};
    s.p = s.p || {};
    s.mocks = s.mocks || [];
    s.set = s.set || {};
    if (!s.set.scale) s.set.scale = 1;
    if (!s.set.rate) s.set.rate = 1;
    return s;
  }

  function saveStore() {
    if (NOSAVE) return;
    try { localStorage.setItem(KEY, JSON.stringify(store)); } catch (e) { /* private window: progress just isn't kept */ }
  }

  function prog(id) { return store.p[id] || null; }

  function record(q, ok) {
    var p = store.p[q.id] || (store.p[q.id] = { s: 0, c: 0, w: 0, k: 0, m: 0 });
    p.s += 1;
    p.t = Date.now();
    if (ok) {
      p.c += 1;
      p.k += 1;
      if (p.m && p.k >= 2) p.m = 0;   // missed questions leave the list after 2 right in a row
    } else {
      p.w += 1;
      p.k = 0;
      p.m = 1;
    }
    saveStore();
  }

  function mastered(q) { var p = prog(q.id); return !!(p && p.c > 0 && !p.m); }

  function missedList() {
    return D.questions.filter(function (q) { var p = prog(q.id); return p && p.m; });
  }

  // ------------------------------------------------------------ small helpers
  function el(tag, attrs, kids) {
    var n = document.createElement(tag);
    var k;
    if (attrs) {
      for (k in attrs) {
        if (!attrs.hasOwnProperty(k) || attrs[k] === null || attrs[k] === undefined || attrs[k] === false) continue;
        if (k === 'text') n.textContent = attrs[k];
        else if (k === 'html') n.innerHTML = attrs[k];
        else if (k === 'cls') n.className = attrs[k];
        else if (k.indexOf('on') === 0) n.addEventListener(k.slice(2), attrs[k]);
        else n.setAttribute(k, attrs[k]);
      }
    }
    (kids || []).forEach(function (c) {
      if (c === null || c === undefined) return;
      n.appendChild(typeof c === 'string' ? document.createTextNode(c) : c);
    });
    return n;
  }

  function shuffle(a) {
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a;
  }

  function pic(key, alt) {
    return el('span', { cls: 'pic' }, [el('img', { src: D.images[key] || '', alt: alt || 'picture' })]);
  }

  function fillImages(root) {
    var imgs = root.querySelectorAll('img[data-img]');
    for (var i = 0; i < imgs.length; i++) imgs[i].src = D.images[imgs[i].getAttribute('data-img')] || '';
  }

  // A sign's meaning sometimes just repeats its name ("Narrow bridge ahead."). Don't show it twice.
  function sameText(a, b) {
    return String(a).replace(/[.\s]+$/, '').toLowerCase() === String(b).toLowerCase();
  }

  function bar(n, total) {
    var pct = total ? Math.round(100 * n / total) : 0;
    return el('div', { cls: 'bar', role: 'progressbar', 'aria-valuenow': String(pct), 'aria-valuemin': '0', 'aria-valuemax': '100' },
      [el('span', { style: 'width:' + pct + '%' })]);
  }

  function go(hash) {
    if (location.hash === hash) render();
    else location.hash = hash;
  }

  function topbar(title, back) {
    return el('div', { cls: 'topbar' }, [
      el('button', { cls: 'iconbtn', onclick: function () { go(back || '#/'); } }, ['← Back']),
      el('div', { cls: 'title', text: title }),
      el('button', { cls: 'iconbtn', onclick: function () { go('#/'); } }, ['🏠 Home'])
    ]);
  }

  function applyScale() {
    document.documentElement.style.fontSize = Math.round(18 * store.set.scale) + 'px';
  }

  // ------------------------------------------------------------ read aloud (browser speech)
  var TTS = !!(window.speechSynthesis && window.SpeechSynthesisUtterance);
  var voice = null;

  function pickVoice() {
    if (!TTS) return null;
    var vs = window.speechSynthesis.getVoices() || [];
    var pref = ['en-CA', 'en-US', 'en-GB', 'en'];
    for (var i = 0; i < pref.length; i++) {
      for (var j = 0; j < vs.length; j++) {
        if ((vs[j].lang || '').replace('_', '-').indexOf(pref[i]) === 0) return vs[j];
      }
    }
    return null;
  }
  if (TTS && 'onvoiceschanged' in window.speechSynthesis) {
    window.speechSynthesis.onvoiceschanged = function () { voice = pickVoice(); };
  }

  // Spell out units so the voice reads "150 metres", not "150 m".
  function sayable(t) {
    return String(t || '')
      .replace(/km\/h/g, ' kilometres per hour')
      .replace(/(\d)\s?mm\b/g, '$1 millimetres')
      .replace(/(\d)\s?cm\b/g, '$1 centimetres')
      .replace(/(\d)\s?kg\b/g, '$1 kilograms')
      .replace(/(\d)\s?km\b/g, '$1 kilometres')
      .replace(/(\d)\s?m\b/g, '$1 metres')
      .replace(/½/g, 'half')
      .replace(/→/g, ', then ')
      .replace(/[·•]/g, ', ')
      .replace(/\s+/g, ' ')
      .trim();
  }

  function speak(parts) {
    if (!TTS) return;
    var synth = window.speechSynthesis;
    synth.cancel();
    if (!voice) voice = pickVoice();
    (typeof parts === 'string' ? [parts] : parts).forEach(function (t) {
      t = sayable(t);
      if (!t) return;
      var u = new window.SpeechSynthesisUtterance(t);
      u.rate = store.set.rate;
      u.lang = voice ? voice.lang : 'en-CA';
      if (voice) u.voice = voice;
      synth.speak(u);
    });
  }

  function stopSpeaking() { if (TTS) window.speechSynthesis.cancel(); }

  function readQuestion(it) {
    var q = it.q;
    var parts = [q.q];
    if (q.type === 'pick') parts.push('Choose picture A, B, C or D.');
    else it.order.forEach(function (ci, pos) { parts.push(LETTERS[pos] + '. ' + q.c[ci]); });
    speak(parts);
  }

  // ------------------------------------------------------------ choosing questions
  function poolFor(f) {
    return D.questions.filter(function (q) {
      return (!f.half || q.half === f.half) && (!f.cat || q.cat === f.cat) &&
        (!f.type || q.type === f.type) && (!f.ids || f.ids.indexOf(q.id) >= 0);
    });
  }

  // Higher = asked sooner: missed first, then never-seen, then the shakiest ones.
  function priority(q) {
    var p = prog(q.id);
    var r = Math.random();
    if (!p) return 2 + r;
    if (p.m) return 3 + r;
    return Math.max(0, 1 - p.k * 0.25) + (p.w > p.c ? 0.5 : 0) + r * 0.5;
  }

  // Round-robin across question types so every type gets the same weight.
  function pickBalanced(pool, n, pureRandom) {
    var groups = {};
    var keys = [];
    pool.forEach(function (q) {
      if (!groups[q.type]) { groups[q.type] = []; keys.push(q.type); }
      groups[q.type].push(q);
    });
    keys.forEach(function (k) {
      groups[k] = groups[k]
        .map(function (q) { return { q: q, w: pureRandom ? Math.random() : priority(q) }; })
        .sort(function (a, b) { return b.w - a.w; })
        .map(function (x) { return x.q; });
    });
    var out = [];
    while (out.length < n) {
      var added = 0;
      var order = shuffle(keys.slice());
      for (var i = 0; i < order.length && out.length < n; i++) {
        var g = groups[order[i]];
        if (g.length) { out.push(g.shift()); added++; }
      }
      if (!added) break;
    }
    return shuffle(out);
  }

  // ------------------------------------------------------------ quiz sessions
  var session = null;

  function startSession(mode, title, list, back) {
    session = {
      mode: mode, title: title, back: back || '#/', i: 0, finished: false,
      items: list.map(function (q) { return { q: q, order: shuffle([0, 1, 2, 3]), pick: null, done: false }; })
    };
    go('#/quiz');
  }

  function startPractice(f, n, title, back) {
    var pool = poolFor(f);
    if (!pool.length) { window.alert('No questions here yet.'); return; }
    var count = n === 'all' ? pool.length : Math.min(n, pool.length);
    startSession('practice', title, pickBalanced(pool, count), back);
  }

  function startMock() {
    var list = [];
    HALF_KEYS.forEach(function (h) { list = list.concat(pickBalanced(poolFor({ half: h }), 20, true)); });
    startSession('mock', 'Mock G1 test', list, '#/');
  }

  function startMissed() {
    var ids = missedList().map(function (q) { return q.id; });
    if (!ids.length) return;
    startPractice({ ids: ids }, 'all', 'Missed questions', '#/');
  }

  function answer(ci) {
    if (!session || session.finished) return;
    var it = session.items[session.i];
    if (session.mode === 'mock') {
      it.pick = ci;   // you can change your mind until you press Next
      markChosen(it);
      showNext('Next →');
      return;
    }
    if (it.pick !== null) return;
    it.pick = ci;
    it.done = true;
    record(it.q, ci === it.q.ans);
    showAnswer(it, true);
  }

  function choiceButtons() { return app.querySelectorAll('.choice'); }

  function markChosen(it) {
    var bs = choiceButtons();
    for (var i = 0; i < bs.length; i++) {
      var ci = Number(bs[i].getAttribute('data-ci'));
      bs[i].className = 'choice' + (ci === it.pick ? ' chosen' : '');
      bs[i].setAttribute('aria-pressed', ci === it.pick ? 'true' : 'false');
    }
  }

  function showNext(label) {
    var nb = document.getElementById('nextbtn');
    if (!nb) return;
    nb.textContent = session.i === session.items.length - 1 ? (session.mode === 'mock' ? 'See my results' : 'Finish') : label;
    nb.className = 'btn primary';
  }

  function showAnswer(it, fresh) {
    var q = it.q;
    var ok = it.pick === q.ans;
    var bs = choiceButtons();
    for (var i = 0; i < bs.length; i++) {
      var ci = Number(bs[i].getAttribute('data-ci'));
      var cls = 'choice';
      var mark = '';
      if (ci === q.ans) { cls += ' right'; mark = '✅'; }
      else if (ci === it.pick) { cls += ' wrong'; mark = '❌'; }
      bs[i].className = cls;
      bs[i].setAttribute('disabled', 'disabled');
      bs[i].querySelector('.mark').textContent = mark;
    }
    var right = LETTERS[it.order.indexOf(q.ans)];
    var answerText = q.type === 'pick' ? 'picture ' + right : right + '. ' + q.c[q.ans];
    var fb = document.getElementById('fb');
    fb.innerHTML = '';
    fb.appendChild(el('div', { cls: 'feedback ' + (ok ? 'ok' : 'no') }, [
      el('div', { cls: 'verdict', text: ok ? '✅ Correct!' : '❌ Not quite. The answer is ' + answerText }),
      el('p', { text: q.e }),
      q.s ? el('div', { cls: 'quote small', text: (q.f === 'ontario.ca' ? '🌐 ontario.ca: “' : '📖 Driver’s Handbook: “') + q.s + '”' }) : null
    ]));
    showNext('Next question →');
    if (fresh && store.set.auto) speak([ok ? 'Correct.' : 'Not quite. The answer is ' + answerText + '.', q.e]);
  }

  function next() {
    var it = session.items[session.i];
    if (it.pick === null) return;
    if (session.mode === 'mock' && !it.done) {
      record(it.q, it.pick === it.q.ans);
      it.done = true;
    }
    if (session.i < session.items.length - 1) {
      session.i += 1;
      render();
    } else {
      finish();
    }
  }

  function finish() {
    session.finished = true;
    if (session.mode === 'mock') {
      var s = score(session.items.slice(0, 20));
      var r = score(session.items.slice(20));
      store.mocks.push({ t: Date.now(), s: s, r: r });
      if (store.mocks.length > 30) store.mocks.shift();
      saveStore();
    }
    go('#/results');
  }

  function score(items) {
    var n = 0;
    items.forEach(function (it) { if (it.pick === it.q.ans) n++; });
    return n;
  }

  // ------------------------------------------------------------ views
  window.addEventListener('hashchange', render);

  function render() {
    stopSpeaking();
    var parts = location.hash.replace(/^#\/?/, '').split('/');
    app.innerHTML = '';
    window.scrollTo(0, 0);
    switch (parts[0]) {
      case 'half': viewHalf(parts[1]); break;
      case 'guide': viewGuide(parts[1]); break;
      case 'topic': viewTopic(parts[1]); break;
      case 'quiz': viewQuiz(); break;
      case 'results': viewResults(); break;
      case 'flash': viewFlash(parts[1]); break;
      case 'page': viewPage(parts[1]); break;
      case 'settings': viewSettings(); break;
      default: viewHome();
    }
  }

  function halfCard(h) {
    var H = D.halves[h];
    var qs = poolFor({ half: h });
    var m = qs.filter(mastered).length;
    return el('div', { cls: 'card' }, [
      el('h2', { text: H.icon + ' ' + H.title }),
      el('p', { cls: 'muted small', text: H.desc }),
      bar(m, qs.length),
      el('p', { cls: 'small muted', text: m + ' of ' + qs.length + ' questions mastered' }),
      el('button', { cls: 'btn primary', onclick: function () { startPractice({ half: h }, 20, '20 mixed ' + H.title.toLowerCase() + ' questions', '#/'); } },
        ['▶ Practice 20 mixed questions', el('span', { cls: 'sub', text: 'All 5 question types, equal amounts' })]),
      el('button', { cls: 'btn', onclick: function () { go('#/half/' + h); } }, ['📖 Study guide, topics & question types']),
      el('button', { cls: 'btn', onclick: function () { go('#/flash/' + h); } },
        ['🃏 Flashcards', el('span', { cls: 'sub', text: h === 'signs' ? 'Every sign, light and marking' : 'Every number to remember' })])
    ]);
  }

  function viewHome() {
    var missed = missedList().length;
    app.appendChild(el('div', { cls: 'card hero' }, [
      el('h1', { text: 'G1 Practice' }),
      el('p', { text: 'Ontario G1 knowledge test: 40 questions, 20 signs + 20 rules.' }),
      el('p', { cls: 'muted', text: 'You need 16 right in EACH half to pass.' }),
      NOSAVE ? el('p', { cls: 'muted small', text: '🕶 No-save mode: nothing is stored. Close the tab and your progress is gone.' }) : null
    ]));
    if (session && !session.finished) {
      app.appendChild(el('button', { cls: 'btn primary big', onclick: function () { go('#/quiz'); } },
        ['↩ Continue: ' + session.title, el('span', { cls: 'sub', text: 'Question ' + (session.i + 1) + ' of ' + session.items.length })]));
    }
    var row = el('div', { cls: 'row' });
    HALF_KEYS.forEach(function (h) { row.appendChild(el('div', { cls: 'col' }, [halfCard(h)])); });
    app.appendChild(row);
    app.appendChild(el('div', { cls: 'card' }, [
      el('button', { cls: 'btn primary big', onclick: startMock },
        ['🎯 Mock G1 test', el('span', { cls: 'sub', text: '20 signs + 20 rules, marked at the end like the real test' })]),
      el('button', { cls: 'btn big', onclick: startMissed, disabled: missed ? null : 'disabled' },
        ['❌ Missed questions (' + missed + ')', el('span', { cls: 'sub', text: missed ? 'They stay here until you get them right twice in a row' : 'Nothing yet. Questions you get wrong show up here.' })]),
      el('button', { cls: 'btn big', onclick: function () { go('#/page/testday'); } },
        ['📋 Test day', el('span', { cls: 'sub', text: 'What to bring, how it works, and the read-aloud (audio) option' })]),
      el('button', { cls: 'btn', onclick: function () { go('#/settings'); } }, ['⚙️ Text size and read aloud'])
    ]));
    if (store.mocks.length) {
      var list = el('div', {});
      store.mocks.slice(-5).reverse().forEach(function (m) {
        var pass = m.s >= 16 && m.r >= 16;
        list.appendChild(el('p', {}, [
          el('span', { cls: pass ? 'pass' : 'fail', text: pass ? 'PASS ' : 'FAIL ' }),
          'Signs ' + m.s + '/20 · Rules ' + m.r + '/20 · ',
          el('span', { cls: 'muted small', text: new Date(m.t).toLocaleDateString() })
        ]));
      });
      app.appendChild(el('div', { cls: 'card' }, [el('h2', { text: 'Your mock tests' }), list]));
    }
    app.appendChild(el('p', { cls: 'small muted center', text: 'Progress is saved on this device. Questions come from the Official MTO Driver’s Handbook. Built ' + D.built + '.' }));
  }

  function viewHalf(h) {
    if (!D.halves[h]) { go('#/'); return; }
    var H = D.halves[h];
    app.appendChild(topbar(H.icon + ' ' + H.title, '#/'));
    var pool = poolFor({ half: h });

    var practice = el('div', { cls: 'card' }, [
      el('h2', { text: 'Mixed practice' }),
      el('p', { cls: 'muted small', text: 'Every question type comes up equally.' })
    ]);
    var counts = el('div', { cls: 'btnrow' });
    [10, 20, 40, 'all'].forEach(function (n) {
      counts.appendChild(el('button', { cls: 'btn', onclick: function () { startPractice({ half: h }, n, (n === 'all' ? 'All' : n) + ' mixed ' + H.title.toLowerCase() + ' questions', '#/half/' + h); } },
        [n === 'all' ? 'All ' + pool.length : n + ' questions']));
    });
    practice.appendChild(counts);
    app.appendChild(practice);

    var types = el('div', { cls: 'card' }, [el('h2', { text: 'Practice by question type' })]);
    D.types[h].forEach(function (t) {
      var n = poolFor({ half: h, type: t.key }).length;
      types.appendChild(el('button', { cls: 'btn', onclick: function () { startPractice({ half: h, type: t.key }, 20, t.label, '#/half/' + h); } },
        [t.label + ' (' + n + ')', el('span', { cls: 'sub', text: t.desc })]));
    });
    app.appendChild(types);

    var topics = el('div', { cls: 'card' }, [el('h2', { text: 'Topics: study, then practice' })]);
    D.cats.forEach(function (c) {
      if (c.half !== h) return;
      var qs = poolFor({ cat: c.id });
      var m = qs.filter(mastered).length;
      var box = el('div', { cls: 'review' }, [
        el('h3', { text: c.id + ' · ' + c.title }),
        qs.length ? bar(m, qs.length) : null,
        el('p', { cls: 'small muted', text: qs.length ? m + ' of ' + qs.length + ' mastered' : 'Study sheet + flashcards' })
      ]);
      var btns = el('div', { cls: 'btnrow' }, [
        el('button', { cls: 'btn', onclick: function () { go('#/guide/' + c.id); } }, ['📖 Study'])
      ]);
      if (qs.length) {
        btns.appendChild(el('button', { cls: 'btn', onclick: function () { startPractice({ cat: c.id }, 20, c.id + ' · ' + c.title, '#/half/' + h); } }, ['▶ Practice']));
      }
      box.appendChild(btns);
      topics.appendChild(box);
    });
    app.appendChild(topics);

    app.appendChild(el('button', { cls: 'btn big', onclick: function () { go('#/flash/' + h); } }, ['🃏 Flashcards']));
  }

  function readBlocks(root) {
    var out = [];
    var kids = root.children;
    for (var i = 0; i < kids.length; i++) {
      var n = kids[i];
      var tag = n.tagName;
      if (tag === 'UL' || tag === 'OL') {
        var lis = n.querySelectorAll('li');
        for (var j = 0; j < lis.length; j++) {
          var own = '';
          for (var c = 0; c < lis[j].childNodes.length; c++) {
            var cn = lis[j].childNodes[c];
            if (cn.nodeType === 3 || (cn.tagName !== 'UL' && cn.tagName !== 'OL')) own += cn.textContent;
          }
          out.push(own);
        }
      } else if (n.className === 'tablewrap') {
        var rows = n.querySelectorAll('tr');
        for (var r = 0; r < rows.length; r++) {
          var cells = [];
          for (var x = 0; x < rows[r].cells.length; x++) cells.push(rows[r].cells[x].textContent);
          out.push(cells.join('. '));
        }
      } else if (tag !== 'FIGURE') {
        out.push(n.textContent);
      }
    }
    return out;
  }

  function guideCard(htmlText) {
    var g = el('div', { cls: 'card guide', html: htmlText });
    fillImages(g);
    return g;
  }

  function speakButtons(target) {
    if (!TTS) return null;
    return el('div', { cls: 'btnrow' }, [
      el('button', { cls: 'btn', onclick: function () { speak(readBlocks(target)); } }, ['🔊 Read this page']),
      el('button', { cls: 'btn', onclick: stopSpeaking }, ['■ Stop reading'])
    ]);
  }

  function viewGuide(id) {
    var c = CAT[id];
    if (!c) { go('#/'); return; }
    app.appendChild(topbar(c.id + ' · ' + c.title, '#/half/' + c.half));
    var g = guideCard(c.guide);
    app.appendChild(speakButtons(g));
    app.appendChild(g);
    if (c.n) {
      app.appendChild(el('button', { cls: 'btn primary big', onclick: function () { startPractice({ cat: c.id }, 20, c.id + ' · ' + c.title, '#/guide/' + c.id); } },
        ['▶ Practice this topic', el('span', { cls: 'sub', text: c.n + ' questions' })]));
    } else {
      app.appendChild(el('button', { cls: 'btn primary big', onclick: function () { go('#/flash/' + c.half); } }, ['🃏 Drill these with flashcards']));
    }
  }

  function viewTopic(id) {
    var c = CAT[id];
    if (!c || !c.n) { go(c ? '#/guide/' + id : '#/'); return; }
    startPractice({ cat: id }, 20, c.id + ' · ' + c.title, '#/guide/' + id);
  }

  function viewPage(id) {
    var p = null;
    D.pages.forEach(function (x) { if (x.id === id) p = x; });
    if (!p) { go('#/'); return; }
    app.appendChild(topbar(p.title, '#/'));
    var g = guideCard(p.html);
    app.appendChild(speakButtons(g));
    app.appendChild(g);
  }

  function viewQuiz() {
    if (!session) { go('#/'); return; }
    if (session.finished) { go('#/results'); return; }
    var it = session.items[session.i];
    var q = it.q;
    var mock = session.mode === 'mock';
    var total = session.items.length;
    app.appendChild(topbar(session.title, session.back));

    var where = 'Question ' + (session.i + 1) + ' of ' + total;
    if (mock) where += session.i < 20 ? ' · Signs half' : ' · Rules half';
    var card = el('div', { cls: 'card', 'data-qid': q.id }, [
      el('div', { cls: 'qhead' }, [
        el('span', { text: where }),
        TTS ? el('button', { cls: 'iconbtn', onclick: function () { readQuestion(it); } }, ['🔊 Read']) : null
      ]),
      el('div', {}, [
        el('span', { cls: 'chip accent', text: TYPELABEL[q.type] }),
        el('span', { cls: 'chip', text: q.cat + ' · ' + CAT[q.cat].title }),
        q.o ? el('span', { cls: 'chip', text: '⭐ Official MTO sample' }) : null
      ])
    ]);
    if (q.img) card.appendChild(el('div', { cls: 'qpic' }, [pic(q.img, 'Picture for this question')]));
    card.appendChild(el('div', { cls: 'qtext', text: q.q }));

    var box = el('div', { cls: q.type === 'pick' ? 'pickgrid' : 'choices' });
    it.order.forEach(function (ci, pos) {
      box.appendChild(el('button', { cls: 'choice', 'data-ci': String(ci), onclick: function () { answer(ci); } }, [
        el('span', { cls: 'letter', text: LETTERS[pos] }),
        q.type === 'pick' ? pic(q.c[ci], 'Picture ' + LETTERS[pos]) : el('span', { cls: 'ctext', text: q.c[ci] }),
        el('span', { cls: 'mark' })
      ]));
    });
    card.appendChild(box);
    card.appendChild(el('div', { id: 'fb' }));
    card.appendChild(el('button', { id: 'nextbtn', cls: 'btn primary hidden', onclick: next }, ['Next →']));
    if (mock) card.appendChild(el('p', { cls: 'small muted', text: 'Mock test: answers are marked at the end. You can change your answer until you press Next.' }));
    app.appendChild(card);

    if (it.pick !== null) {
      if (mock) { markChosen(it); showNext('Next →'); } else showAnswer(it, false);
    } else if (store.set.auto) {
      readQuestion(it);
    }
  }

  function reviewItem(it, n) {
    var q = it.q;
    var right = LETTERS[it.order.indexOf(q.ans)];
    var mine = it.pick === null ? 'no answer' : LETTERS[it.order.indexOf(it.pick)];
    var box = el('div', { cls: 'review' }, [
      el('p', { cls: 'small muted', text: n + '. ' + TYPELABEL[q.type] + ' · ' + q.cat }),
      q.img ? el('div', { cls: 'qpic' }, [pic(q.img, 'Picture for this question')]) : null,
      el('p', {}, [el('strong', { text: q.q })])
    ]);
    if (q.type === 'pick') {
      box.appendChild(el('p', { text: 'You chose ' + mine + '. The right picture is ' + right + ':' }));
      box.appendChild(el('div', { cls: 'qpic' }, [pic(q.c[q.ans], 'Right answer')]));
    } else {
      box.appendChild(el('p', { cls: 'fail', text: '❌ You chose: ' + (it.pick === null ? mine : mine + '. ' + q.c[it.pick]) }));
      box.appendChild(el('p', { cls: 'pass', text: '✅ Answer: ' + right + '. ' + q.c[q.ans] }));
    }
    box.appendChild(el('p', { text: q.e }));
    return box;
  }

  function typeBreakdown(items) {
    var t = {};
    var keys = [];
    items.forEach(function (it) {
      var k = it.q.type;
      if (!t[k]) { t[k] = { n: 0, ok: 0 }; keys.push(k); }
      t[k].n += 1;
      if (it.pick === it.q.ans) t[k].ok += 1;
    });
    var box = el('div', {}, [el('h3', { text: 'By question type' })]);
    keys.forEach(function (k) {
      box.appendChild(el('p', { text: TYPELABEL[k] + ': ' + t[k].ok + ' / ' + t[k].n }));
    });
    return box;
  }

  function viewResults() {
    if (!session || !session.finished) { go('#/'); return; }
    var items = session.items;
    app.appendChild(topbar('Results', '#/'));
    var card = el('div', { cls: 'card center' });
    if (session.mode === 'mock') {
      var s = score(items.slice(0, 20));
      var r = score(items.slice(20));
      var pass = s >= 16 && r >= 16;
      card.appendChild(el('div', { cls: 'score ' + (pass ? 'pass' : 'fail'), text: pass ? 'PASS 🎉' : 'Not yet' }));
      card.appendChild(el('p', {}, ['🚸 Signs: ', el('strong', { text: s + ' / 20' }), s >= 16 ? ' ✅' : ' ❌ (need 16)']));
      card.appendChild(el('p', {}, ['📘 Rules: ', el('strong', { text: r + ' / 20' }), r >= 16 ? ' ✅' : ' ❌ (need 16)']));
    } else {
      var ok = score(items);
      card.appendChild(el('div', { cls: 'score', text: ok + ' / ' + items.length }));
      card.appendChild(el('p', { cls: 'muted', text: Math.round(100 * ok / items.length) + '% right · 80% is the pass mark' }));
    }
    app.appendChild(card);
    app.appendChild(el('div', { cls: 'card' }, [typeBreakdown(items)]));

    var wrong = items.filter(function (it) { return it.pick !== it.q.ans; });
    var again = el('div', { cls: 'btnrow' });
    if (wrong.length) {
      again.appendChild(el('button', { cls: 'btn primary', onclick: function () {
        startPractice({ ids: wrong.map(function (it) { return it.q.id; }) }, 'all', 'Practice my mistakes', '#/');
      } }, ['▶ Practice my ' + wrong.length + ' mistakes']));
    }
    again.appendChild(el('button', { cls: 'btn', onclick: function () { go('#/'); } }, ['🏠 Home']));
    app.appendChild(again);

    if (wrong.length) {
      var rev = el('div', { cls: 'card' }, [el('h2', { text: 'Review your mistakes' })]);
      wrong.forEach(function (it, n) { rev.appendChild(reviewItem(it, n + 1)); });
      app.appendChild(rev);
    }
  }

  var flashState = null;

  function viewFlash(h) {
    if (!D.flash[h]) { go('#/'); return; }
    if (!flashState || flashState.h !== h) flashState = { h: h, cards: shuffle(D.flash[h].slice()), i: 0, flipped: false };
    var f = flashState;
    var c = f.cards[f.i];
    app.appendChild(topbar('Flashcards: ' + D.halves[h].title, '#/half/' + h));
    app.appendChild(el('p', { cls: 'muted center', text: 'Card ' + (f.i + 1) + ' of ' + f.cards.length + ' · tap the card to flip it' }));

    var face;
    if (h === 'signs') {
      face = f.flipped ?
        [pic(c.img, c.name), el('p', { cls: 'back' }, [el('strong', { text: c.name })]), sameText(c.meaning, c.name) ? null : el('p', { text: c.meaning }), c.do ? el('p', { cls: 'small' }, [el('strong', { text: 'Do: ' }), c.do]) : null] :
        [pic(c.img, 'What does this mean?'), el('div', { cls: 'hint', text: 'What does it mean? Tap to check.' })];
    } else {
      face = f.flipped ?
        [el('div', { cls: 'value', text: c.back }), el('p', { cls: 'back', text: c.front }), el('div', { cls: 'hint', text: c.group + ' · ' + c.cat })] :
        [el('div', { cls: 'front', text: c.front }), el('div', { cls: 'hint', text: 'What is the number? Tap to check.' })];
    }
    function flip() { f.flipped = !f.flipped; render(); }
    var card = el('div', { cls: 'card flash', tabindex: '0', role: 'button', 'aria-label': 'Flip card', onclick: flip }, face);
    app.appendChild(card);
    app.appendChild(el('div', { cls: 'btnrow' }, [
      el('button', { cls: 'btn', onclick: function () { f.i = (f.i - 1 + f.cards.length) % f.cards.length; f.flipped = false; render(); } }, ['◀ Back']),
      el('button', { cls: 'btn primary', onclick: flip }, ['Flip']),
      el('button', { cls: 'btn', onclick: function () { f.i = (f.i + 1) % f.cards.length; f.flipped = false; render(); } }, ['Next ▶'])
    ]));
    app.appendChild(el('div', { cls: 'btnrow' }, [
      el('button', { cls: 'btn', onclick: function () { shuffle(f.cards); f.i = 0; f.flipped = false; render(); } }, ['🔀 Shuffle']),
      TTS ? el('button', { cls: 'btn', onclick: function () {
        speak(h === 'signs' ? (f.flipped ? [c.name, c.meaning, c.do] : ['What does this sign mean?']) : (f.flipped ? [c.back, c.front] : [c.front]));
      } }, ['🔊 Read']) : null
    ]));
  }

  function viewSettings() {
    app.appendChild(topbar('Settings', '#/'));
    var sizes = [0.85, 1, 1.15, 1.3, 1.5];
    var rates = [{ v: 0.8, t: 'Slow' }, { v: 1, t: 'Normal' }, { v: 1.2, t: 'Fast' }];
    var card = el('div', { cls: 'card' }, [
      el('h2', { text: 'Text size' }),
      el('div', { cls: 'setrow' }, [
        el('span', { cls: 'label', text: Math.round(store.set.scale * 100) + '%' }),
        el('div', {}, [
          el('button', { cls: 'iconbtn', 'aria-label': 'Smaller text', onclick: function () { setScale(-1); } }, ['A−']),
          el('button', { cls: 'iconbtn', 'aria-label': 'Bigger text', onclick: function () { setScale(1); } }, ['A+'])
        ])
      ]),
      el('h2', { text: 'Read aloud' })
    ]);
    function setScale(d) {
      var i = sizes.indexOf(store.set.scale);
      if (i < 0) i = 1;
      store.set.scale = sizes[Math.max(0, Math.min(sizes.length - 1, i + d))];
      saveStore(); applyScale(); render();
    }
    if (!TTS) {
      card.appendChild(el('p', { cls: 'muted', text: 'This browser has no built-in voice, so read aloud is off. Try Chrome, Edge or Safari.' }));
    } else {
      card.appendChild(el('p', { cls: 'muted small', text: 'The real test computers at DriveTest can read questions to you through headphones. Practising with your ears works the same way.' }));
      var speed = el('div', { cls: 'btnrow' });
      rates.forEach(function (r) {
        speed.appendChild(el('button', { cls: 'btn toggle' + (store.set.rate === r.v ? ' on' : ''), onclick: function () { store.set.rate = r.v; saveStore(); render(); } }, [r.t]));
      });
      card.appendChild(el('p', { text: 'Speed' }));
      card.appendChild(speed);
      card.appendChild(el('button', { cls: 'btn toggle' + (store.set.auto ? ' on' : ''), onclick: function () { store.set.auto = !store.set.auto; saveStore(); render(); } },
        [(store.set.auto ? '✅ ' : '⬜ ') + 'Read every question aloud automatically']));
      card.appendChild(el('button', { cls: 'btn', onclick: function () { speak('This is how questions will sound. You need 16 right in each half.'); } }, ['🔊 Test the voice']));
    }
    app.appendChild(card);
    app.appendChild(el('div', { cls: 'card' }, [
      el('h2', { text: 'Progress' }),
      el('p', { cls: 'muted small', text: NOSAVE ? 'No-save mode: progress is kept only until you close or reload this tab.' : 'Your progress is saved in this browser on this device only. Nothing is sent anywhere.' }),
      el('button', { cls: 'btn', onclick: function () {
        if (window.confirm('Erase all your progress and mock test scores on this device?')) {
          store.p = {}; store.mocks = []; saveStore(); session = null; go('#/');
        }
      } }, ['🗑 Reset my progress'])
    ]));
  }

  // ------------------------------------------------------------ keyboard (laptop)
  var KEYCODES = { 13: 'Enter', 32: ' ', 37: 'ArrowLeft', 39: 'ArrowRight' };
  document.addEventListener('keydown', function (e) {
    if (e.altKey || e.ctrlKey || e.metaKey) return;
    var k = e.key || KEYCODES[e.keyCode] || String.fromCharCode(e.keyCode || 0).toLowerCase();
    var view = location.hash.replace(/^#\/?/, '').split('/')[0];
    if (view === 'quiz' && session && !session.finished) {
      var it = session.items[session.i];
      var idx = k.length === 1 ? '1234'.indexOf(k) : -1;
      if (idx < 0 && k.length === 1) idx = 'abcd'.indexOf(k.toLowerCase());
      if (idx >= 0) { answer(it.order[idx]); e.preventDefault(); return; }
      if ((k === 'Enter' || k === 'ArrowRight') && it.pick !== null) { next(); e.preventDefault(); return; }
      if (k === 'r' || k === 'R') { readQuestion(it); e.preventDefault(); }
    } else if (view === 'flash' && flashState) {
      var f = flashState;
      var onButton = e.target && e.target.tagName === 'BUTTON';
      if ((k === ' ' || k === 'Enter') && !onButton) { f.flipped = !f.flipped; render(); e.preventDefault(); }
      else if (k === 'ArrowRight') { f.i = (f.i + 1) % f.cards.length; f.flipped = false; render(); }
      else if (k === 'ArrowLeft') { f.i = (f.i - 1 + f.cards.length) % f.cards.length; f.flipped = false; render(); }
    }
  });

  applyScale();
  render();
})();
