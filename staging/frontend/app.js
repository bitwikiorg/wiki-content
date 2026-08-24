const app = document.querySelector('#app');
const statusBar = document.querySelector('#statusBar');
const namespaceList = document.querySelector('#namespaceList');
const searchInput = document.querySelector('#searchInput');
const searchButton = document.querySelector('#searchButton');

const state = {
  pages: [],
  pageById: new Map(),
  graph: { nodes: [], edges: [] },
  nodeById: new Map(),
  ontology: { schema: {}, objects: [] },
  meta: {},
};

function esc(value) {
  return String(value ?? '')
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');
}

function arrayTags(values = []) {
  if (!values.length) return '<span class="muted">None</span>';
  return `<div class="tag-list">${values.map(v => `<span class="tag">${esc(v)}</span>`).join('')}</div>`;
}

function repoFileUrl(path) {
  const encoded = path.split('/').map(encodeURIComponent).join('/');
  return `https://github.com/bitwikiorg/wiki-content/blob/main/${encoded}`;
}

function parseRoute() {
  const raw = location.hash.slice(1) || '/';
  const [path, query = ''] = raw.split('?', 2);
  return { path, params: new URLSearchParams(query) };
}

function setRoute(path, params = {}) {
  const query = new URLSearchParams(params).toString();
  location.hash = query ? `${path}?${query}` : path;
}

async function loadJSON(path) {
  const response = await fetch(path, { cache: 'no-cache' });
  if (!response.ok) throw new Error(`${path}: ${response.status}`);
  return response.json();
}

async function initialize() {
  try {
    const [pages, graph, ontology, meta] = await Promise.all([
      loadJSON('./data/pages.json'),
      loadJSON('./data/graph.json'),
      loadJSON('./data/ontology.json'),
      loadJSON('./data/build-meta.json'),
    ]);
    state.pages = pages;
    state.pageById = new Map(pages.map(page => [page.id, page]));
    state.graph = graph;
    state.nodeById = new Map(graph.nodes.map(node => [node.id, node]));
    state.ontology = ontology;
    state.meta = meta;
    renderNamespaces();
    statusBar.textContent = `${meta.page_count} source objects · ${meta.ontology_object_count} knowledge objects · ${meta.graph_edge_count} graph edges · ${meta.source_sha.slice(0, 12)}`;
    route();
  } catch (error) {
    statusBar.textContent = 'Staging build failed to load.';
    app.innerHTML = `<div class="empty"><strong>Unable to load staging artifacts.</strong><br>${esc(error.message)}</div>`;
  }
}

function renderNamespaces() {
  const counts = new Map();
  for (const page of state.pages) counts.set(page.namespace, (counts.get(page.namespace) || 0) + 1);
  namespaceList.innerHTML = [...counts.entries()]
    .sort((a, b) => a[0].localeCompare(b[0]))
    .map(([name, count]) => `<a href="#/search?namespace=${encodeURIComponent(name)}">${esc(name)} <span class="muted">(${count})</span></a>`)
    .join('');
}

