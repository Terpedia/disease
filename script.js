const list = document.querySelector('#disease-list');
const search = document.querySelector('#search');
const meta = document.querySelector('#catalog-meta');
let diseases = [];

function render() {
  const query = search.value.trim().toLowerCase();
  const visible = diseases.filter((disease) => [disease.name, ...(disease.aliases || [])]
    .join(' ').toLowerCase().includes(query));
  meta.textContent = `${visible.length} of ${diseases.length} disease${diseases.length === 1 ? '' : 's'} · claims carry their own confidence and source`;
  list.innerHTML = visible.map((disease) => `
    <article class="card">
      <div class="card-top"><span class="eyebrow">${disease.classification || 'Unclassified'}</span><span class="status">${disease.status}</span></div>
      <h2>${disease.name}</h2>
      <p>${disease.overview}</p>
      <div class="claims"><strong>${disease.claims.length}</strong> evidence claim${disease.claims.length === 1 ? '' : 's'}</div>
      ${disease.claims.map((claim) => `<div class="claim"><span class="confidence ${claim.confidence}">${claim.confidence}</span><p>${claim.statement}</p><a href="${claim.source.url}" target="_blank" rel="noreferrer">${claim.source.title} ↗</a></div>`).join('')}
    </article>`).join('') || '<p class="empty">No matching diseases yet.</p>';
}

fetch('data/disease-catalog.json').then((response) => response.json()).then((catalog) => {
  diseases = catalog.diseases;
  render();
}).catch(() => { meta.textContent = 'Catalog unavailable'; list.innerHTML = '<p class="empty">Could not load the catalog.</p>'; });
search.addEventListener('input', render);
