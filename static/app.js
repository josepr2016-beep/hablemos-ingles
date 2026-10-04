/* Hablemos Inglés — lógica del navegador.
   Voz: usa la síntesis y el reconocimiento de voz que trae el navegador (gratis). */

const $ = (s) => document.querySelector(s);
const app = $('#app');
const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const today = () => {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
};
const shuffle = (a) => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
async function api(url, body, method) {
  const opt = body || method ? { method: method || 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body || {}) } : undefined;
  const r = await fetch(url, opt);
  return r.json();
}

let C = null;      // contenido
let P = null;      // perfil activo
let S = null;      // estado del perfil
let Q = null;      // sesión en curso
let runId = 0;     // cambia al salir de una pantalla, para detener procesos pendientes

/* ---------- Voz: hablar (síntesis) ---------- */
const hasTTS = 'speechSynthesis' in window;
let voice = null;
function pickVoice() {
  const vs = speechSynthesis.getVoices();
  const pref = ['Google US English', 'Microsoft Aria', 'Microsoft Jenny', 'Samantha'];
  voice = pref.map((n) => vs.find((v) => v.name.includes(n))).find(Boolean)
    || vs.find((v) => v.lang === 'en-US') || vs.find((v) => v.lang.startsWith('en')) || null;
}
if (hasTTS) { pickVoice(); speechSynthesis.onvoiceschanged = pickVoice; }
let baseRate = 0.95; // más lento en el nivel Inicial
function say(text, rate = baseRate) {
  return new Promise((res) => {
    if (!hasTTS) return res();
    speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(text);
    u.lang = 'en-US'; u.rate = rate;
    if (voice) u.voice = voice;
    u.onend = res; u.onerror = res;
    speechSynthesis.speak(u);
    setTimeout(res, 10000);
  });
}
const hush = () => { if (hasTTS) speechSynthesis.cancel(); };

/* ---------- Voz: escuchar (reconocimiento) ---------- */
const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
function listen() {
  return new Promise((resolve) => {
    let done = false;
    const end = (v) => { if (!done) { done = true; resolve(v); } };
    let r;
    try {
      r = new SR();
      r.lang = 'en-US'; r.interimResults = false; r.maxAlternatives = 5;
      r.onresult = (e) => end({ alts: Array.from(e.results[0]).map((a) => a.transcript) });
      r.onerror = (e) => end({ alts: [], error: e.error });
      r.onend = () => end({ alts: [] });
      r.start();
    } catch (err) { end({ alts: [], error: 'start' }); }
  });
}
function micMsg(error) {
  if (error === 'not-allowed' || error === 'service-not-allowed') return 'El micrófono está bloqueado. Permítelo en el candado de la barra de direcciones.';
  if (error === 'network') return 'Sin conexión con el servicio de voz. Revisa internet e intenta de nuevo.';
  return 'No te escuché. Acércate al micrófono e intenta otra vez.';
}

