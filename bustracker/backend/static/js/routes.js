/* ── ROUTES PAGE ── */

let _currentUser = null;
let _managingRouteId = null;
let _managingRouteName = null;

document.addEventListener('DOMContentLoaded', async () => {
  _currentUser = await initPage();
  if (!_currentUser) return;

  if (_currentUser.role === 'operator' || _currentUser.role === 'admin' || _currentUser.is_superuser) {
    document.getElementById('routes-actions').innerHTML = `
      <button class="btn-primary" onclick="document.getElementById('add-route-form').classList.toggle('hidden')">
        + Add Route
      </button>
    `;
  }
  loadRoutes();
});

async function loadRoutes() {
  const grid = document.getElementById('routes-grid');
  grid.innerHTML = '<div class="empty-state"><p>Loading...</p></div>';
  try {
    const routes = await GET('/routes/');
    if (!routes.length) {
      grid.innerHTML = emptyState('🛣', 'No routes yet. Add one above.');
      return;
    }

    const canManage = _currentUser.role === 'operator' ||
                      _currentUser.role === 'admin' ||
                      _currentUser.is_superuser;

    grid.innerHTML = routes.map(r => `
      <div class="route-card">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:10px;">
          <span class="route-number">Route ${r.route_number}</span>
          <span class="badge badge-${r.is_active ? 'active' : 'inactive'}">${r.is_active ? 'Active' : 'Inactive'}</span>
        </div>

        <div class="route-path">
          <span>${r.origin}</span>
          <span class="route-arrow">→</span>
          <span>${r.destination}</span>
        </div>

        <div style="font-size:0.82rem;color:var(--text-muted);margin-top:4px;">${r.name}</div>

        ${r.operator_name ? `
          <div style="font-size:0.78rem;color:var(--text-muted);margin-top:4px;">
            🏢 ${r.operator_name}
          </div>
        ` : ''}

        <!-- Stops summary -->
        <div style="margin-top:12px;">
          ${r.stops_detail && r.stops_detail.length
            ? `<div style="font-size:0.8rem;color:var(--text-secondary);">
                <strong style="color:var(--text-muted);font-size:0.75rem;text-transform:uppercase;letter-spacing:.5px;">
                  ${r.stops_detail.length} Stop${r.stops_detail.length !== 1 ? 's' : ''}
                </strong>
                <div style="margin-top:5px;display:flex;flex-wrap:wrap;gap:4px;">
                  ${r.stops_detail.map(s => `
                    <span style="background:var(--bg-elevated);border:1px solid var(--border);
                      border-radius:20px;padding:2px 8px;font-size:0.75rem;color:var(--text-secondary);">
                      ${s.order}. ${s.stop.name}
                    </span>
                  `).join('')}
                </div>
              </div>`
            : `<div style="font-size:0.8rem;color:var(--warning);">⚠ No stops assigned yet</div>`
          }
        </div>

        ${canManage ? `
          <div style="margin-top:14px;padding-top:12px;border-top:1px solid var(--border);">
            <button class="btn-outline" style="font-size:0.82rem;padding:6px 12px;width:100%;"
              onclick="openManageStops(${r.id}, 'Route ${r.route_number} — ${r.origin} → ${r.destination}')">
              📍 Manage Stops
            </button>
          </div>
        ` : ''}
      </div>
    `).join('');
  } catch (e) {
    grid.innerHTML = emptyState('🛣', 'Failed to load routes.');
    console.error(e);
  }
}

async function createRoute() {
  const data = {
    route_number: document.getElementById('new-route-num').value.trim(),
    name:         document.getElementById('new-route-name').value.trim(),
    origin:       document.getElementById('new-route-origin').value.trim(),
    destination:  document.getElementById('new-route-dest').value.trim(),
  };
  if (!data.route_number || !data.origin || !data.destination) {
    toast('Route number, origin and destination are required', 'error'); return;
  }
  if (!data.name) data.name = `Route ${data.route_number}`;
  try {
    await POST('/routes/', data);
    toast('Route created!', 'success');
    document.getElementById('add-route-form').classList.add('hidden');
    ['new-route-num','new-route-name','new-route-origin','new-route-dest'].forEach(id => {
      document.getElementById(id).value = '';
    });
    loadRoutes();
  } catch (err) { toast(extractError(err), 'error'); }
}

/* ── MANAGE STOPS ────────────────────────────────────────── */

async function openManageStops(routeId, routeLabel) {
  _managingRouteId = routeId;
  _managingRouteName = routeLabel;

  document.getElementById('manage-route-label').textContent = routeLabel;
  document.getElementById('manage-stops-panel').classList.remove('hidden');

  // Scroll to panel
  document.getElementById('manage-stops-panel').scrollIntoView({ behavior: 'smooth', block: 'start' });

  // Load current stops + all available stops
  await Promise.all([
    loadRouteCurrentStops(routeId),
    loadAllStopsDropdown(routeId),
  ]);
}

