/* ── DASHBOARD PAGE ── */

let _miniMap = null;
let _miniMarkers = {};

document.addEventListener('DOMContentLoaded', async () => {
  const user = await initPage();
  if (!user) return;

  document.getElementById('dash-welcome').textContent = `Welcome back, ${user.first_name || user.username}!`;

  await loadStats(user);
  initMiniMap();
  loadRecentActivity(user);

  // Refresh map markers every 10s
  setInterval(() => refreshMiniMarkers(), 10000);
});

async function loadStats(user) {
  const grid = document.getElementById('stats-grid');
  let stats = [];
  const role = (user.is_superuser || user.role === 'admin') ? 'admin' : user.role;

  try {
    if (role === 'admin') {
      const d = await GET('/admin/stats/');
      stats = [
        { label:'Passengers',        value: d.total_users,        icon:'👤' },
        { label:'Active Buses',      value: d.active_buses,       icon:'🚌', type:'accent' },
        { label:'Routes',            value: d.total_routes,       icon:'🛣' },
        { label:'Pending Approvals', value: d.pending_approvals,  icon:'⏳', type: d.pending_approvals > 0 ? 'warning' : '' },
        { label:'Traffic Blocks',    value: d.active_blocks,      icon:'🚧', type: d.active_blocks > 0 ? 'danger' : '' },
        { label:'Open Complaints',   value: d.pending_complaints, icon:'📋', type:'info' },
      ];
    } else if (role === 'operator') {
      const d = await GET('/operator/dashboard/');
      stats = [
        { label:'My Buses',    value: d.total_buses,    icon:'🚌' },
        { label:'Active Now',  value: d.active_buses,   icon:'🟢', type:'accent' },
        { label:'Routes',      value: d.total_routes,   icon:'🛣' },
        { label:'Avg Rating',  value: (d.average_rating || 0) + '★', icon:'⭐', type:'warning' },
      ];
    } else if (role === 'driver') {
      const d = await GET('/driver/info/');
      const bus = d.assigned_bus;
      stats = [
        { label:'My Bus',          value: bus ? bus.bus_number : 'N/A', icon:'🚌' },
        { label:'Route',           value: bus?.route_detail?.route_number || 'N/A', icon:'🛣' },
        { label:'Traffic Blocks',  value: d.active_traffic_blocks.length, icon:'🚧', type: d.active_traffic_blocks.length > 0 ? 'danger' : '' },
      ];
    } else {
      const [buses, routes, blocks] = await Promise.all([
        GET('/buses/active/'), GET('/routes/'), GET('/traffic-blocks/'),
      ]);
      stats = [
        { label:'Active Buses',   value: buses.length,  icon:'🚌', type:'accent' },
        { label:'Routes',         value: routes.length, icon:'🛣' },
        { label:'Traffic Blocks', value: blocks.length, icon:'🚧', type: blocks.length > 0 ? 'danger' : '' },
      ];
    }
  } catch (e) { console.error(e); }

  grid.innerHTML = stats.map(s => `
    <div class="stat-card ${s.type || ''}">
      <div class="stat-icon">${s.icon}</div>
      <div class="stat-value">${s.value}</div>
      <div class="stat-label">${s.label}</div>
    </div>
  `).join('');
}

function initMiniMap() {
  const el = document.getElementById('mini-map');
  if (!el) return;
  _miniMap = L.map('mini-map', { zoomControl: false, attributionControl: false }).setView([11.2588, 75.7804], 12);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(_miniMap);
  refreshMiniMarkers();
}

async function refreshMiniMarkers() {
  if (!_miniMap) return;
  try {
    const buses = await GET('/location/buses/');
    Object.values(_miniMarkers).forEach(m => _miniMap.removeLayer(m));
    _miniMarkers = {};
    buses.forEach(bus => {
      const icon = L.divIcon({
        className: '',
        html: `<div class="bus-marker-icon">🚌</div>`,
        iconSize: [28, 28], iconAnchor: [14, 14],
      });
      _miniMarkers[bus.bus_id] = L.marker([bus.latitude, bus.longitude], { icon })
        .addTo(_miniMap)
        .bindPopup(`<strong>${bus.bus_number}</strong><br>${bus.route_name || 'N/A'}`);
    });
  } catch {}
}

async function loadRecentActivity(user) {
  const el = document.getElementById('recent-activity');
  const items = [];
  try {
    const blocks = await GET('/traffic-blocks/');
    blocks.slice(0, 3).forEach(b => items.push({
      text: `Traffic block: ${b.title}`,
      time: formatTime(b.created_at),
      color: 'var(--danger)',
    }));
  } catch {}
  try {
    if (user.role === 'admin') {
      const complaints = await GET('/complaints/');
      complaints.slice(0, 2).forEach(c => items.push({
        text: `Complaint: ${c.subject}`,
        time: formatTime(c.created_at),
        color: 'var(--warning)',
      }));
    }
  } catch {}

  if (!items.length) {
    el.innerHTML = emptyState('📋', 'No recent activity');
    return;
  }
  el.innerHTML = items.map(i => `
    <div class="activity-item">
      <div class="activity-dot" style="background:${i.color}"></div>
      <div>
        <div class="activity-text">${i.text}</div>
        <div class="activity-time">${i.time}</div>
      </div>
    </div>
  `).join('');
}
