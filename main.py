import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from database import init_db, list_items, create_item, delete_item, get_db_status


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: SQLite 데이터베이스 및 스키마 초기화
    init_db()
    yield


app = FastAPI(title="banchan Workspace", lifespan=lifespan)


class ItemCreate(BaseModel):
    title: str
    category: str = "general"


@app.get("/api/items")
def api_list_items():
    return {"items": list_items()}


@app.post("/api/items")
def api_create_item(payload: ItemCreate):
    title = payload.title.strip()
    if not title:
        raise HTTPException(status_code=400, detail="항목 내용을 입력해주세요.")
    item = create_item(title=title, category=payload.category)
    return {"item": item}


@app.delete("/api/items/{item_id}")
def api_delete_item(item_id: int):
    success = delete_item(item_id)
    if not success:
        raise HTTPException(status_code=404, detail="항목을 찾을 수 없습니다.")
    return {"success": True}


@app.get("/api/db-status")
def api_db_status():
    return get_db_status()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "database": "sqlite"}


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
    .primary { padding:15px 22px; border-radius:10px; background:var(--ink); color:white; font-weight:800; box-shadow:6px 6px 0 var(--lime); cursor:pointer; border:none; text-decoration:none; display:inline-block; }
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

    /* DB Test Section */
    .db-section { padding:80px 0; border-top:1px solid var(--line); }
    .db-card { background:white; border-radius:24px; border:1.5px solid var(--line); padding:36px; box-shadow:0 12px 36px rgba(11,16,32,.04); }
    .db-header { display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:16px; margin-bottom:28px; }
    .db-title { font-size:28px; font-weight:800; letter-spacing:-.04em; margin:0; }
    .db-badge { display:inline-flex; align-items:center; gap:8px; padding:6px 14px; border-radius:99px; background:#e6fcf5; color:#0ca678; font-size:13px; font-weight:700; border:1px solid #c3fae8; }
    .db-meta { display:flex; gap:20px; font-size:13px; color:#697083; margin-bottom:24px; flex-wrap:wrap; padding:14px 18px; background:#f8f9fa; border-radius:12px; font-family:monospace; }
    .db-form { display:flex; gap:10px; margin-bottom:28px; flex-wrap:wrap; }
    .db-input { flex:1; min-width:240px; padding:14px 18px; border-radius:12px; border:1.5px solid var(--line); font-size:15px; outline:none; transition:border-color .2s; }
    .db-input:focus { border-color:var(--violet); }
    .db-select { padding:14px 16px; border-radius:12px; border:1.5px solid var(--line); font-size:15px; background:white; outline:none; }
    .db-btn { padding:14px 24px; border-radius:12px; background:var(--ink); color:white; font-weight:700; border:none; cursor:pointer; transition:transform .15s; }
    .db-btn:active { transform:scale(.97); }
    .db-list { list-style:none; padding:0; margin:0; display:flex; flex-direction:column; gap:10px; }
    .db-item { display:flex; justify-content:space-between; align-items:center; padding:16px 20px; background:#faf9f4; border-radius:14px; border:1px solid rgba(11,16,32,.06); }
    .db-item-left { display:flex; align-items:center; gap:14px; }
    .db-item-id { font-size:12px; font-weight:800; color:var(--violet); background:rgba(140,124,255,.1); padding:4px 8px; border-radius:6px; }
    .db-item-title { font-size:15px; font-weight:600; color:var(--ink); }
    .db-item-tag { font-size:11px; padding:3px 8px; border-radius:99px; background:#e9ecef; color:#495057; font-weight:600; }
    .db-item-time { font-size:12px; color:#868e96; margin-right:12px; }
    .db-del-btn { padding:6px 12px; border-radius:8px; border:1px solid #ffa39e; background:#fff1f0; color:#cf1322; font-size:12px; font-weight:700; cursor:pointer; }

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
    <div class="links"><a href="#db-test">SQLite Test</a><a href="#features">Features</a><a class="pill" href="#db-test">Live Demo</a></div>
  </nav>
  <main>
    <section class="hero shell">
      <div>
        <div class="eyebrow">The calm workspace</div>
        <h1>Work in<br><span>eight orbit.</span></h1>
        <p class="lead">흩어진 업무와 대화를 하나의 흐름으로. banchan은 팀이 중요한 일에만 집중하도록 프로젝트의 모든 신호를 정리합니다.</p>
        <div class="actions"><a class="primary" href="#db-test">🗄️ SQLite DB 테스트하기</a><a class="secondary" href="#features">기능 둘러보기 →</a></div>
      </div>
      <div class="board" aria-label="banchan product preview">
        <div class="board-head"><div class="dots"><i></i><i></i><i></i></div><div class="version">RELEASE 2.1 (SQLite)</div></div>
        <div class="card"><small>Database Engine</small><h2>SQLite 3 Active</h2><div class="metric"><strong id="metric-count">-</strong><span>live items stored</span></div></div>
        <div class="tasks"><div class="task"><em>PERSISTENCE</em><b>schema.sql loaded</b></div><div class="task"><em>DEPLOYMENT</em><b>On-Premise ready</b></div></div>
      </div>
    </section>

    <!-- LIVE SQLITE DATABASE TEST SECTION -->
    <section class="db-section shell" id="db-test">
      <div class="db-card">
        <div class="db-header">
          <div>
            <h2 class="db-title">🗄️ 온프레미스 SQLite 데이터베이스 테스트</h2>
            <p style="margin:6px 0 0; color:#697083; font-size:14px;">
              컨테이너 내부 SQLite 파일 입출력 및 데이터 보존(Persistence) 동작을 실시간으로 확인합니다.
            </p>
          </div>
          <div class="db-badge">
            <span style="width:8px; height:8px; border-radius:50%; background:#20c997; display:inline-block;"></span>
            SQLite 정상 연결됨
          </div>
        </div>

        <div class="db-meta" id="db-meta-info">
          <span>경로: 로딩 중…</span>
          <span>총 데이터: 로딩 중…</span>
        </div>

        <form class="db-form" id="item-form">
          <input class="db-input" id="item-title" placeholder="테스트할 데이터 내용을 입력하세요 (예: 서버 재기동 영속성 테스트)" required />
          <select class="db-select" id="item-category">
            <option value="infra">infra</option>
            <option value="database">database</option>
            <option value="deployment">deployment</option>
            <option value="test">test</option>
          </select>
          <button type="submit" class="db-btn">+ SQLite에 저장</button>
        </form>

        <ul class="db-list" id="items-container">
          <li style="text-align:center; padding:20px; color:#868e96;">데이터를 불러오는 중…</li>
        </ul>
      </div>
    </section>

    <div class="ticker"><div><span>PLAN WITH CLARITY</span><span>SHIP WITHOUT NOISE</span><span>SQLITE ONPREMISE LIVE</span><span>PLAN WITH CLARITY</span></div></div>

    <section class="features shell" id="features">
      <h2>Everything your team needs. Nothing it doesn’t.</h2>
      <div class="grid">
        <article class="feature"><span class="num">01</span><h3>One clear timeline</h3><p>업데이트와 결정을 한곳에 모아 누구나 지금 상황을 바로 이해합니다.</p></article>
        <article class="feature"><span class="num">02</span><h3>Quiet automation</h3><p>반복 업무는 자동화하고, 팀에게는 필요한 순간에만 정확한 알림을 보냅니다.</p></article>
        <article class="feature"><span class="num">03</span><h3>Progress you can see</h3><p>복잡한 보고서 없이 목표와 진행률을 실시간으로 확인합니다.</p></article>
      </div>
    </section>
  </main>
  <footer class="shell"><span>© 2026 banchan LABS</span><span>On-premise Database Verification.</span></footer>

  <script>
    async function loadDb() {
      try {
        const [statusRes, itemsRes] = await Promise.all([
          fetch('/api/db-status'),
          fetch('/api/items')
        ]);
        const status = await statusRes.json();
        const { items } = await itemsRes.json();

        document.getElementById('metric-count').textContent = status.total_items + ' items';
        document.getElementById('db-meta-info').innerHTML = `
          <span>📂 DB 파일: <strong>${status.db_path}</strong></span>
          <span>📊 레코드 수: <strong>${status.total_items}개</strong> (로그: ${status.total_logs}건)</span>
          <span>💾 파일 크기: <strong>${(status.size_bytes / 1024).toFixed(1)} KB</strong></span>
        `;

        const container = document.getElementById('items-container');
        if (!items || items.length === 0) {
          container.innerHTML = '<li style="text-align:center; padding:20px; color:#868e96;">저장된 데이터가 없습니다.</li>';
          return;
        }

        container.innerHTML = items.map(item => `
          <li class="db-item">
            <div class="db-item-left">
              <span class="db-item-id">#${item.id}</span>
              <span class="db-item-title">${item.title}</span>
              <span class="db-item-tag">${item.category}</span>
            </div>
            <div style="display:flex; align-items:center;">
              <span class="db-item-time">${item.created_at}</span>
              <button class="db-del-btn" onclick="deleteItem(${item.id})">삭제</button>
            </div>
          </li>
        `).join('');
      } catch (err) {
        console.error('DB 불러오기 실패:', err);
      }
    }

    document.getElementById('item-form').addEventListener('submit', async (e) => {
      e.preventDefault();
      const titleInput = document.getElementById('item-title');
      const categoryInput = document.getElementById('item-category');
      const title = titleInput.value.trim();
      if (!title) return;

      try {
        const res = await fetch('/api/items', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ title, category: categoryInput.value })
        });
        if (res.ok) {
          titleInput.value = '';
          loadDb();
        }
      } catch (err) {
        alert('저장에 실패했습니다.');
      }
    });

    async function deleteItem(id) {
      if (!confirm('이 항목을 삭제하시겠습니까?')) return;
      try {
        const res = await fetch('/api/items/' + id, { method: 'DELETE' });
        if (res.ok) loadDb();
      } catch (err) {
        alert('삭제에 실패했습니다.');
      }
    }

    loadDb();
  </script>
</body>
</html>"""