function renderHome(filter = {}) {
  const q = (filter.q || '').trim().toLocaleLowerCase();
  const namespace = filter.namespace || '';
  const pages = state.pages
    .filter(page => !namespace || page.namespace === namespace)
    .filter(page => !q || [page.title, page.namespace, page.entity_type, page.domain, page.source_path].some(v => String(v || '').toLocaleLowerCase().includes(q)))
    .sort((a, b) => a.title.localeCompare(b.title));

  const heading = q ? `Search: ${filter.q}` : namespace ? `Namespace: ${namespace}` : 'BITwiki staging workbench';
  app.innerHTML = `
    <section class="home-intro">
      <h1>${esc(heading)}</h1>
      <p><strong>Inspectable micro-staging for BITwiki/MediaWiki.</strong> This projection asks what repository knowledge will become when promoted, what it connects to, and how it can be displayed without changing the deployable source.</p>
      <div class="metric-row">
        <div class="metric"><strong>${state.meta.page_count}</strong><span>source objects</span></div>
        <div class="metric"><strong>${state.meta.ontology_object_count}</strong><span>typed knowledge objects</span></div>
        <div class="metric"><strong>${state.meta.graph_node_count}</strong><span>graph nodes</span></div>
        <div class="metric"><strong>${state.meta.graph_edge_count}</strong><span>derived edges</span></div>
      </div>
    </section>
    <div class="source-toolbar"><span>${pages.length} matching objects</span><span>Generated from repository source; no staging metadata is written back.</span></div>
    <div class="page-list">
      ${pages.slice(0, 250).map(page => `
        <div class="page-row">
          <a href="#/page/${page.id}">${esc(page.title)}</a>
          <span class="muted">${esc(page.namespace)}</span>
          <span class="muted">${esc(page.entity_type || page.content_model)}</span>
          <span class="${page.validation_status === 'pass' ? 'validation-pass' : 'validation-error'}">${esc(page.validation_status)}</span>
        </div>
      `).join('') || '<div class="empty">No staged source objects match this query.</div>'}
    </div>
  `;
}

function pageTabs(page, active) {
  const tabs = ['read', 'source', 'structure', 'graph', 'promote'];
  return `
    <div class="tabs" role="tablist">
      ${tabs.map(tab => `<button class="${tab === active ? 'active' : ''}" data-view="${tab}">${tab[0].toUpperCase() + tab.slice(1)}</button>`).join('')}
    </div>
  `;
}

function identityCard(page) {
  const identity = page.parsed.identity || {};
  return `
    <aside class="inspector-card">
      <h2>${esc(page.title)}</h2>
      <dl class="inspector-grid">
        <dt>Entity type</dt><dd>${esc(identity.entity_type || 'Not specified')}</dd>
        <dt>Domain</dt><dd>${esc(identity.domain || 'Not specified')}</dd>
        <dt>Epistemic</dt><dd>${esc(identity.status || 'Not specified')}</dd>
        <dt>Provenance</dt><dd>${esc(identity.provenance || 'Not specified')}</dd>
        <dt>Namespace</dt><dd>${esc(page.namespace)}</dd>
        <dt>Validation</dt><dd class="${page.validation.status === 'pass' ? 'validation-pass' : 'validation-error'}">${esc(page.validation.status)}</dd>
      </dl>
    </aside>
  `;
}

function renderRead(page) {
  return `
    <div class="read-layout">
      <article class="article-body">${page.preview_html}</article>
      ${identityCard(page)}
    </div>
  `;
}

function renderSource(page) {
  return `
    <div class="source-toolbar">
      <span>${esc(page.source_path)} · ${esc(page.content_model)}</span>
      <a href="${repoFileUrl(page.source_path)}" target="_blank" rel="noreferrer">Open exact source on GitHub ↗</a>
    </div>
    <pre class="source-code"><code>${esc(page.source)}</code></pre>
  `;
}

