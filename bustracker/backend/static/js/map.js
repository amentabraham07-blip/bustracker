/* ── MAP PAGE ── */

let _map = null;
let _busMarkers = {};
let _stopMarkers = [];
let _blockCircles = [];
let _showStops = false;
let _showBlocks = true;
let _busFilter = 'all';
let _refreshTimer = null;

document.addEventListener('DOMContentLoaded', async () => {
  const user = await initPage();
  if (!user) return;
  window._currentUser = user;
  initMap(user);
});

function initMap(user) {
  _map = L.map('main-map').setView([11.2588, 75.7804], 13);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© <a href="https://openstreetmap.org">OpenStreetMap</a> contributors',
    maxZoom: 19,
  }).addTo(_map);

  // Police/admin can click map to set block coordinates
  if (user.role === 'police' || user.role === 'admin') {
    _map.on('click', e => {
      const lat = document.getElementById('block-lat');
      const lng = document.getElementById('block-lng');
      if (lat && lng) {
        lat.value = e.latlng.lat.toFixed(6);
        lng.value = e.latlng.lng.toFixed(6);
        toast('Location set from map click');
      }
    });
  }

  loadBusMarkers();
  loadBlockCircles();

  // Auto-refresh every 10s
  _refreshTimer = setInterval(() => {
    loadBusMarkers();
    if (_showBlocks) loadBlockCircles();
  }, 10000);
}

async function loadBusMarkers() {
  if (!_map) return;
  try {
    const buses = await GET('/location/buses/');
    Object.values(_busMarkers).forEach(m => _map.removeLayer(m));
    _busMarkers = {};
    buses.forEach(bus => {
      if (_busFilter === 'active' && bus.status === 'inactive') return;
      const icon = L.divIcon({
        className: '',
        html: `<div class="bus-marker-icon" title="Bus ${bus.bus_number}">🚌</div>`,
        iconSize: [28, 28], iconAnchor: [14, 14],
      });
      const marker = L.marker([bus.latitude, bus.longitude], { icon }).addTo(_map);
      marker.bindPopup(`
        <strong>🚌 ${bus.bus_number}</strong><br>
        <span style="color:#8899bb">Route:</span> ${bus.route_name || 'Unassigned'}<br>
        <span style="color:#8899bb">Speed:</span> ${bus.speed || 0} km/h<br>
        <small style="color:#556688">Updated ${formatTime(bus.last_updated)}</small><br>
        <button onclick="showBusInfo(${bus.bus_id})"
          style="margin-top:8px;padding:4px 12px;background:#00d4aa;color:#0a0e1a;border:none;border-radius:6px;cursor:pointer;font-size:12px;font-weight:600;">
          View Details
        </button>
      `);
      _busMarkers[bus.bus_id] = marker;
    });
  } catch (e) { console.error('Bus markers error:', e); }
}

async function loadStopMarkers() {
  if (!_map) return;
  _stopMarkers.forEach(m => _map.removeLayer(m));
  _stopMarkers = [];
  try {
    const stops = await GET('/stops/');
    stops.forEach(s => {
      const icon = L.divIcon({
        className: '',
        html: `<div style="background:#60a5fa;border:2px solid #0a0e1a;border-radius:50%;width:14px;height:14px;box-shadow:0 0 6px rgba(96,165,250,0.7)"></div>`,
        iconSize: [14, 14], iconAnchor: [7, 7],
      });
      const m = L.marker([s.latitude, s.longitude], { icon })
        .addTo(_map)
        .bindPopup(`<strong>📍 ${s.name}</strong>${s.address ? `<br><small>${s.address}</small>` : ''}`);
      _stopMarkers.push(m);
    });
  } catch {}
}

