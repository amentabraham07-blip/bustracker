/* ── DRIVER PAGE ── */

let _tracking = false;
let _locationInterval = null;

document.addEventListener('DOMContentLoaded', async () => {
  const user = await initPage();
  if (!user) return;
  if (user.role !== 'driver' && user.role !== 'admin') {
    window.location.href = '/dashboard/'; return;
  }
  loadDriverInfo();
});

async function loadDriverInfo() {
  try {
    const info = await GET('/driver/info/');
    renderBusInfo(info.assigned_bus);
    renderBlocks(info.active_traffic_blocks);
  } catch (e) { console.error(e); }
}

function renderBusInfo(bus) {
  const el = document.getElementById('driver-bus-info');
  if (!bus) {
    el.innerHTML = emptyState('🚌', 'No bus assigned. Contact your operator.');
    return;
  }
  el.innerHTML = `
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;font-size:0.88rem;">
      <div><span style="color:var(--text-muted);font-size:0.75rem;text-transform:uppercase;letter-spacing:.5px">Bus No.</span><br>
        <strong style="color:var(--accent);font-size:1.2rem;">${bus.bus_number}</strong></div>
      <div><span style="color:var(--text-muted);font-size:0.75rem;text-transform:uppercase;letter-spacing:.5px">Status</span><br>
        <span class="badge badge-${bus.status}">${bus.status}</span></div>
      <div><span style="color:var(--text-muted);font-size:0.75rem;text-transform:uppercase;letter-spacing:.5px">Route</span><br>
        <strong>${bus.route_detail ? `Route ${bus.route_detail.route_number} — ${bus.route_detail.origin} → ${bus.route_detail.destination}` : 'Not assigned'}</strong></div>
      <div><span style="color:var(--text-muted);font-size:0.75rem;text-transform:uppercase;letter-spacing:.5px">Capacity</span><br>
        <strong>${bus.capacity} seats</strong></div>
      <div><span style="color:var(--text-muted);font-size:0.75rem;text-transform:uppercase;letter-spacing:.5px">Model</span><br>
        <strong>${bus.model || '—'}</strong></div>
      <div><span style="color:var(--text-muted);font-size:0.75rem;text-transform:uppercase;letter-spacing:.5px">Registration</span><br>
        <strong style="font-family:var(--font-mono);font-size:0.82rem;">${bus.registration_number}</strong></div>
    </div>
  `;
}

function renderBlocks(blocks) {
  const el = document.getElementById('driver-blocks');
  if (!blocks.length) {
    el.innerHTML = '<div style="padding:20px;text-align:center;color:var(--success)">✅ No active traffic blocks on your route</div>';
    return;
  }
  el.innerHTML = blocks.map(b => `
    <div class="block-card severity-${b.severity}" style="margin-bottom:12px;">
      <div class="block-title">⚠️ ${b.title}</div>
      <div class="block-desc">${b.description}</div>
      <div class="block-meta">
        <span class="badge badge-${b.severity}">${b.severity.toUpperCase()}</span>
        <span style="font-size:0.8rem;color:var(--text-muted)">📍 ${b.latitude.toFixed(4)}, ${b.longitude.toFixed(4)}</span>
        <span style="font-size:0.8rem;color:var(--text-muted)">${formatTime(b.created_at)}</span>
      </div>
    </div>
  `).join('');
}

function toggleDriverTracking() {
  if (_tracking) stopTracking(); else startTracking();
}

function startTracking() {
  if (!navigator.geolocation) { toast('Geolocation not supported', 'error'); return; }
  _tracking = true;
  const btn = document.getElementById('tracking-toggle');
  btn.textContent = 'Stop Tracking';
  btn.style.background = 'var(--danger)';
  document.getElementById('driver-status-badge').textContent = 'Online';
  document.getElementById('driver-status-badge').className = 'status-badge online';
  toast('Tracking started — location shared every 10 seconds', 'success');

  const send = () => {
    navigator.geolocation.getCurrentPosition(async pos => {
      const { latitude, longitude, speed, heading } = pos.coords;
      document.getElementById('driver-lat').textContent = latitude.toFixed(6);
      document.getElementById('driver-lng').textContent = longitude.toFixed(6);
      document.getElementById('driver-speed').textContent = speed ? (speed * 3.6).toFixed(1) : '0';
      document.getElementById('driver-last-update').textContent = new Date().toLocaleTimeString();
      try {
        await POST('/location/update/', {
          latitude, longitude,
          speed:   speed ? speed * 3.6 : 0,
          heading: heading || 0,
        });
      } catch (e) { console.warn('Location update failed:', e); }
    }, err => console.warn('GPS error:', err), { enableHighAccuracy: true });
  };

  send();
  _locationInterval = setInterval(send, 10000);
}

function stopTracking() {
  _tracking = false;
  clearInterval(_locationInterval);
  const btn = document.getElementById('tracking-toggle');
  btn.textContent = 'Start Tracking';
  btn.style.background = '';
  document.getElementById('driver-status-badge').textContent = 'Offline';
  document.getElementById('driver-status-badge').className = 'status-badge offline';
  toast('Tracking stopped');
}

// Stop tracking if user navigates away
window.addEventListener('beforeunload', () => { if (_tracking) stopTracking(); });
