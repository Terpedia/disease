const list = document.querySelector('#disease-list');
const detail = document.querySelector('#disease-detail');
const search = document.querySelector('#search');
const meta = document.querySelector('#catalog-meta');
let diseases = [];
let records = new Map();
let phenotypeCounts = new Map();

const esc = (value = '') => String(value).replace(/[&<>"']/g, (char) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
const tags = (items, formatter) => items.map((item) => `<span class="tag">${formatter(item)}</span>`).join('');

function stats(record, disease) {
  return `<div class="stats"><span><strong>${record.markers?.length || 0}</strong> markers</span><span><strong>${record.genes?.length || 0}</strong> genes</span><span><strong>${record.pathways?.length || 0}</strong> pathways</span><span><strong>${record.regulators?.length || 0}</strong> regulators</span><span><strong>${phenotypeCounts.get(disease.id) || 0}</strong> phenotypes</span></div>`;
}

function renderIndex() {
  const query = search.value.trim().toLowerCase();
  const visible = diseases.filter((disease) => [disease.name, ...(disease.aliases || [])].join(' ').toLowerCase().includes(query));
  meta.textContent = `${visible.length} of ${diseases.length} disease${diseases.length === 1 ? '' : 's'} · source-linked claims and structured biology`;
  list.hidden = false;
  detail.hidden = true;
  list.innerHTML = visible.map((disease) => {
    const record = records.get(disease.id) || {};
    return `<article class="card"><div class="card-top"><span class="eyebrow">${esc(disease.classification || 'Unclassified')}</span><span class="status">${esc(disease.status)}</span></div><h2>${esc(disease.name)}</h2><p>${esc(disease.overview)}</p>${stats(record, disease)}<a class="card-link" href="#disease/${encodeURIComponent(disease.id)}">Open disease page <span>→</span></a></article>`;
  }).join('') || '<p class="empty">No matching diseases yet.</p>';
}

function renderDetail(id) {
  const disease = diseases.find((item) => item.id === id);
  if (!disease) { window.location.hash = ''; return; }
  const record = records.get(id) || {};
  meta.textContent = 'Disease detail · evidence remains source-linked';
  list.hidden = true;
  detail.hidden = false;
  detail.innerHTML = `<a class="back" href="#">← All diseases</a><div class="detail-head"><div><p class="eyebrow">${esc(disease.classification || 'Unclassified')} · ${esc(disease.status)}</p><h1>${esc(disease.name)}</h1><p class="detail-lede">${esc(disease.overview)}</p></div><div class="identifiers"><span>MONDO</span><code>${esc(record.identifiers?.mondo || 'not mapped')}</code></div></div>${stats(record, disease)}<div class="detail-grid"><section class="panel"><p class="eyebrow">01 / Biomarkers</p><h2>What can be measured</h2><div class="facts-list">${tags(record.markers || [], (item) => `${esc(item.name)} <small>${esc(item.compartment)} · ${esc(item.direction)}</small>`) || '<p class="muted">No markers ingested yet.</p>'}</div><p class="panel-note">Marker status is contextual; research signals are not automatically diagnostic.</p></section><section class="panel"><p class="eyebrow">02 / Genes</p><h2>Molecular actors</h2><div class="facts-list">${tags(record.genes || [], (item) => `<strong>${esc(item.symbol)}</strong> <small>${esc(item.role)}</small>`) || '<p class="muted">No genes ingested yet.</p>'}</div></section><section class="panel panel-wide"><p class="eyebrow">03 / Mechanism</p><h2>Pathways and regulators</h2><div class="mechanism"><div><h3>Pathways</h3>${tags(record.pathways || [], (item) => `${esc(item.name)} <small>${esc(item.source)}</small>`)}</div><div><h3>Regulators</h3>${tags(record.regulators || [], (item) => `<strong>${esc(item.symbol)}</strong> → ${esc(item.target)}`)}</div></div></section><section class="panel panel-wide"><p class="eyebrow">04 / Evidence ledger</p><h2>Claims worth checking</h2>${disease.claims.map((claim) => `<div class="claim"><span class="confidence ${esc(claim.confidence)}">${esc(claim.confidence)}</span><p>${esc(claim.statement)}</p><a href="${esc(claim.source.url)}" target="_blank" rel="noreferrer">${esc(claim.source.title)} ↗</a></div>`).join('')}</section></div>`;
}

function render() { const match = window.location.hash.match(/^#disease\/(.+)$/); match ? renderDetail(decodeURIComponent(match[1])) : renderIndex(); }

Promise.all([
  fetch('data/disease-catalog.json').then((response) => response.json()),
  fetch('data/disease-records.json').then((response) => response.json()),
  fetch('data/phenotype-annotations.json').then((response) => response.json())
]).then(([catalog, structured, phenotypes]) => {
  diseases = catalog.diseases;
  records = new Map(structured.records.map((record) => [record.id, record]));
  (phenotypes.annotations || []).forEach((annotation) => phenotypeCounts.set(annotation.disease_id, (phenotypeCounts.get(annotation.disease_id) || 0) + 1));
  render();
}).catch(() => { meta.textContent = 'Catalog unavailable'; list.innerHTML = '<p class="empty">Could not load the catalog.</p>'; });
search.addEventListener('input', renderIndex);
window.addEventListener('hashchange', render);