async function loadBlockCircles() {
  if (!_map) return;
  _blockCircles.forEach(c => _map.removeLayer(c));
  _blockCircles = [];
  try {
    const blocks = await GET('/traffic-blocks/');
    const colors = { critical: '#ff4d6d', high: '#ffb347', medium: '#60a5fa', low: '#4ade80' };
    blocks.forEach(b => {
      const color = colors[b.severity] || '#ffb347';
      const circle = L.circle([b.latitude, b.longitude], {
        radius: b.radius,
        color, fillColor: color, fillOpacity: 0.15, weight: 2,
      }).addTo(_map).bindPopup(`
        <strong>⚠️ ${b.title}</strong><br>
        <span style="color:#8899bb">Severity:</span> ${b.severity.toUpperCase()}<br>
        ${b.description}<br>
        <small style="color:#556688">By ${b.officer_name}</small>
      `);
      _blockCircles.push(circle);
    });
  } catch {}
}

function filterMapBuses(filter) {
  _busFilter = filter;
  document.getElementById('btn-all').classList.toggle('active', filter === 'all');
  document.getElementById('btn-active').classList.toggle('active', filter === 'active');
  loadBusMarkers();
}

function toggleStops() {
  _showStops = !_showStops;
  document.getElementById('btn-stops').classList.toggle('active', _showStops);
  if (_showStops) {
    loadStopMarkers();
  } else {
    _stopMarkers.forEach(m => _map.removeLayer(m));
    _stopMarkers = [];
  }
}

function toggleBlocks() {
  _showBlocks = !_showBlocks;
  document.getElementById('btn-blocks').classList.toggle('active', _showBlocks);
  if (_showBlocks) {
    loadBlockCircles();
  } else {
    _blockCircles.forEach(c => _map.removeLayer(c));
    _blockCircles = [];
  }
}

async function refreshMap() {
  await loadBusMarkers();
  if (_showStops) await loadStopMarkers();
  if (_showBlocks) await loadBlockCircles();
  toast('Map refreshed');
}

async function showBusInfo(busId) {
  try {
    const bus = await GET(`/buses/${busId}/`);
    const loc = await GET(`/location/bus/${busId}/`).catch(() => null);
    const panel = document.getElementById('bus-info-panel');
    document.getElementById('bus-info-content').innerHTML = `
      <h3 style="margin-bottom:14px;font-size:1.1rem;">🚌 Bus ${bus.bus_number}</h3>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;font-size:0.88rem;">
        <div><span style="color:var(--text-muted);font-size:0.75rem;text-transform:uppercase;letter-spacing:.5px">Registration</span><br><strong>${bus.registration_number}</strong></div>
        <div><span style="color:var(--text-muted);font-size:0.75rem;text-transform:uppercase;letter-spacing:.5px">Status</span><br><span class="badge badge-${bus.status}">${bus.status}</span></div>
        <div><span style="color:var(--text-muted);font-size:0.75rem;text-transform:uppercase;letter-spacing:.5px">Route</span><br><strong>${bus.route_detail ? `Route ${bus.route_detail.route_number} — ${bus.route_detail.name}` : 'Not assigned'}</strong></div>
        <div><span style="color:var(--text-muted);font-size:0.75rem;text-transform:uppercase;letter-spacing:.5px">Driver</span><br><strong>${bus.driver_name || 'Unassigned'}</strong></div>
        <div><span style="color:var(--text-muted);font-size:0.75rem;text-transform:uppercase;letter-spacing:.5px">Capacity</span><br><strong>${bus.capacity} seats</strong></div>
        ${loc ? `<div><span style="color:var(--text-muted);font-size:0.75rem;text-transform:uppercase;letter-spacing:.5px">Speed</span><br><strong>${loc.speed} km/h</strong></div>` : ''}
      </div>
      ${loc ? `<div style="margin-top:12px;font-family:var(--font-mono);font-size:0.78rem;color:var(--text-muted)">📍 ${loc.latitude.toFixed(6)}, ${loc.longitude.toFixed(6)}<br>🕐 ${formatTime(loc.timestamp)}</div>` : ''}
    `;
    panel.classList.remove('hidden');
  } catch (e) { toast('Could not load bus details', 'error'); }
}

function closeBusInfo() {
  document.getElementById('bus-info-panel').classList.add('hidden');
}
