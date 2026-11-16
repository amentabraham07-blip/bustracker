/* ── BUSES PAGE ── */

let _currentUser = null;

document.addEventListener('DOMContentLoaded', async () => {
  _currentUser = await initPage();
  if (!_currentUser) return;

  if (_currentUser.role === 'operator' || _currentUser.role === 'admin' || _currentUser.is_superuser) {
    document.getElementById('buses-actions').innerHTML = `
      <button class="btn-primary" onclick="openAddBusForm()">+ Add Bus</button>
    `;
  }
  loadBuses();
});

async function loadBuses() {
  const container = document.getElementById('buses-table-container');
  container.innerHTML = '<div class="empty-state"><p>Loading...</p></div>';
  try {
    const buses = await GET('/buses/');
    if (!buses.length) {
      container.innerHTML = emptyState('🚌', 'No buses registered yet. Click "Add Bus" to get started.');
      return;
    }
    const canEdit = _currentUser.role === 'operator' || _currentUser.role === 'admin' || _currentUser.is_superuser;
    container.innerHTML = `
      <div class="table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th>Bus No.</th>
              <th>Registration</th>
              <th>Model</th>
              <th>Route</th>
              <th>Driver</th>
              <th>Status</th>
              <th>Cap.</th>
              ${canEdit ? '<th>Actions</th>' : ''}
            </tr>
          </thead>
          <tbody>
            ${buses.map(b => `
              <tr>
                <td><strong>${b.bus_number}</strong></td>
                <td style="font-family:var(--font-mono);font-size:0.82rem;">${b.registration_number}</td>
                <td>${b.model || '—'}</td>
                <td>
                  ${b.route_detail
                    ? `<span class="route-number" style="font-size:0.75rem;padding:2px 8px;">Route ${b.route_detail.route_number}</span>
                       <div style="font-size:0.78rem;color:var(--text-muted);margin-top:2px;">${b.route_detail.origin} → ${b.route_detail.destination}</div>`
                    : '<span style="color:var(--text-muted);font-size:0.82rem;">Not assigned</span>'}
                </td>
                <td>
                  ${b.driver_name
                    ? `<strong>${b.driver_name}</strong>`
                    : `<span style="color:var(--warning);font-size:0.82rem;">⚠ No driver</span>`}
                </td>
                <td><span class="badge badge-${b.status}">${b.status}</span></td>
                <td>${b.capacity}</td>
                ${canEdit ? `
                  <td>
                    <button class="btn-outline" style="font-size:0.8rem;padding:5px 10px;"
                      onclick="openAssignModal(${b.id}, '${b.bus_number}', ${b.driver || 'null'}, ${b.route || 'null'})">
                      ✏ Assign
                    </button>
                  </td>
                ` : ''}
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>
    `;
  } catch (e) {
    container.innerHTML = emptyState('🚌', 'Failed to load buses.');
  }
}

async function openAddBusForm() {
  document.getElementById('add-bus-form').classList.toggle('hidden');
  await populateDropdown('new-bus-route', '/routes/',
    r => ({ value: r.id, label: `Route ${r.route_number} — ${r.origin} → ${r.destination}` }),
    'No route assigned');
  await populateDriverDropdown('new-bus-driver');
}

async function populateDropdown(selectId, endpoint, mapper, emptyLabel) {
  try {
    const items = await GET(endpoint);
    const sel = document.getElementById(selectId);
    sel.innerHTML = `<option value="">${emptyLabel}</option>` +
      items.map(i => { const m = mapper(i); return `<option value="${m.value}">${m.label}</option>`; }).join('');
  } catch {}
}

async function populateDriverDropdown(selectId, selectedId) {
  try {
    const drivers = await GET('/admin/users/?role=driver');
    const sel = document.getElementById(selectId);
    sel.innerHTML = '<option value="">No driver assigned</option>' +
      drivers.filter(d => d.is_approved).map(d =>
        `<option value="${d.id}" ${d.id === selectedId ? 'selected' : ''}>
          ${d.first_name} ${d.last_name} (@${d.username})
        </option>`
      ).join('');
  } catch {}
}

async function createBus() {
  const data = {
    bus_number:          document.getElementById('new-bus-num').value.trim(),
    registration_number: document.getElementById('new-bus-reg').value.trim(),
    capacity:            parseInt(document.getElementById('new-bus-cap').value) || 50,
    model:               document.getElementById('new-bus-model').value.trim(),
    route:               document.getElementById('new-bus-route').value || null,
    driver:              document.getElementById('new-bus-driver').value || null,
  };
  if (!data.bus_number || !data.registration_number) {
    toast('Bus number and registration number are required', 'error'); return;
  }
  try {
    await POST('/buses/', data);
    toast('Bus added! Driver has been notified if assigned.', 'success');
    document.getElementById('add-bus-form').classList.add('hidden');
    ['new-bus-num','new-bus-reg','new-bus-model'].forEach(id => document.getElementById(id).value = '');
    document.getElementById('new-bus-cap').value = '50';
    loadBuses();
  } catch (err) { toast(extractError(err), 'error'); }
}

/* ── ASSIGN MODAL ───────────────────────────────────────── */

async function openAssignModal(busId, busNumber, currentDriverId, currentRouteId) {
  const content = document.getElementById('modal-content');
  content.innerHTML = `
    <h3 style="margin-bottom:4px;font-size:1.05rem;">✏ Assign Driver & Route</h3>
    <p style="color:var(--text-muted);font-size:0.85rem;margin-bottom:20px;">Bus: <strong style="color:var(--accent)">${busNumber}</strong></p>

    <div class="form-group">
      <label>Assign Driver</label>
      <select id="assign-driver-sel" class="form-input">
        <option value="">Loading...</option>
      </select>
      <p style="font-size:0.78rem;color:var(--text-muted);margin-top:4px;">Only approved drivers are listed. The assigned driver will be notified.</p>
    </div>

    <div class="form-group">
      <label>Assign Route</label>
      <select id="assign-route-sel" class="form-input">
        <option value="">Loading...</option>
      </select>
    </div>

    <div id="assign-error" class="form-error hidden"></div>
    <div class="form-actions" style="margin-top:16px;">
      <button class="btn-outline" onclick="closeModal()">Cancel</button>
      <button class="btn-primary" onclick="saveAssignment(${busId})">💾 Save Assignment</button>
    </div>
  `;
  document.getElementById('modal-overlay').classList.remove('hidden');

  // Load drivers
  try {
    const drivers = await GET('/admin/users/?role=driver');
    const sel = document.getElementById('assign-driver-sel');
    sel.innerHTML = '<option value="">— No driver —</option>' +
      drivers.filter(d => d.is_approved).map(d =>
        `<option value="${d.id}" ${d.id === currentDriverId ? 'selected' : ''}>
          ${d.first_name} ${d.last_name} (@${d.username})
        </option>`
      ).join('');
    if (!drivers.filter(d => d.is_approved).length) {
      sel.innerHTML = '<option value="">No approved drivers available</option>';
    }
  } catch {
    document.getElementById('assign-driver-sel').innerHTML = '<option value="">Could not load drivers</option>';
  }

  // Load routes
  try {
    const routes = await GET('/routes/');
    const sel = document.getElementById('assign-route-sel');
    sel.innerHTML = '<option value="">— No route —</option>' +
      routes.map(r =>
        `<option value="${r.id}" ${r.id === currentRouteId ? 'selected' : ''}>
          Route ${r.route_number} — ${r.origin} → ${r.destination}
        </option>`
      ).join('');
  } catch {
    document.getElementById('assign-route-sel').innerHTML = '<option value="">Could not load routes</option>';
  }
}

async function saveAssignment(busId) {
  const driverVal = document.getElementById('assign-driver-sel').value;
  const routeVal  = document.getElementById('assign-route-sel').value;
  const errEl     = document.getElementById('assign-error');
  errEl.classList.add('hidden');
  try {
    await PATCH(`/buses/${busId}/assign/`, {
      driver_id: driverVal ? parseInt(driverVal) : '',
      route_id:  routeVal  ? parseInt(routeVal)  : '',
    });
    closeModal();
    toast('Assignment saved! Driver will be notified.', 'success');
    loadBuses();
  } catch (err) {
    errEl.textContent = extractError(err);
    errEl.classList.remove('hidden');
  }
}