function renderStructure(page) {
  const parsed = page.parsed;
  const identity = parsed.identity || {};
  const semanticRelations = parsed.semantic.filter(item => item.is_relationship === 'true');
  return `
    <div class="panel-grid">
      <section class="panel">
        <h3>Identity</h3>
        <dl>
          <dt>Entity type</dt><dd>${esc(identity.entity_type || '—')}</dd>
          <dt>Domain</dt><dd>${esc(identity.domain || '—')}</dd>
          <dt>Status</dt><dd>${esc(identity.status || '—')}</dd>
          <dt>Provenance</dt><dd>${esc(identity.provenance || '—')}</dd>
          <dt>Content model</dt><dd>${esc(page.content_model)}</dd>
          <dt>Projection</dt><dd>${esc(page.projection_kind)}</dd>
        </dl>
      </section>
      <section class="panel">
        <h3>Document anatomy</h3>
        ${parsed.headings.length ? `<ol>${parsed.headings.map(h => `<li>${esc(h.title)} <span class="muted">H${h.level}</span></li>`).join('')}</ol>` : '<span class="muted">No wikitext headings extracted.</span>'}
      </section>
      <section class="panel">
        <h3>Classification</h3>
        <p><strong>Categories</strong></p>${arrayTags(parsed.categories)}
        <p><strong>Properties used</strong></p>${arrayTags(parsed.properties)}
      </section>
      <section class="panel">
        <h3>Runtime dependencies</h3>
        <p><strong>Templates</strong></p>${arrayTags(parsed.templates)}
        <p><strong>Lua modules</strong></p>${arrayTags(parsed.modules)}
      </section>
      <section class="panel">
        <h3>Semantic relations</h3>
        ${semanticRelations.length ? `<ul>${semanticRelations.map(item => `<li><strong>${esc(item.property)}</strong> → ${esc(item.target)}</li>`).join('')}</ul>` : '<span class="muted">No controlled semantic relationship assertions extracted.</span>'}
      </section>
      <section class="panel">
        <h3>Structural links</h3>
        <p>${parsed.wikilinks.length} ordinary wiki links</p>
        ${arrayTags(parsed.wikilinks.slice(0, 40))}
      </section>
    </div>
  `;
}

function neighborsFor(pageId, layer = 'all') {
  return state.graph.edges.filter(edge => {
    const adjacent = edge.source === pageId || edge.target === pageId;
    return adjacent && (layer === 'all' || edge.layer === layer);
  });
}

function graphNodeLabel(id, fallback = '') {
  return state.nodeById.get(id)?.title || fallback || 'Unresolved';
}

function renderGraphSvg(centerId, layer = 'all') {
  const edges = neighborsFor(centerId, layer).slice(0, 48);
  const center = state.nodeById.get(centerId);
  if (!center) return '<div class="empty">This object is not in the graph projection.</div>';
  if (!edges.length) return '<div class="empty">No graph edges for the selected layer.</div>';

  const width = 900;
  const height = 540;
  const cx = width / 2;
  const cy = height / 2;
  const radius = Math.min(width, height) * 0.36;
  const neighborKeys = [];
  const neighborMap = new Map();

  edges.forEach((edge, index) => {
    const otherId = edge.source === centerId ? edge.target : edge.source;
    const key = otherId || `ghost-${index}`;
    if (!neighborMap.has(key)) {
      neighborKeys.push(key);
      neighborMap.set(key, {
        id: otherId,
        title: otherId ? graphNodeLabel(otherId) : edge.target_title,
      });
    }
  });

  const positions = new Map([[centerId, { x: cx, y: cy }]]);
  neighborKeys.forEach((key, index) => {
    const angle = (Math.PI * 2 * index / neighborKeys.length) - Math.PI / 2;
    positions.set(key, { x: cx + Math.cos(angle) * radius, y: cy + Math.sin(angle) * radius });
  });

  const edgeSvg = edges.map((edge, index) => {
    const otherId = edge.source === centerId ? edge.target : edge.source;
    const key = otherId || `ghost-${index}`;
    const a = positions.get(centerId);
    const b = positions.get(key);
    if (!b) return '';
    const mx = (a.x + b.x) / 2;
    const my = (a.y + b.y) / 2;
    return `
      <line class="graph-edge ${esc(edge.layer)}" x1="${a.x}" y1="${a.y}" x2="${b.x}" y2="${b.y}"></line>
      <text class="edge-label" x="${mx}" y="${my - 3}">${esc(edge.type)}</text>
    `;
  }).join('');

  const nodeSvg = [
    `<g class="graph-node center" data-node="${centerId}" transform="translate(${cx} ${cy})"><circle r="24"></circle><text y="40">${esc(center.title)}</text></g>`,
    ...neighborKeys.map(key => {
      const point = positions.get(key);
      const node = neighborMap.get(key);
      const clickable = Boolean(node.id);
      return `<g class="graph-node" ${clickable ? `data-node="${node.id}"` : ''} transform="translate(${point.x} ${point.y})"><circle r="17"></circle><text y="31">${esc(node.title.length > 34 ? node.title.slice(0, 31) + '…' : node.title)}</text></g>`;
    })
  ].join('');

  return `<svg class="graph-canvas" viewBox="0 0 ${width} ${height}" role="img" aria-label="Local knowledge graph">${edgeSvg}${nodeSvg}</svg>`;
}

