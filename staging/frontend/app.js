const app = document.querySelector('#app');
const statusBar = document.querySelector('#statusBar');
const namespaceList = document.querySelector('#namespaceList');
const portalList = document.querySelector('#portalList');
const searchInput = document.querySelector('#searchInput');
const searchButton = document.querySelector('#searchButton');

const state = {
  pages: [],
  pageById: new Map(),
  pageByTitle: new Map(),
  pageByTitleFold: new Map(),
  fullPageCache: new Map(),
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

function liveWikiUrl(title) {
  return `https://bitwiki.org/wiki/${encodeURIComponent(String(title).replaceAll(' ', '_'))}`;
}

function normalizeTitle(title) {
  return String(title || '').replaceAll('_', ' ').trim();
}

function specialHref(title) {
  const normalized = normalizeTitle(title).toLocaleLowerCase();
  if (normalized === 'special:allpages') return '#/all-pages';
  if (normalized === 'special:categories') return '#/categories';
  if (normalized === 'special:random') return '#/random';
  if (normalized === 'special:recentchanges') return liveWikiUrl('Special:RecentChanges');
  if (normalized === 'special:newpages') return liveWikiUrl('Special:NewPages');
  return null;
}

function wikiHrefTitle(title) {
  const normalized = normalizeTitle(title).replace(/^:/, '');
  const special = specialHref(normalized);
  if (special) return special;
  return `#/wiki/${encodeURIComponent(normalized.replaceAll(' ', '_'))}`;
}

function pageHref(page) {
  return wikiHrefTitle(page.title);
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

async function loadFullPage(id) {
  if (state.fullPageCache.has(id)) return state.fullPageCache.get(id);
  const page = await loadJSON(`./data/page/${encodeURIComponent(id)}.json`);
  state.fullPageCache.set(id, page);
  return page;
}

function findPageByTitle(title) {
  const normalized = normalizeTitle(title);
  return state.pageByTitle.get(normalized) || state.pageByTitleFold.get(normalized.toLocaleLowerCase());
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
    state.pageByTitle = new Map(pages.map(page => [page.title, page]));
    state.pageByTitleFold = new Map(pages.map(page => [page.title.toLocaleLowerCase(), page]));
    state.graph = graph;
    state.nodeById = new Map(graph.nodes.map(node => [node.id, node]));
    state.ontology = ontology;
    state.meta = meta;

    renderNamespaces();
    await renderSidebarPortals();
    statusBar.innerHTML = `<strong>Staging projection</strong> · ${meta.page_count} source objects · ${meta.ontology_object_count} knowledge objects · ${meta.graph_edge_count} graph edges · <code>${esc(meta.source_sha.slice(0, 12))}</code>`;
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
    .map(([name, count]) => `<a href="#/all-pages?namespace=${encodeURIComponent(name)}">${esc(name)} <span class="muted">(${count})</span></a>`)
    .join('');
}

function parsePortalTemplate(source) {
  const match = source.match(/\{\{\s*(Domain portal|Topic portal)\b([\s\S]*?)\n\}\}/i);
  if (!match) return null;
  const params = {};
  for (const line of match[2].split('\n')) {
    const param = line.match(/^\s*\|([A-Za-z0-9_]+)\s*=\s*(.*)$/);
    if (param) params[param[1]] = param[2].trim();
  }
  return { kind: match[1].toLocaleLowerCase().startsWith('domain') ? 'domain' : 'topic', params };
}

function wikiFragment(value = '') {
  const links = [];
  let text = String(value).replace(/\[\[([^\[\]]+)\]\]/g, (_whole, inner) => {
    const [targetRaw, labelRaw] = inner.split('|', 2);
    const target = normalizeTitle(targetRaw).replace(/^:/, '');
    const label = labelRaw || target.replace(/^Portal:/, '');
    const token = `@@BITWIKILINK${links.length}@@`;
    links.push(`<a href="${wikiHrefTitle(target)}">${esc(label)}</a>`);
    return token;
  });
  text = text.replace(/<br\s*\/?\s*>/gi, '@@BITBR@@');
  let out = esc(text);
  out = out.replace(/'''''(.*?)'''''/g, '<strong><em>$1</em></strong>');
  out = out.replace(/'''(.*?)'''/g, '<strong>$1</strong>');
  out = out.replace(/''(.*?)''/g, '<em>$1</em>');
  out = out.replaceAll('@@BITBR@@', '<br>');
  links.forEach((link, index) => { out = out.replace(`@@BITWIKILINK${index}@@`, link); });
  return out;
}

async function renderSidebarPortals() {
  const portalIndexes = state.pages.filter(page => page.namespace === 'Portal');
  const fullPages = await Promise.all(portalIndexes.map(page => loadFullPage(page.id)));
  const domainPortals = fullPages
    .map(page => ({ page, portal: parsePortalTemplate(page.source) }))
    .filter(item => item.portal?.kind === 'domain')
    .sort((a, b) => a.page.title.localeCompare(b.page.title));

  portalList.innerHTML = domainPortals
    .map(({ page }) => `<a href="${pageHref(page)}">${esc(page.title.replace(/^Portal:/, ''))}</a>`)
    .join('');
}

function renderDirectory({ q = '', namespace = '', heading = 'All pages' } = {}) {
  const query = q.trim().toLocaleLowerCase();
  const pages = state.pages
    .filter(page => !namespace || page.namespace === namespace)
    .filter(page => !query || [page.title, page.namespace, page.entity_type, page.domain, page.source_path].some(v => String(v || '').toLocaleLowerCase().includes(query)))
    .sort((a, b) => a.title.localeCompare(b.title));

  app.innerHTML = `
    <article class="mw-special">
      <h1 class="page-title">${esc(heading)}</h1>
      <p class="page-subtitle">Derived staging index over repository-backed MediaWiki titles.</p>
      <div class="directory-toolbar">
        <span>${pages.length} titles</span>
        ${namespace ? `<a href="#/all-pages">Clear namespace filter</a>` : ''}
      </div>
      <div class="page-list">
        ${pages.map(page => `
          <div class="page-row">
            <a href="${pageHref(page)}">${esc(page.title)}</a>
            <span class="muted">${esc(page.namespace)}</span>
            <span class="muted">${esc(page.entity_type || page.content_model)}</span>
            <span class="${page.validation_status === 'pass' ? 'validation-pass' : 'validation-error'}">${esc(page.validation_status)}</span>
          </div>
        `).join('') || '<div class="empty">No staged source objects match this query.</div>'}
      </div>
    </article>
  `;
}

function pageTabs(page, active) {
  const tabs = ['read', 'source', 'structure', 'graph', 'promote'];
  return `
    <div class="tabs" role="tablist" aria-label="Page inspection modes">
      ${tabs.map(tab => `<button class="${tab === active ? 'active' : ''}" data-view="${tab}">${tab[0].toUpperCase() + tab.slice(1)}</button>`).join('')}
    </div>
  `;
}

function identityCard(page) {
  const identity = page.parsed.identity || {};
  return `
    <aside class="inspector-card">
      <h2>Staging inspection</h2>
      <dl class="inspector-grid">
        <dt>Entity type</dt><dd>${esc(identity.entity_type || 'Not specified')}</dd>
        <dt>Domain</dt><dd>${esc(identity.domain || 'Not specified')}</dd>
        <dt>Epistemic</dt><dd>${esc(identity.status || 'Not specified')}</dd>
        <dt>Provenance</dt><dd>${esc(identity.provenance || 'Not specified')}</dd>
        <dt>Namespace</dt><dd>${esc(page.namespace)}</dd>
        <dt>Validation</dt><dd class="${page.validation.status === 'pass' ? 'validation-pass' : 'validation-error'}">${esc(page.validation.status)}</dd>
      </dl>
      <div class="inspector-actions">
        <a href="${repoFileUrl(page.source_path)}" target="_blank" rel="noreferrer">Git source ↗</a>
        <a href="${liveWikiUrl(page.title)}" target="_blank" rel="noreferrer">Live title ↗</a>
      </div>
    </aside>
  `;
}

function portalMembers(page, portal) {
  const params = portal.params;
  if (portal.kind === 'domain' && params.domain) {
    return state.pages
      .filter(candidate => candidate.namespace === 'Main' && candidate.domain === params.domain)
      .sort((a, b) => a.title.localeCompare(b.title));
  }

  if (params.category) {
    const target = `Category:${params.category}`;
    const ids = new Set(state.graph.edges
      .filter(edge => edge.layer === 'structural' && edge.type === 'Category' && edge.target_title === target)
      .map(edge => edge.source));
    return [...ids]
      .map(id => state.pageById.get(id))
      .filter(candidate => candidate && candidate.namespace === 'Main')
      .sort((a, b) => a.title.localeCompare(b.title));
  }
  return [];
}

function renderPortalRead(page, portal) {
  const p = portal.params;
  const members = portalMembers(page, portal);
  const parent = p.parent ? `<div class="portal-parent"><strong>Parent portals:</strong> ${wikiFragment(p.parent)}</div>` : '';
  const subportals = p.subportals ? `
    <section>
      <h2>Subportals</h2>
      <div class="portal-fragment">${wikiFragment(p.subportals.replace(/^\*\s*/, ''))}</div>
    </section>` : '';

  return `
    <div class="read-layout portal-read-layout">
      <article class="article-body portal-body">
        ${parent}
        <p class="portal-description">${wikiFragment(p.description || '')}</p>

        <section>
          <h2>Start here</h2>
          <p>${wikiFragment(p.start || '')}</p>
        </section>

        ${p.learning_path ? `
          <section>
            <h2>Learn progressively</h2>
            <p>${wikiFragment(p.learning_path)}</p>
          </section>` : ''}

        <section>
          <h2>Browse ${portal.kind === 'domain' ? 'this domain' : 'this topic'}</h2>
          <div class="portal-query-note">Staging projection of the MediaWiki semantic/category browse surface.</div>
          ${members.length ? `
            <table class="portal-query-table">
              <thead><tr><th>Page</th><th>Entity type</th><th>Epistemic status</th></tr></thead>
              <tbody>${members.map(member => `<tr><td><a href="${pageHref(member)}">${esc(member.title)}</a></td><td>${esc(member.entity_type || '—')}</td><td>${esc(member.status || '—')}</td></tr>`).join('')}</tbody>
            </table>` : '<div class="empty compact">No staged Main-namespace members currently resolve for this portal.</div>'}
          ${p.category ? `<p><a href="${wikiHrefTitle(`Category:${p.category}`)}">Browse the ${esc(p.category)} category</a></p>` : ''}
        </section>

        ${subportals}

        <section>
          <h2>Related portals</h2>
          <p>${wikiFragment(p.related || 'None specified.')}</p>
        </section>

        <section class="portal-about">
          <h2>About this portal</h2>
          <p>This portal is a reader-facing view over the knowledge corpus. It does not define the ontology and does not imply that its domain or topic is exclusive.</p>
          <p>In staging, the same source-defined portal becomes inspectable through Structure, Graph, and Promote without changing its MediaWiki representation.</p>
        </section>
      </article>
      ${identityCard(page)}
    </div>
  `;
}

function renderRead(page) {
  const portal = page.namespace === 'Portal' ? parsePortalTemplate(page.source) : null;
  if (portal) return renderPortalRead(page, portal);
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
  const portal = page.namespace === 'Portal' ? parsePortalTemplate(page.source) : null;
  return `
    <div class="panel-grid">
      <section class="panel">
        <h3>MediaWiki identity</h3>
        <dl>
          <dt>Title</dt><dd>${esc(page.title)}</dd>
          <dt>Namespace</dt><dd>${esc(page.namespace)}</dd>
          <dt>Content model</dt><dd>${esc(page.content_model)}</dd>
          <dt>Projection</dt><dd>${esc(page.projection_kind)}</dd>
          ${portal ? `<dt>Portal shell</dt><dd>${esc(portal.kind === 'domain' ? 'Template:Domain portal' : 'Template:Topic portal')}</dd>` : ''}
        </dl>
      </section>
      <section class="panel">
        <h3>Knowledge identity</h3>
        <dl>
          <dt>Entity type</dt><dd>${esc(identity.entity_type || '—')}</dd>
          <dt>Domain</dt><dd>${esc(identity.domain || '—')}</dd>
          <dt>Status</dt><dd>${esc(identity.status || '—')}</dd>
          <dt>Provenance</dt><dd>${esc(identity.provenance || '—')}</dd>
        </dl>
      </section>
      <section class="panel">
        <h3>Document anatomy</h3>
        ${parsed.headings.length ? `<ol>${parsed.headings.map(h => `<li>${esc(h.title)} <span class="muted">H${h.level}</span></li>`).join('')}</ol>` : '<span class="muted">No literal wikitext headings extracted; this page may be template-driven.</span>'}
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
      neighborMap.set(key, { id: otherId, title: otherId ? graphNodeLabel(otherId) : edge.target_title });
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
    return `<line class="graph-edge ${esc(edge.layer)}" x1="${a.x}" y1="${a.y}" x2="${b.x}" y2="${b.y}"></line><text class="edge-label" x="${mx}" y="${my - 3}">${esc(edge.type)}</text>`;
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
    <p class="graph-legend">Local neighborhood only. Semantic, structural, and runtime edges remain separate inspection layers.</p>
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

function hydrateRawTables(container) {
  const rawLines = [...container.querySelectorAll('.wikitext-raw-line')];
  const consumed = new Set();

  for (const start of rawLines) {
    if (consumed.has(start) || !start.textContent.trim().startsWith('{|')) continue;
    const sequence = [start];
    let cursor = start.nextElementSibling;
    while (cursor?.classList.contains('wikitext-raw-line')) {
      sequence.push(cursor);
      if (cursor.textContent.trim() === '|}') break;
      cursor = cursor.nextElementSibling;
    }
    if (sequence.at(-1)?.textContent.trim() !== '|}') continue;

    const table = document.createElement('table');
    table.className = 'wikitable staged-wikitable';
    let row = null;
    const ensureRow = () => {
      if (!row) {
        row = document.createElement('tr');
        table.appendChild(row);
      }
      return row;
    };

    for (const line of sequence.slice(1, -1)) {
      const text = line.textContent.trim();
      if (!text || text === '|-') {
        row = null;
        continue;
      }
      if (text.startsWith('!')) {
        const current = ensureRow();
        line.innerHTML.replace(/^!\s*/, '').split(/\s*!!\s*/).forEach(value => {
          const cell = document.createElement('th');
          cell.innerHTML = value;
          current.appendChild(cell);
        });
        continue;
      }
      if (text.startsWith('|')) {
        const current = ensureRow();
        line.innerHTML.replace(/^\|\s*/, '').split(/\s*\|\|\s*/).forEach(value => {
          const cell = document.createElement('td');
          cell.innerHTML = value;
          current.appendChild(cell);
        });
      }
    }

    start.replaceWith(table);
    sequence.slice(1).forEach(line => line.remove());
    sequence.forEach(line => consumed.add(line));
  }
}

function rewriteArticleLinks(container) {
  const specialByLabel = new Map([
    ['all pages', '#/all-pages'],
    ['random page', '#/random'],
    ['categories', '#/categories'],
    ['recent edits', liveWikiUrl('Special:RecentChanges')],
    ['new pages', liveWikiUrl('Special:NewPages')],
  ]);

  container.querySelectorAll('a[href^="#/page/"]').forEach(anchor => {
    const raw = anchor.getAttribute('href').split('/').pop();
    const page = state.pageById.get(decodeURIComponent(raw));
    if (page) {
      anchor.setAttribute('href', pageHref(page));
      return;
    }
    const replacement = specialByLabel.get(anchor.textContent.trim().toLocaleLowerCase());
    if (replacement) anchor.setAttribute('href', replacement);
  });
}

async function renderPage(id, activeView = 'read', graphLayer = 'all') {
  const index = state.pageById.get(id);
  if (!index) {
    app.innerHTML = '<div class="empty">Staged page not found.</div>';
    return;
  }
  const page = await loadFullPage(id);
  const view = ['read', 'source', 'structure', 'graph', 'promote'].includes(activeView) ? activeView : 'read';
  let body = '';
  if (view === 'read') body = renderRead(page);
  if (view === 'source') body = renderSource(page);
  if (view === 'structure') body = renderStructure(page);
  if (view === 'graph') body = renderGraphView(page, graphLayer);
  if (view === 'promote') body = renderPromote(page);

  const isMainPage = page.title === 'Main Page';
  app.innerHTML = `
    <article class="${isMainPage ? 'main-page-shell' : ''}">
      ${isMainPage && view === 'read' ? '' : `<h1 class="page-title">${esc(page.title)}</h1>`}
      <div class="page-meta-line">
        <span>${isMainPage ? 'BITwiki Main Page' : `From BITwiki staging · ${esc(page.source_path)}`}</span>
        <span class="page-meta-actions"><a href="${repoFileUrl(page.source_path)}" target="_blank" rel="noreferrer">Git source ↗</a> · <a href="${liveWikiUrl(page.title)}" target="_blank" rel="noreferrer">Live BITwiki ↗</a></span>
      </div>
      ${pageTabs(page, view)}
      <section class="view">${body}</section>
    </article>
  `;

  app.querySelectorAll('[data-view]').forEach(button => {
    button.addEventListener('click', () => setRoute(`/wiki/${encodeURIComponent(page.title.replaceAll(' ', '_'))}`, { view: button.dataset.view }));
  });
  app.querySelector('#graphLayer')?.addEventListener('change', event => setRoute(`/wiki/${encodeURIComponent(page.title.replaceAll(' ', '_'))}`, { view: 'graph', layer: event.target.value }));
  hydrateRawTables(app);
  rewriteArticleLinks(app);
  wireGraphNodeClicks();
}

function wireGraphNodeClicks() {
  app.querySelectorAll('.graph-node[data-node]').forEach(node => {
    node.addEventListener('click', () => {
      const page = state.pageById.get(node.dataset.node);
      if (page) setRoute(`/wiki/${encodeURIComponent(page.title.replaceAll(' ', '_'))}`, { view: 'graph' });
    });
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
    <h1 class="page-title">Knowledge graph</h1>
    <p class="page-subtitle">Staging inspection surface over MediaWiki titles and semantic/runtime connections.</p>
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
        ${center ? `<a href="${wikiHrefTitle(center.title)}?view=structure">Inspect ${esc(center.title)}</a>` : ''}
      </div>
      ${centerId ? renderGraphSvg(centerId, layer) : '<div class="empty">No graph nodes generated.</div>'}
      <p class="graph-legend">The graph is a derived view. MediaWiki titles, source files, SMW properties, templates, and runtime dependencies remain the underlying concepts.</p>
    </section>
  `;
  app.querySelector('#graphCenter')?.addEventListener('change', event => setRoute('/graph', { node: event.target.value, layer }));
  app.querySelector('#globalGraphLayer')?.addEventListener('change', event => setRoute('/graph', { node: centerId, layer: event.target.value }));
  wireGraphNodeClicks();
}

async function renderPortals() {
  const indexes = state.pages.filter(page => page.namespace === 'Portal');
  const fullPages = await Promise.all(indexes.map(page => loadFullPage(page.id)));
  const portals = fullPages
    .map(page => ({ page, portal: parsePortalTemplate(page.source) }))
    .filter(item => item.portal)
    .sort((a, b) => a.page.title.localeCompare(b.page.title));
  const domains = portals.filter(item => item.portal.kind === 'domain');
  const topics = portals.filter(item => item.portal.kind === 'topic');

  const cards = items => items.map(({ page, portal }) => `
    <a class="portal-card" href="${pageHref(page)}">
      <strong>${esc(portal.params.title || page.title.replace(/^Portal:/, ''))}</strong>
      <span>${esc((portal.params.description || '').slice(0, 180))}${(portal.params.description || '').length > 180 ? '…' : ''}</span>
    </a>`).join('');

  app.innerHTML = `
    <article class="mw-special">
      <h1 class="page-title">Portals</h1>
      <p class="page-subtitle">Reader-facing navigation views already defined in the MediaWiki corpus.</p>
      <section class="portal-directory-section">
        <h2>Knowledge domains</h2>
        <div class="portal-grid">${cards(domains)}</div>
      </section>
      <section class="portal-directory-section">
        <h2>Focused subportals</h2>
        <div class="portal-grid">${cards(topics)}</div>
      </section>
      <p class="muted">Portal parentage is navigation, not ontology inheritance. The staging frontend preserves that distinction.</p>
    </article>`;
}

function renderCategories() {
  const categoryPages = state.pages.filter(page => page.namespace === 'Category').sort((a, b) => a.title.localeCompare(b.title));
  const counts = new Map();
  for (const edge of state.graph.edges) {
    if (edge.layer !== 'structural' || edge.type !== 'Category') continue;
    counts.set(edge.target_title, (counts.get(edge.target_title) || 0) + 1);
  }
  app.innerHTML = `
    <article class="mw-special">
      <h1 class="page-title">Categories</h1>
      <p class="page-subtitle">MediaWiki category browse surface reconstructed from staged source relations.</p>
      <div class="category-index">
        ${categoryPages.map(page => `<a href="${pageHref(page)}"><span>${esc(page.title.replace(/^Category:/, ''))}</span><small>${counts.get(page.title) || 0} members</small></a>`).join('')}
      </div>
    </article>`;
}

function renderRandom() {
  const candidates = state.pages.filter(page => page.namespace === 'Main' && page.entity_type);
  if (!candidates.length) return renderDirectory({ namespace: 'Main', heading: 'Main namespace' });
  const page = candidates[Math.floor(Math.random() * candidates.length)];
  setRoute(`/wiki/${encodeURIComponent(page.title.replaceAll(' ', '_'))}`);
}

async function route() {
  const { path, params } = parseRoute();
  window.scrollTo({ top: 0, behavior: 'instant' });

  if (path === '/' || path === '') {
    const mainPage = findPageByTitle('Main Page');
    if (mainPage) await renderPage(mainPage.id, params.get('view') || 'read', params.get('layer') || 'all');
    else renderDirectory({ heading: 'BITwiki' });
    return;
  }
  if (path === '/search') {
    const q = params.get('q') || '';
    const namespace = params.get('namespace') || '';
    searchInput.value = q;
    renderDirectory({ q, namespace, heading: q ? `Search results for “${q}”` : 'Search' });
    return;
  }
  if (path === '/all-pages') {
    const namespace = params.get('namespace') || '';
    renderDirectory({ namespace, heading: namespace ? `${namespace} namespace` : 'All pages' });
    return;
  }
  if (path === '/portals') {
    await renderPortals();
    return;
  }
  if (path === '/categories') {
    renderCategories();
    return;
  }
  if (path === '/random') {
    renderRandom();
    return;
  }
  if (path === '/graph') {
    renderGraphExplorer(params);
    return;
  }

  const wikiMatch = path.match(/^\/wiki\/(.+)$/);
  if (wikiMatch) {
    const title = normalizeTitle(decodeURIComponent(wikiMatch[1]));
    const special = specialHref(title);
    if (special?.startsWith('#')) {
      location.hash = special.slice(1);
      return;
    }
    const page = findPageByTitle(title);
    if (page) {
      await renderPage(page.id, params.get('view') || 'read', params.get('layer') || 'all');
      return;
    }
    app.innerHTML = `<div class="empty"><strong>${esc(title)}</strong><br>This MediaWiki title is referenced but not present in the staged repository projection.</div>`;
    return;
  }

  const legacyPageMatch = path.match(/^\/page\/([^/]+)$/);
  if (legacyPageMatch) {
    const page = state.pageById.get(decodeURIComponent(legacyPageMatch[1]));
    if (page) {
      setRoute(`/wiki/${encodeURIComponent(page.title.replaceAll(' ', '_'))}`, Object.fromEntries(params.entries()));
      return;
    }
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
