const list = document.querySelector('#disease-list');
const search = document.querySelector('#search');
const meta = document.querySelector('#catalog-meta');
let diseases = [];
let records = new Map();

function render() {
  const query = search.value.trim().toLowerCase();
  const visible = diseases.filter((disease) => [disease.name, ...(disease.aliases || [])]
    .join(' ').toLowerCase().includes(query));
  meta.textContent = `${visible.length} of ${diseases.length} disease${diseases.length === 1 ? '' : 's'} · claims carry their own confidence and source`;
  list.innerHTML = visible.map((disease) => {
    const record = records.get(disease.id) || {};
    const markers = record.markers || [];
    const genes = record.genes || [];
    const pathways = record.pathways || [];
    const regulators = record.regulators || [];
    return `
    <article class="card">
      <div class="card-top"><span class="eyebrow">${disease.classification || 'Unclassified'}</span><span class="status">${disease.status}</span></div>
      <h2>${disease.name}</h2>
      <p>${disease.overview}</p>
      <div class="stats"><span><strong>${markers.length}</strong> markers</span><span><strong>${genes.length}</strong> genes</span><span><strong>${pathways.length}</strong> pathways</span><span><strong>${regulators.length}</strong> regulators</span></div>
      <div class="claims"><strong>${disease.claims.length}</strong> evidence claim${disease.claims.length === 1 ? '' : 's'}</div>
      ${markers.length ? `<section class="facts"><h3>Biochemical markers</h3><p>${markers.map((item) => `<span class="tag">${item.name} · ${item.direction}</span>`).join('')}</p></section>` : ''}
      ${genes.length ? `<section class="facts"><h3>Genes</h3><p>${genes.map((item) => `<span class="tag">${item.symbol} · ${item.role}</span>`).join('')}</p></section>` : ''}
      ${pathways.length ? `<section class="facts"><h3>Pathways</h3><p>${pathways.map((item) => `<span class="tag">${item.name}</span>`).join('')}</p></section>` : ''}
      ${regulators.length ? `<section class="facts"><h3>Regulators</h3><p>${regulators.map((item) => `<span class="tag">${item.symbol} → ${item.target}</span>`).join('')}</p></section>` : ''}
      ${disease.claims.map((claim) => `<div class="claim"><span class="confidence ${claim.confidence}">${claim.confidence}</span><p>${claim.statement}</p><a href="${claim.source.url}" target="_blank" rel="noreferrer">${claim.source.title} ↗</a></div>`).join('')}
    </article>`;
  }).join('') || '<p class="empty">No matching diseases yet.</p>';
}

Promise.all([fetch('data/disease-catalog.json').then((response) => response.json()), fetch('data/disease-records.json').then((response) => response.json())]).then(([catalog, structured]) => {
  diseases = catalog.diseases;
  records = new Map(structured.records.map((record) => [record.id, record]));
  render();
}).catch(() => { meta.textContent = 'Catalog unavailable'; list.innerHTML = '<p class="empty">Could not load the catalog.</p>'; });
search.addEventListener('input', render);