function renderGraphView(page, layer = 'all') {
  const counts = ['semantic', 'structural', 'runtime'].map(name => [name, neighborsFor(page.id, name).length]);
  return `
    <div class="graph-toolbar">
      <label>Layer
        <select id="graphLayer">
          ${['all', 'semantic', 'structural', 'runtime'].map(name => `<option value="${name}" ${name === layer ? 'selected' : ''}>${name}</option>`).join('')}
        </select>
      </label>
      ${counts.map(([name, count]) => `<span class="tag">${name}: ${count}</span>`).join('')}
    </div>
    ${renderGraphSvg(page.id, layer)}
    <p class="graph-legend">Local neighborhood only. Semantic, structural, and runtime edges are deliberately separate layers; unresolved targets remain visible rather than being silently discarded.</p>
  `;
}

function renderPromote(page) {
  const p = page.promotion;
  const issues = page.validation.issues || [];
  return `
    <div class="panel-grid">
      <section class="panel">
        <h3>MediaWiki target</h3>
        <dl>
          <dt>Title</dt><dd>${esc(p.target_title)}</dd>
          <dt>Namespace</dt><dd>${esc(p.namespace)}</dd>
          <dt>Content model</dt><dd>${esc(p.content_model)}</dd>
          <dt>Deployable mapping</dt><dd class="${p.deployable ? 'validation-pass' : 'validation-warning'}">${p.deployable ? 'yes' : 'projection only'}</dd>
          <dt>Source</dt><dd>${esc(p.source_path)}</dd>
        </dl>
      </section>
      <section class="panel">
        <h3>Promotion readiness</h3>
        <dl>
          <dt>Validation</dt><dd class="${p.validation_status === 'pass' ? 'validation-pass' : 'validation-error'}">${esc(p.validation_status)}</dd>
          <dt>Live comparison</dt><dd>${esc(p.live_comparison)}</dd>
          <dt>Executor</dt><dd><code>${esc(p.deployment_executor)}</code></dd>
        </dl>
        ${issues.length ? `<ul>${issues.map(issue => `<li>${esc(issue.code)}: ${esc(issue.field || '')} ${esc(issue.value || '')}</li>`).join('')}</ul>` : '<p class="validation-pass">No staging identity errors detected.</p>'}
      </section>
      <section class="panel">
        <h3>Required runtime objects</h3>
        ${arrayTags(p.dependencies)}
      </section>
      <section class="panel">
        <h3>Write contract</h3>
        <p>${esc(p.write_policy)}</p>
        <p class="muted">The workbench never promotes automatically. Existing deployment tooling remains authoritative for actual MediaWiki writes.</p>
      </section>
    </div>
  `;
}

