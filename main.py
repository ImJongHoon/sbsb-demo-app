from fastapi import FastAPI
from fastapi.responses import HTMLResponse


app = FastAPI(title="banchan Workspace")


@app.get("/", response_class=HTMLResponse)
def read_root() -> str:
    return """<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="theme-color" content="#0b1020" />
  <title>banchan — Work in one orbit</title>
  <style>
    :root { --ink:#0b1020; --paper:#f6f4ee; --lime:#c7ff4a; --violet:#8c7cff; --line:rgba(11,16,32,.14); }
    * { box-sizing:border-box; }
    html { scroll-behavior:smooth; }
    body { margin:0; color:var(--ink); background:var(--paper); font-family:Inter,ui-sans-serif,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; }
    a { color:inherit; text-decoration:none; }
    .shell { width:min(1180px,calc(100% - 40px)); margin:auto; }
    nav { height:78px; display:flex; align-items:center; justify-content:space-between; border-bottom:1px solid var(--line); }
    .logo { font-weight:900; letter-spacing:-.06em; font-size:24px; }
    .logo i { display:inline-block; width:11px; height:11px; margin-left:3px; border-radius:50%; background:var(--lime); }
    .links { display:flex; gap:30px; align-items:center; font-size:14px; font-weight:650; }
    .pill { border:1px solid var(--ink); border-radius:999px; padding:11px 17px; }
    .hero { padding:84px 0 62px; display:grid; grid-template-columns:1.05fr .95fr; gap:70px; align-items:center; }
    .eyebrow { display:flex; align-items:center; gap:9px; font-size:12px; font-weight:800; letter-spacing:.12em; text-transform:uppercase; }
    .eyebrow:before { content:""; width:28px; height:3px; background:var(--violet); }
    h1 { margin:24px 0; max-width:720px; font-size:clamp(58px,7.4vw,104px); line-height:.88; letter-spacing:-.075em; }
    h1 span { display:block; color:var(--violet); }
    .lead { max-width:590px; margin:0 0 34px; color:#4d5364; font-size:18px; line-height:1.65; }
    .actions { display:flex; gap:12px; align-items:center; }
    .primary { padding:15px 22px; border-radius:10px; background:var(--ink); color:white; font-weight:800; box-shadow:6px 6px 0 var(--lime); }
    .secondary { padding:15px 18px; font-weight:750; }
    .board { position:relative; min-height:480px; padding:20px; border-radius:28px; background:var(--ink); color:white; box-shadow:20px 20px 0 var(--violet); overflow:hidden; }
    .board:after { content:""; position:absolute; width:260px; height:260px; right:-80px; top:-90px; border-radius:50%; background:var(--lime); filter:blur(2px); opacity:.92; }
    .board-head { position:relative; z-index:1; display:flex; justify-content:space-between; align-items:center; padding:6px 4px 20px; }
    .dots { display:flex; gap:6px; } .dots i { width:8px; height:8px; border-radius:50%; background:#697083; }
    .version { padding:7px 10px; border:1px solid rgba(255,255,255,.28); border-radius:99px; font-size:11px; letter-spacing:.08em; }
    .card { position:relative; z-index:1; padding:22px; border:1px solid rgba(255,255,255,.15); border-radius:18px; background:rgba(255,255,255,.08); backdrop-filter:blur(12px); }
    .card small { color:#aab0c0; text-transform:uppercase; letter-spacing:.11em; }
    .card h2 { margin:9px 0 24px; font-size:32px; letter-spacing:-.04em; }
    .metric { display:flex; align-items:end; justify-content:space-between; margin-top:14px; padding-top:17px; border-top:1px solid rgba(255,255,255,.12); }
    .metric strong { font-size:42px; letter-spacing:-.06em; } .metric span { color:var(--lime); font-size:13px; }
    .tasks { position:relative; z-index:1; display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-top:12px; }
    .task { min-height:108px; padding:16px; border-radius:15px; background:#faf9f4; color:var(--ink); }
    .task b { display:block; margin-top:25px; font-size:15px; } .task em { font-style:normal; color:#74798a; font-size:12px; }
    .ticker { border-top:1px solid var(--line); border-bottom:1px solid var(--line); overflow:hidden; }
    .ticker div { display:flex; width:max-content; gap:48px; padding:19px 0; font-size:14px; font-weight:850; letter-spacing:.04em; }
    .ticker span:before { content:"✦"; margin-right:48px; color:var(--violet); }
    .features { padding:95px 0; }
    .features h2 { max-width:730px; margin:0 0 50px; font-size:clamp(42px,6vw,72px); line-height:.98; letter-spacing:-.065em; }
    .grid { display:grid; grid-template-columns:repeat(3,1fr); border-top:1px solid var(--ink); }
    .feature { padding:30px 28px 30px 0; border-bottom:1px solid var(--line); }
    .feature + .feature { padding-left:28px; border-left:1px solid var(--line); }
    .feature .num { color:var(--violet); font-size:12px; font-weight:900; }
    .feature h3 { margin:48px 0 12px; font-size:24px; letter-spacing:-.04em; }
    .feature p { margin:0; color:#656b79; line-height:1.6; }
    footer { display:flex; justify-content:space-between; padding:30px 0 45px; border-top:1px solid var(--line); color:#686e7d; font-size:13px; }
    @media (max-width:850px) { .links a:not(.pill){display:none}.hero{grid-template-columns:1fr;padding-top:55px}.board{min-height:430px}.grid{grid-template-columns:1fr}.feature+.feature{padding-left:0;border-left:0}.tasks{grid-template-columns:1fr 1fr} }
  </style>
</head>
<body>
  <nav class="shell">
    <a class="logo" href="#">banchan<i></i></a>
    <div class="links"><a href="#features">Features</a><a href="#about">About</a><a class="pill" href="#start">Start free</a></div>
  </nav>
  <main>
    <section class="hero shell">
      <div>
        <div class="eyebrow">The calm workspace</div>
        <h1>Work in<br><span>three orbit.</span></h1>
        <p class="lead">흩어진 업무와 대화를 하나의 흐름으로. banchan은 팀이 중요한 일에만 집중하도록 프로젝트의 모든 신호를 정리합니다.</p>
        <div class="actions"><a class="primary" id="start" href="#features">무료로 시작하기</a><a class="secondary" href="#features">둘러보기 →</a></div>
      </div>
      <div class="board" aria-label="banchan product preview">
        <div class="board-head"><div class="dots"><i></i><i></i><i></i></div><div class="version">RELEASE 2.0</div></div>
        <div class="card"><small>Weekly momentum</small><h2>Design system sprint</h2><div class="metric"><strong>84%</strong><span>↑ 12% this week</span></div></div>
        <div class="tasks"><div class="task"><em>IN REVIEW</em><b>Mobile navigation</b></div><div class="task"><em>NEXT UP</em><b>Launch checklist</b></div></div>
      </div>
    </section>
    <div class="ticker"><div><span>PLAN WITH CLARITY</span><span>SHIP WITHOUT NOISE</span><span>MOVE AS ONE TEAM</span><span>PLAN WITH CLARITY</span></div></div>
    <section class="features shell" id="features">
      <h2>Everything your team needs. Nothing it doesn’t.</h2>
      <div class="grid">
        <article class="feature"><span class="num">01</span><h3>One clear timeline</h3><p>업데이트와 결정을 한곳에 모아 누구나 지금 상황을 바로 이해합니다.</p></article>
        <article class="feature"><span class="num">02</span><h3>Quiet automation</h3><p>반복 업무는 자동화하고, 팀에게는 필요한 순간에만 정확한 알림을 보냅니다.</p></article>
        <article class="feature"><span class="num">03</span><h3>Progress you can see</h3><p>복잡한 보고서 없이 목표와 진행률을 실시간으로 확인합니다.</p></article>
      </div>
    </section>
  </main>
  <footer class="shell" id="about"><span>© 2026 banchan LABS</span><span>Built for focused teams.</span></footer>
</body>
</html>"""


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
