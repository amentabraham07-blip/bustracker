/* ── BUS STOPS PAGE ── */

let _allStops = [];
let _currentUser = null;

document.addEventListener('DOMContentLoaded', async () => {
  _currentUser = await initPage();
  if (!_currentUser) return;

  // Show Add Stop button only for admin/superuser
  if (_currentUser.role === 'admin' || _currentUser.is_superuser) {
    document.getElementById('add-stop-btn').style.display = '';
  }

  loadStops();
});

async function loadStops() {
  const grid = document.getElementById('stops-grid');
  grid.innerHTML = '<div class="empty-state"><p>Loading...</p></div>';
  try {
    _allStops = await GET('/stops/');
    renderStops(_allStops);
  } catch {
    grid.innerHTML = emptyState('📍', 'Failed to load bus stops.');
  }
}

function renderStops(stops) {
  const grid = document.getElementById('stops-grid');
  const canAdmin = _currentUser && (_currentUser.role === 'admin' || _currentUser.is_superuser);

  if (!stops.length) {
    grid.innerHTML = emptyState('📍', 'No bus stops found.');
    return;
  }

  grid.innerHTML = stops.map(s => `
    <div class="stop-card" id="stop-card-${s.id}">
      <div style="display:flex;justify-content:space-between;align-items:flex-start;">
        <div class="stop-name">📍 ${s.name}</div>
        ${canAdmin ? `
          <button onclick="deleteStop(${s.id}, '${s.name.replace(/'/g, "\\'")}')"
            style="background:transparent;border:none;color:var(--text-muted);cursor:pointer;font-size:1rem;padding:0;line-height:1;"
            title="Delete stop">✕</button>
        ` : ''}
      </div>
      ${s.address ? `<div style="font-size:0.8rem;color:var(--text-muted);margin-top:3px;">${s.address}</div>` : ''}
      <div class="stop-coords" style="margin-top:6px;">${s.latitude.toFixed(5)}, ${s.longitude.toFixed(5)}</div>
      ${s.distance_km !== undefined
        ? `<span class="stop-distance">📏 ${s.distance_km} km away</span>`
        : ''}
      <div style="margin-top:10px;">
        <button class="btn-outline" style="font-size:0.78rem;padding:4px 10px;"
          onclick="viewOnMap(${s.latitude}, ${s.longitude}, '${s.name.replace(/'/g, "\\'")}')">
          🗺 View on Map
        </button>
      </div>
    </div>
  `).join('');
}

function filterStops() {
  const q = document.getElementById('stops-search').value.toLowerCase();
  const filtered = _allStops.filter(s =>
    s.name.toLowerCase().includes(q) || (s.address || '').toLowerCase().includes(q)
  );
  renderStops(filtered);
}

function findNearbyStops() {
  if (!navigator.geolocation) { toast('Geolocation not supported', 'error'); return; }
  toast('Getting your location...');
  navigator.geolocation.getCurrentPosition(async pos => {
    try {
      const stops = await GET(`/stops/nearby/?lat=${pos.coords.latitude}&lng=${pos.coords.longitude}&radius=3`);
      renderStops(stops);
      toast(`Found ${stops.length} stop${stops.length !== 1 ? 's' : ''} within 3 km`);
    } catch { toast('Failed to find nearby stops', 'error'); }
  }, () => toast('Location access denied', 'error'));
}

function toggleAddStopForm() {
  document.getElementById('add-stop-form').classList.toggle('hidden');
  document.getElementById('stop-error').classList.add('hidden');
}

function pickLocationForStop() {
  if (!navigator.geolocation) { toast('Geolocation not supported', 'error'); return; }
  navigator.geolocation.getCurrentPosition(pos => {
    document.getElementById('stop-lat').value = pos.coords.latitude.toFixed(6);
    document.getElementById('stop-lng').value = pos.coords.longitude.toFixed(6);
    toast('Coordinates set from your location');
  }, () => toast('Could not get location', 'error'));
}

async function createStop() {
  const errEl = document.getElementById('stop-error');
  errEl.classList.add('hidden');

  const data = {
    name:      document.getElementById('stop-name').value.trim(),
    address:   document.getElementById('stop-address').value.trim(),
    latitude:  parseFloat(document.getElementById('stop-lat').value),
    longitude: parseFloat(document.getElementById('stop-lng').value),
  };

  if (!data.name) {
    errEl.textContent = 'Stop name is required.'; errEl.classList.remove('hidden'); return;
  }
  if (isNaN(data.latitude) || isNaN(data.longitude)) {
    errEl.textContent = 'Valid latitude and longitude are required.'; errEl.classList.remove('hidden'); return;
  }
  if (data.latitude < -90 || data.latitude > 90 || data.longitude < -180 || data.longitude > 180) {
    errEl.textContent = 'Coordinates out of range.'; errEl.classList.remove('hidden'); return;
  }

  try {
    await POST('/stops/', data);
    toast('Bus stop added!', 'success');
    toggleAddStopForm();
    // Clear form
    ['stop-name', 'stop-address', 'stop-lat', 'stop-lng'].forEach(id => {
      document.getElementById(id).value = '';
    });
    loadStops();
  } catch (err) {
    errEl.textContent = extractError(err); errEl.classList.remove('hidden');
  }
}

async function deleteStop(id, name) {
  if (!confirm(`Delete stop "${name}"?\n\nThis will also remove it from all routes.`)) return;
  try {
    await apiFetch('DELETE', `/stops/${id}/`);
    toast('Stop deleted.', 'warning');
    // Remove card from UI immediately
    const card = document.getElementById(`stop-card-${id}`);
    if (card) { card.style.opacity = '0'; card.style.transition = '0.3s'; setTimeout(loadStops, 350); }
  } catch (err) { toast(extractError(err), 'error'); }
}

function viewOnMap(lat, lng, name) {
  sessionStorage.setItem('mapTarget', JSON.stringify({ lat, lng, name }));
  window.location.href = '/map/';
}