async function renderPage(id, activeView = 'read', graphLayer = 'all') {
  const index = state.pageById.get(id);
  if (!index) {
    app.innerHTML = '<div class="empty">Staged page not found.</div>';
    return;
  }
  const page = await loadJSON(`./data/page/${encodeURIComponent(id)}.json`);
  const view = ['read', 'source', 'structure', 'graph', 'promote'].includes(activeView) ? activeView : 'read';
  let body = '';
  if (view === 'read') body = renderRead(page);
  if (view === 'source') body = renderSource(page);
  if (view === 'structure') body = renderStructure(page);
  if (view === 'graph') body = renderGraphView(page, graphLayer);
  if (view === 'promote') body = renderPromote(page);

  app.innerHTML = `
    <article>
      <h1 class="page-title">${esc(page.title)}</h1>
      <p class="page-subtitle">From BITwiki staging · ${esc(page.source_path)}</p>
      ${pageTabs(page, view)}
      <section class="view">${body}</section>
    </article>
  `;

  app.querySelectorAll('[data-view]').forEach(button => {
    button.addEventListener('click', () => setRoute(`/page/${id}`, { view: button.dataset.view }));
  });
  app.querySelector('#graphLayer')?.addEventListener('change', event => setRoute(`/page/${id}`, { view: 'graph', layer: event.target.value }));
  wireGraphNodeClicks();
}

function wireGraphNodeClicks() {
  app.querySelectorAll('.graph-node[data-node]').forEach(node => {
    node.addEventListener('click', () => setRoute(`/page/${node.dataset.node}`, { view: 'graph' }));
  });
}

function renderGraphExplorer(params) {
  const requested = params.get('node');
  const centerId = requested && state.nodeById.has(requested)
    ? requested
    : state.graph.nodes.find(node => node.entity_type)?.id || state.graph.nodes[0]?.id;
  const center = state.nodeById.get(centerId);
  const layer = params.get('layer') || 'all';
  app.innerHTML = `
    <h1 class="page-title">Graph explorer</h1>
    <p class="page-subtitle">Derived inspection graph; not a second ontology authority.</p>
    <section class="view">
      <div class="graph-toolbar">
        <label>Center
          <select id="graphCenter">
            ${state.graph.nodes.slice().sort((a,b) => a.title.localeCompare(b.title)).map(node => `<option value="${node.id}" ${node.id === centerId ? 'selected' : ''}>${esc(node.title)}</option>`).join('')}
          </select>
        </label>
        <label>Layer
          <select id="globalGraphLayer">
            ${['all', 'semantic', 'structural', 'runtime'].map(name => `<option value="${name}" ${name === layer ? 'selected' : ''}>${name}</option>`).join('')}
          </select>
        </label>
        ${center ? `<a href="#/page/${center.id}?view=structure">Inspect ${esc(center.title)}</a>` : ''}
      </div>
      ${centerId ? renderGraphSvg(centerId, layer) : '<div class="empty">No graph nodes generated.</div>'}
      <p class="graph-legend">The explorer intentionally starts from a local neighborhood instead of rendering an unreadable whole-corpus graph soup.</p>
    </section>
  `;
  app.querySelector('#graphCenter')?.addEventListener('change', event => setRoute('/graph', { node: event.target.value, layer }));
  app.querySelector('#globalGraphLayer')?.addEventListener('change', event => setRoute('/graph', { node: centerId, layer: event.target.value }));
  wireGraphNodeClicks();
}

async function route() {
  const { path, params } = parseRoute();
  window.scrollTo({ top: 0, behavior: 'instant' });
  if (path === '/' || path === '') {
    renderHome();
    return;
  }
  if (path === '/search') {
    const q = params.get('q') || '';
    const namespace = params.get('namespace') || '';
    searchInput.value = q;
    renderHome({ q, namespace });
    return;
  }
  if (path === '/graph') {
    renderGraphExplorer(params);
    return;
  }
  const pageMatch = path.match(/^\/page\/([^/]+)$/);
  if (pageMatch) {
    await renderPage(decodeURIComponent(pageMatch[1]), params.get('view') || 'read', params.get('layer') || 'all');
    return;
  }
  app.innerHTML = '<div class="empty">Unknown staging route.</div>';
}

function submitSearch() {
  const q = searchInput.value.trim();
  setRoute('/search', q ? { q } : {});
}

searchButton.addEventListener('click', submitSearch);
searchInput.addEventListener('keydown', event => {
  if (event.key === 'Enter') submitSearch();
});
window.addEventListener('hashchange', route);

initialize();