/* ---------- Calificación: compara palabra por palabra ---------- */
const CONTR = {
  "i'm": 'i am', "you're": 'you are', "we're": 'we are', "they're": 'they are', "he's": 'he is', "she's": 'she is',
  "it's": 'it is', "that's": 'that is', "what's": 'what is', "where's": 'where is', "who's": 'who is', "how's": 'how is',
  "there's": 'there is', "don't": 'do not', "doesn't": 'does not', "isn't": 'is not', "aren't": 'are not',
  "didn't": 'did not', "haven't": 'have not', "wasn't": 'was not', "won't": 'will not', "couldn't": 'could not', "wouldn't": 'would not',
  "can't": 'can not', cannot: 'can not', "i'll": 'i will', "i'd": 'i would', "let's": 'let us', "i've": 'i have',
};
const NUM = { 0: 'zero', 1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six', 7: 'seven', 8: 'eight', 9: 'nine', 10: 'ten', 40: 'forty' };
function normWord(w) {
  w = w.toLowerCase().replace(/[’`]/g, "'").replace(/[^a-z0-9']/g, '').replace(/^'+|'+$/g, '');
  if (!w) return [];
  if (NUM[w]) w = NUM[w];
  return (CONTR[w] || w).split(' ');
}
function toks(text) {
  const words = text.split(/\s+/).filter(Boolean);
  const out = [];
  words.forEach((w, i) => normWord(w).forEach((t) => out.push({ t, i })));
  return { words, out };
}
function grade(target, alts) {
  const T = toks(target);
  const tt = T.out.map((x) => x.t);
  let best = null;
  for (const a of alts) {
    const H = toks(a).out.map((x) => x.t);
    const n = tt.length, m = H.length;
    const d = Array.from({ length: n + 1 }, () => new Array(m + 1).fill(0));
    for (let i = n - 1; i >= 0; i--) for (let j = m - 1; j >= 0; j--) d[i][j] = tt[i] === H[j] ? d[i + 1][j + 1] + 1 : Math.max(d[i + 1][j], d[i][j + 1]);
    const hit = new Array(n).fill(false);
    let i = 0, j = 0;
    while (i < n && j < m) {
      if (tt[i] === H[j]) { hit[i] = true; i++; j++; } else if (d[i + 1][j] >= d[i][j + 1]) i++; else j++;
    }
    const ok = T.words.map((_, wi) => T.out.every((x, k) => x.i !== wi || hit[k]));
    const score = Math.round((100 * ok.filter(Boolean).length) / ok.length);
    if (!best || score > best.score) best = { score, ok, heard: a };
  }
  return best;
}
const scoreCls = (s) => (s >= 80 ? 'g' : s >= 50 ? 'm' : 'b');
const scoreMsg = (s) => (s === 100 ? '¡Perfecto! Se entendió todo.' : s >= 80 ? '¡Muy bien! Casi todo se entendió.' : s >= 50 ? 'Vas bien. Repite las palabras en rojo.' : 'Escucha la frase lenta y vuelve a intentar.');
const wordsHtml = (text) => text.split(/\s+/).map((w, i) => `<span class="w" data-i="${i}">${esc(w)}</span>`).join(' ');
function wireWords(root) {
  root.querySelectorAll('.w').forEach((el) => { el.onclick = () => say(el.textContent.replace(/[^A-Za-z' ]/g, ''), 0.8); });
}
function paint(root, ok) {
  root.querySelectorAll('.w').forEach((el, i) => { el.classList.remove('ok', 'no'); el.classList.add(ok[i] ? 'ok' : 'no'); });
}

/* ---------- Perfiles ---------- */
const lvl = (id) => C.levels.find((l) => l.id === id) || C.levels[1];
const levelBtns = (sel) => C.levels.map((l) => `<button class="lv ${l.id === sel ? 'sel' : ''}" data-l="${l.id}"><b>${l.emoji} ${l.name}</b><small>${esc(l.desc)}</small></button>`).join('');
const AVATARS = ['🙂', '😎', '🦊', '🐼', '🦁', '🐸', '🦄', '🚀', '⚽', '🌟'];
async function loadProfiles() {
  runId++; hush(); P = null;
  try { localStorage.removeItem('hi_profile'); } catch (e) { /* sin almacenamiento */ }
  const list = await api(`/api/profiles?day=${today()}`);
  app.innerHTML = `
    <div class="hero"><h1>Hablemos Inglés</h1><p>Escucha, repite y conversa. Diez minutos al día.</p></div>
    <h3>¿Quién va a practicar?</h3>
    <div class="plist">
      ${list.map((p) => `<button class="pcard" data-id="${p.id}"><span class="av">${esc(p.avatar)}</span><b>${esc(p.name)}</b><small>${lvl(p.level).emoji} ${lvl(p.level).name} · 🔥 ${p.streak}</small></button>`).join('')}
      <button class="pcard add" id="add"><span class="av">＋</span><b>Nuevo perfil</b></button>
    </div>
    <div id="form"></div>`;
  app.querySelectorAll('.pcard[data-id]').forEach((b) => { b.onclick = () => openProfile(list.find((p) => p.id === Number(b.dataset.id))); });
  $('#add').onclick = () => {
    let av = AVATARS[0]; let level = 2;
    $('#form').innerHTML = `<div class="card" style="margin-top:12px"><b>Nuevo perfil</b>
      <input type="text" id="nm" maxlength="40" placeholder="Nombre">
      <div class="row avs" style="justify-content:flex-start">${AVATARS.map((a, i) => `<button data-a="${a}" class="${i ? '' : 'sel'}">${a}</button>`).join('')}</div>
      <p class="lbl">¿Desde qué nivel quiere empezar?</p><div class="lvs">${levelBtns(level)}</div>
      <button class="btn primary" id="save">Crear perfil</button></div>`;
    app.querySelectorAll('.lv').forEach((b) => { b.onclick = () => { level = Number(b.dataset.l); app.querySelectorAll('.lv').forEach((x) => x.classList.toggle('sel', x === b)); }; });
    app.querySelectorAll('.avs button').forEach((b) => { b.onclick = () => { av = b.dataset.a; app.querySelectorAll('.avs button').forEach((x) => x.classList.toggle('sel', x === b)); }; });
    $('#nm').focus();
    $('#save').onclick = async () => {
      const name = $('#nm').value.trim();
      if (!name) { $('#nm').focus(); return; }
      const p = await api(`/api/profiles?day=${today()}`, { name, avatar: av, level });
      if (p.id) openProfile(p);
    };
  };
}
function openProfile(p) {
  P = p;
  try { localStorage.setItem('hi_profile', String(p.id)); } catch (e) { /* sin almacenamiento */ }
  loadHome();
}

/* ---------- Inicio del perfil ---------- */
async function loadHome() {
  runId++; hush(); Q = null;
  S = await api(`/api/profiles/${P.id}/state?day=${today()}`);
  const box = (id) => (S.progress[id] ? S.progress[id].box : 0);
  P.level = S.level; baseRate = S.level === 1 ? 0.8 : 0.95;
  const units = C.units.filter((u) => u.level === S.level);
  app.innerHTML = `
    <header class="hd"><button class="link" id="sw">${esc(P.avatar)} ${esc(P.name)} ▾</button>
      <div class="stats"><span title="Días seguidos">🔥 ${S.streak}</span><span title="Puntos">⭐ ${S.total_points}</span></div></header>
    ${SR ? '' : '<div class="warn">Este navegador no puede escucharte, así que no calificará tu pronunciación. Usa Chrome o Edge (computador y Android) o Safari (iPhone). Los ejercicios de escucha sí funcionan.</div>'}
    <button class="daily" id="daily"><b>▶ Práctica de hoy</b><small>${S.due_count ? `${S.due_count} frases para repasar y algunas nuevas` : 'Frases nuevas para escuchar y repetir'} · ${S.today_points} puntos hoy</small></button>
    <h3>Nivel</h3><div class="lvs row3">${C.levels.map((l) => `<button class="lv ${l.id === S.level ? 'sel' : ''}" data-l="${l.id}"><b>${l.emoji} ${l.name}</b></button>`).join('')}</div>
    <p class="hint" style="text-align:left">${esc(lvl(S.level).desc)} Puedes cambiarlo cuando quieras; el progreso de cada nivel se conserva.</p>
    <h3>Temas</h3>
    ${units.map((u) => {
      const done = u.phrases.filter((p) => box(p.id) >= 1).length;
      const solid = u.phrases.filter((p) => box(p.id) >= 3).length;
      return `<div class="card unit"><div class="uh"><span class="emo">${u.emoji}</span><div><b>${esc(u.title)}</b>
        <small>${done}/${u.phrases.length} practicadas · ${solid} dominadas</small><div class="meter"><i style="width:${(100 * done) / u.phrases.length}%"></i></div></div></div>
        <div class="row"><button class="btn" data-u="${u.id}" data-m="speak">🎤 Hablar</button><button class="btn" data-u="${u.id}" data-m="listen">🎧 Escuchar</button><button class="btn" data-u="${u.id}" data-m="dialog">💬 Conversar</button></div></div>`;
    }).join('')}
    <div class="card unit"><div class="uh"><span class="emo">👂</span><div><b>Sonidos difíciles</b><small>ship / sheep, three / tree, very / berry…</small></div></div>
      <div class="row"><button class="btn" id="pairs">Entrenar el oído</button></div></div>
    <p class="hint"><button class="link danger" id="del">Eliminar este perfil</button></p>`;
  $('#sw').onclick = loadProfiles;
  app.querySelectorAll('.lv').forEach((b) => { b.onclick = async () => { await api(`/api/profiles/${P.id}/level`, { level: Number(b.dataset.l) }); loadHome(); }; });
  $('#daily').onclick = startDaily;
  $('#pairs').onclick = () => startSession(shuffle(C.pairs).slice(0, 8).map((p) => ({ type: 'pair', item: p })));
  app.querySelectorAll('[data-u]').forEach((b) => {
    b.onclick = () => {
      const u = C.units.find((x) => x.id === b.dataset.u);
      if (b.dataset.m === 'dialog') return renderDialog(u);
      const items = b.dataset.m === 'listen' ? shuffle(u.phrases) : u.phrases;
      startSession(items.map((p) => ({ type: b.dataset.m, item: p })));
    };
  });
  $('#del').onclick = async (e) => {
    if (e.target.dataset.sure) { await api(`/api/profiles/${P.id}`, null, 'DELETE'); loadProfiles(); return; }
    e.target.dataset.sure = '1'; e.target.textContent = 'Toca otra vez para confirmar: se borra todo el progreso';
  };
}
async function startDaily() {
  const ids = await api(`/api/profiles/${P.id}/daily?day=${today()}`);
  const steps = ids.map((id, i) => ({ type: i % 3 === 0 ? 'listen' : 'speak', item: C.items[id] })).filter((s) => s.item);
  if (!steps.length) return;
  startSession(steps);
}

/* ---------- Motor de sesión ---------- */
function startSession(steps) { runId++; Q = { steps, i: 0, scores: [] }; renderStep(); }
function renderStep() {
  if (Q.i >= Q.steps.length) return renderSummary();
  const st = Q.steps[Q.i];
  ({ speak: renderSpeak, listen: renderListen, pair: renderPair })[st.type](st.item);
}
function shell(inner, pct, label) {
  app.innerHTML = `<div class="top"><button class="link" id="quit" aria-label="Salir">✕</button><div class="bar"><i style="width:${pct}%"></i></div><span>${label}</span></div><div class="card ex">${inner}</div>`;
  $('#quit').onclick = loadHome;
}
const qShell = (inner) => shell(inner, Math.round((100 * Q.i) / Q.steps.length), `${Q.i + 1}/${Q.steps.length}`);
async function finishStep(itemId, score) {
  hush();
  if (score !== null) {
    Q.scores.push(score);
    await api(`/api/profiles/${P.id}/result`, { item_id: itemId, score, day: today() });
  }
  Q.i++; renderStep();
}

/* ---------- Ejercicio: escucha y repite ---------- */
function renderSpeak(it) {
  let best = null;
  qShell(`<p class="tag">🎤 Escucha y repite</p>
    <div class="en" id="en">${wordsHtml(it.en)}</div><p class="es">${esc(it.es)}</p>
    <div class="row"><button class="btn" id="play">🔊 Escuchar</button><button class="btn" id="slow">🐢 Lento</button></div>
    <button class="mic" id="mic" aria-label="Hablar" ${SR ? '' : 'disabled'}>🎤</button>
    <p class="hint" id="hint">${SR ? 'Toca el micrófono y di la frase. Toca una palabra para oírla sola.' : 'Escucha y repite en voz alta. Este navegador no puede calificarte.'}</p>
    <div id="fb"></div><button class="btn primary" id="next">${SR ? 'Saltar' : 'Siguiente'} →</button>`);
  wireWords($('#en'));
  $('#play').onclick = () => say(it.en);
  $('#slow').onclick = () => say(it.en, 0.6);
  $('#next').onclick = () => finishStep(it.id, best);
  $('#mic').onclick = async () => {
    const my = runId; const mic = $('#mic');
    if (mic.classList.contains('on')) return;
    hush(); mic.classList.add('on'); $('#hint').textContent = 'Escuchando… habla ahora';
    const r = await listen();
    if (my !== runId || !$('#mic')) return;
    mic.classList.remove('on');
    if (!r.alts.length) { $('#hint').textContent = micMsg(r.error); return; }
    const g = grade(it.en, r.alts);
    paint($('#en'), g.ok);
    best = Math.max(best === null ? 0 : best, g.score);
    $('#hint').textContent = 'Toca el micrófono para intentar otra vez';
    $('#fb').innerHTML = `<p class="score ${scoreCls(g.score)}">${g.score}%</p><p class="hint">Entendí: “${esc(g.heard)}”</p><p>${scoreMsg(g.score)}</p>`;
    $('#next').textContent = 'Siguiente →';
  };
  say(it.en);
}

/* ---------- Ejercicio: escucha y arma la frase ---------- */
function renderListen(it) {
  const clean = (w) => w.replace(/[.,!?]/g, '');
  const words = it.en.split(/\s+/).map(clean);
  const lower = words.map((w) => w.toLowerCase());
  const pool = shuffle(Object.values(C.items).flatMap((x) => x.en.split(/\s+/).map(clean))).filter((w) => !lower.includes(w.toLowerCase()));
  const tiles = shuffle(words.concat([...new Set(pool)].slice(0, 2)));
  let picked = []; let tries = 0; let score = null;
  qShell(`<p class="tag">🎧 Escucha y arma la frase</p>
    <div class="row"><button class="btn" id="play">🔊 Escuchar</button><button class="btn" id="slow">🐢 Lento</button></div>
    <div class="ans" id="ans"></div><div class="bank" id="bank"></div><div id="fb"></div>
    <button class="btn primary" id="check">Comprobar</button>`);
  $('#play').onclick = () => say(it.en);
  $('#slow').onclick = () => say(it.en, 0.6);
  const draw = () => {
    $('#ans').innerHTML = picked.map((k) => `<button class="tile" data-k="${k}">${esc(tiles[k])}</button>`).join('');
    $('#bank').innerHTML = tiles.map((w, k) => (picked.includes(k) ? '' : `<button class="tile" data-k="${k}">${esc(w)}</button>`)).join('');
    if (score !== null) return;
    $('#ans').querySelectorAll('.tile').forEach((b) => { b.onclick = () => { picked = picked.filter((k) => k !== Number(b.dataset.k)); draw(); }; });
    $('#bank').querySelectorAll('.tile').forEach((b) => { b.onclick = () => { picked.push(Number(b.dataset.k)); draw(); }; });
  };
  draw();
  $('#check').onclick = () => {
    if (score !== null) return finishStep(it.id, score);
    if (!picked.length) return;
    const right = picked.map((k) => tiles[k].toLowerCase()).join(' ') === lower.join(' ');
    if (!right && tries === 0) {
      tries = 1; $('#fb').innerHTML = '<div class="fb no">Casi. Escúchala otra vez, más lento, y corrige.</div>'; say(it.en, 0.6); return;
    }
    score = right ? (tries ? 70 : 100) : 30;
    $('#fb').innerHTML = `<div class="fb ${right ? 'ok' : 'no'}">${right ? '¡Correcto!' : 'La frase era:'}<b>${esc(it.en)}</b>${esc(it.es)}</div>`;
    $('#check').textContent = 'Siguiente →';
    draw();
  };
  say(it.en);
}

/* ---------- Ejercicio: sonidos difíciles ---------- */
function renderPair(p) {
  const target = Math.random() < 0.5 ? p.a : p.b;
  let score = null;
  qShell(`<p class="tag">👂 Sonidos difíciles</p><p>¿Cuál palabra escuchas?</p>
    <div class="row"><button class="btn" id="play">🔊 Escuchar otra vez</button></div>
    <div class="row" style="margin-top:18px"><button class="btn choice" data-w="${p.a}">${p.a}</button><button class="btn choice" data-w="${p.b}">${p.b}</button></div>
    <div id="fb"></div><button class="btn primary" id="next" style="display:none">Siguiente →</button>`);
  $('#play').onclick = () => say(target, 0.8);
  $('#next').onclick = () => finishStep(p.id, score);
  app.querySelectorAll('.choice').forEach((b) => {
    b.onclick = () => {
      if (score === null) {
        const right = b.dataset.w === target;
        score = right ? 100 : 0;
        $('#fb').innerHTML = `<div class="fb ${right ? 'ok' : 'no'}">${right ? '¡Correcto!' : 'Era:'}<b>${target}</b>${esc(p.tip)}<br>Toca cada palabra para comparar cómo suenan.</div>`;
        $('#next').style.display = '';
      }
      say(b.dataset.w, 0.8);
    };
  });
  say(target, 0.8);
}

/* ---------- Conversación guiada ---------- */
function renderDialog(u) {
  const my = ++runId; hush();
  const L = u.dialogue.lines; const scores = []; let k = 0;
  const mine = L.filter((l) => l[0] === 'B').length;
  shell(`<p class="tag">💬 Conversación: ${esc(u.title)}</p><div class="chat" id="chat"></div><div id="ctl"></div>`, 0, `0/${mine}`);
  const alive = () => my === runId && $('#chat');
  async function step() {
    if (!alive()) return;
    if (k >= L.length) {
      const avg = scores.length ? Math.round(scores.reduce((a, b) => a + b, 0) / scores.length) : null;
      if (avg !== null) await api(`/api/profiles/${P.id}/result`, { item_id: u.dialogue.id, score: avg, day: today() });
      Q = { steps: [], i: 0, scores: avg === null ? [] : [avg] };
      return renderSummary();
    }
    const [who, en, es] = L[k];
    const bub = document.createElement('div');
    bub.className = `bub ${who === 'B' ? 'me' : ''}`;
    bub.innerHTML = `<div class="ln">${wordsHtml(en)}</div><small>${esc(es)}</small>`;
    $('#chat').appendChild(bub); wireWords(bub);
    bub.scrollIntoView({ block: 'nearest' });
    if (who === 'A') {
      $('#ctl').innerHTML = '';
      await say(en);
      k++; return step();
    }
    let got = null;
    $('#ctl').innerHTML = `<button class="mic" id="mic" ${SR ? '' : 'disabled'}>🎤</button><p class="hint" id="hint">${SR ? 'Te toca: di tu línea' : 'Di tu línea en voz alta'}</p>
      <div class="row"><button class="btn" id="hear">🔊 Oír mi línea</button><button class="btn" id="go">Continuar →</button></div>`;
    $('#hear').onclick = () => say(en, 0.8);
    $('#go').onclick = () => { if (got !== null) scores.push(got); k++; $('.top .bar i').style.width = `${(100 * scores.length) / mine}%`; $('.top span').textContent = `${scores.length}/${mine}`; step(); };
    $('#mic').onclick = async () => {
      const mic = $('#mic');
      if (mic.classList.contains('on')) return;
      hush(); mic.classList.add('on'); $('#hint').textContent = 'Escuchando… habla ahora';
      const r = await listen();
      if (!alive() || !$('#mic')) return;
      mic.classList.remove('on');
      if (!r.alts.length) { $('#hint').textContent = micMsg(r.error); return; }
      const g = grade(en, r.alts);
      paint(bub, g.ok); got = Math.max(got || 0, g.score);
      $('#hint').textContent = `${g.score}% · ${scoreMsg(g.score)}`;
    };
  }
  step();
}

/* ---------- Resumen ---------- */
async function renderSummary() {
  hush();
  const sc = Q.scores;
  const avg = sc.length ? Math.round(sc.reduce((a, b) => a + b, 0) / sc.length) : null;
  const st = await api(`/api/profiles/${P.id}/state?day=${today()}`);
  app.innerHTML = `<div class="card ex"><div style="font-size:60px">🎉</div><h2>¡Buen trabajo, ${esc(P.name)}!</h2>
    ${avg === null ? '' : `<p class="score ${scoreCls(avg)}">${avg}%</p><p class="hint">Promedio de la sesión</p>`}
    <p>🔥 Racha: ${st.streak} ${st.streak === 1 ? 'día' : 'días'} · ⭐ ${st.today_points} puntos hoy</p>
    <button class="btn primary" id="home">Continuar</button></div>`;
  $('#home').onclick = loadHome;
}

/* ---------- Arranque ---------- */
(async function init() {
  C = await api('/api/content');
  C.items = {};
  C.units.forEach((u) => u.phrases.forEach((p) => { C.items[p.id] = p; }));
  let saved = null;
  try { saved = Number(localStorage.getItem('hi_profile')); } catch (e) { /* sin almacenamiento */ }
  if (saved) {
    const list = await api(`/api/profiles?day=${today()}`);
    const p = list.find((x) => x.id === saved);
    if (p) return openProfile(p);
  }
  loadProfiles();
})();