function closeManageStops() {
  document.getElementById('manage-stops-panel').classList.add('hidden');
  _managingRouteId = null;
  _managingRouteName = null;
}

async function loadRouteCurrentStops(routeId) {
  const el = document.getElementById('route-stops-list');
  el.innerHTML = '<p style="color:var(--text-muted);font-size:0.85rem;">Loading...</p>';
  try {
    const route = await GET(`/routes/${routeId}/`);
    const stops = route.stops_detail || [];

    if (!stops.length) {
      el.innerHTML = `
        <div style="padding:16px;background:var(--bg-elevated);border-radius:var(--radius-sm);
          text-align:center;color:var(--warning);font-size:0.85rem;">
          ⚠ No stops added to this route yet. Use the form below to add stops.
        </div>
      `;
      return;
    }

    el.innerHTML = `
      <div class="table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th style="width:50px;">#</th>
              <th>Stop Name</th>
              <th>Est. Time from Prev.</th>
              <th>Coordinates</th>
              <th style="width:80px;">Remove</th>
            </tr>
          </thead>
          <tbody>
            ${stops.map(s => `
              <tr>
                <td><strong style="color:var(--accent);">${s.order}</strong></td>
                <td>
                  <strong>${s.stop.name}</strong>
                  ${s.stop.address ? `<div style="font-size:0.78rem;color:var(--text-muted);">${s.stop.address}</div>` : ''}
                </td>
                <td style="color:var(--text-secondary);font-size:0.82rem;">${s.estimated_time || '—'}</td>
                <td style="font-family:var(--font-mono);font-size:0.75rem;color:var(--text-muted);">
                  ${s.stop.latitude.toFixed(4)}, ${s.stop.longitude.toFixed(4)}
                </td>
                <td>
                  <button class="btn-danger" style="padding:4px 8px;font-size:0.75rem;"
                    onclick="removeStopFromRoute(${routeId}, ${s.stop.id}, '${s.stop.name.replace(/'/g, "\\'")}')">
                    ✕
                  </button>
                </td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>
    `;
  } catch (e) {
    el.innerHTML = '<p style="color:var(--danger);font-size:0.85rem;">Failed to load stops.</p>';
  }
}

async function loadAllStopsDropdown(routeId) {
  const sel = document.getElementById('add-stop-select');
  sel.innerHTML = '<option value="">Loading available stops...</option>';
  try {
    // Get all stops and current route stops
    const [allStops, route] = await Promise.all([
      GET('/stops/'),
      GET(`/routes/${routeId}/`),
    ]);

    const alreadyIn = new Set((route.stops_detail || []).map(s => s.stop.id));
    const available = allStops.filter(s => !alreadyIn.has(s.id));

    if (!available.length) {
      sel.innerHTML = '<option value="">All stops already added to this route</option>';
      return;
    }

    sel.innerHTML = '<option value="">— Select a stop to add —</option>' +
      available.map(s =>
        `<option value="${s.id}">${s.name}${s.address ? ' — ' + s.address : ''}</option>`
      ).join('');

    // Auto-suggest next order number
    const nextOrder = (route.stops_detail || []).length + 1;
    document.getElementById('add-stop-order').value = nextOrder;

  } catch {
    sel.innerHTML = '<option value="">Could not load stops</option>';
  }
}

async function addStopToRoute() {
  if (!_managingRouteId) return;

  const stopId        = document.getElementById('add-stop-select').value;
  const order         = parseInt(document.getElementById('add-stop-order').value) || 1;
  const estimatedTime = document.getElementById('add-stop-time').value.trim();

  if (!stopId) { toast('Please select a stop', 'error'); return; }

  try {
    const res = await POST(`/routes/${_managingRouteId}/add-stop/`, {
      stop_id: parseInt(stopId),
      order,
      estimated_time: estimatedTime,
    });
    toast(res.message || 'Stop added to route!', 'success');
    document.getElementById('add-stop-time').value = '';
    // Reload the stops list and dropdown
    await Promise.all([
      loadRouteCurrentStops(_managingRouteId),
      loadAllStopsDropdown(_managingRouteId),
    ]);
    // Also refresh route cards
    loadRoutes();
  } catch (err) { toast(extractError(err), 'error'); }
}

async function removeStopFromRoute(routeId, stopId, stopName) {
  if (!confirm(`Remove "${stopName}" from this route?`)) return;
  try {
    await apiFetch('DELETE', `/routes/${routeId}/remove-stop/${stopId}/`);
    toast('Stop removed from route.', 'warning');
    await Promise.all([
      loadRouteCurrentStops(routeId),
      loadAllStopsDropdown(routeId),
    ]);
    loadRoutes();
  } catch (err) { toast(extractError(err), 'error'); }
}
