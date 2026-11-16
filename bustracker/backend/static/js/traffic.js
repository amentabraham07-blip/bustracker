/* ── TRAFFIC BLOCKS PAGE ── */

document.addEventListener('DOMContentLoaded', async () => {
  const user = await initPage();
  if (!user) return;

  if (user.role === 'police' || user.role === 'admin') {
    document.getElementById('traffic-actions').innerHTML = `
      <button class="btn-primary" onclick="document.getElementById('add-block-form').classList.toggle('hidden')">+ Report Block</button>
    `;
  }
  loadTrafficBlocks(user);
});

async function loadTrafficBlocks(user) {
  if (!user) {
    const stored = localStorage.getItem('bt_user');
    user = stored ? JSON.parse(stored) : { role: 'user' };
  }
  const grid = document.getElementById('blocks-grid');
  try {
    const blocks = await GET('/traffic-blocks/');
    if (!blocks.length) {
      grid.innerHTML = emptyState('🚦', 'No active traffic blocks');
      grid.className = '';
      return;
    }
    grid.className = 'blocks-grid';
    grid.innerHTML = blocks.map(b => `
      <div class="block-card severity-${b.severity}">
        <div class="block-title">⚠️ ${b.title}</div>
        <div class="block-desc">${b.description}</div>
        <div class="block-meta">
          <span class="badge badge-${b.severity}">${b.severity.toUpperCase()}</span>
          <span style="font-size:0.8rem;color:var(--text-muted)">Radius: ${b.radius}m</span>
        </div>
        <div style="font-size:0.82rem;color:var(--text-secondary);margin-bottom:12px;">
          📍 ${b.latitude.toFixed(4)}, ${b.longitude.toFixed(4)}<br>
          👮 ${b.officer_name} · ${formatTime(b.created_at)}
        </div>
        ${(user.role === 'police' || user.role === 'admin') ? `
          <button class="btn-success" onclick="clearBlock(${b.id})">✅ Mark Cleared</button>
        ` : ''}
      </div>
    `).join('');
  } catch {
    grid.innerHTML = emptyState('🚧', 'Failed to load traffic blocks.');
  }
}

async function createTrafficBlock() {
  const data = {
    title:       document.getElementById('block-title').value.trim(),
    description: document.getElementById('block-desc').value.trim(),
    latitude:    parseFloat(document.getElementById('block-lat').value),
    longitude:   parseFloat(document.getElementById('block-lng').value),
    severity:    document.getElementById('block-severity').value,
    radius:      parseFloat(document.getElementById('block-radius').value) || 500,
  };
  if (!data.title || isNaN(data.latitude) || isNaN(data.longitude)) {
    toast('Title, latitude and longitude are required', 'error'); return;
  }
  try {
    await POST('/traffic-blocks/', data);
    toast('Traffic block reported — all drivers notified!', 'success');
    document.getElementById('add-block-form').classList.add('hidden');
    clearBlockForm();
    const user = JSON.parse(localStorage.getItem('bt_user') || '{}');
    loadTrafficBlocks(user);
  } catch (err) { toast(extractError(err), 'error'); }
}

async function clearBlock(id) {
  if (!confirm('Mark this traffic block as cleared?')) return;
  try {
    await POST(`/traffic-blocks/${id}/clear/`);
    toast('Traffic block cleared!', 'success');
    const user = JSON.parse(localStorage.getItem('bt_user') || '{}');
    loadTrafficBlocks(user);
  } catch (err) { toast(extractError(err), 'error'); }
}

function useMyLocation() {
  if (!navigator.geolocation) { toast('Geolocation not supported', 'error'); return; }
  navigator.geolocation.getCurrentPosition(pos => {
    document.getElementById('block-lat').value = pos.coords.latitude.toFixed(6);
    document.getElementById('block-lng').value = pos.coords.longitude.toFixed(6);
    toast('Location set from GPS');
  }, () => toast('Could not get your location', 'error'));
}

function clearBlockForm() {
  ['block-title', 'block-desc', 'block-lat', 'block-lng'].forEach(id => {
    document.getElementById(id).value = '';
  });
  document.getElementById('block-severity').value = 'medium';
  document.getElementById('block-radius').value = '500';
}
