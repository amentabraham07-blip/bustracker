/* ── COMPLAINTS PAGE ── */

document.addEventListener('DOMContentLoaded', async () => {
  const user = await initPage();
  if (!user) return;

  // Admin and police only view complaints
  if (user.role === 'admin' || user.role === 'police') {
    document.getElementById('complaint-form-card').classList.add('hidden');
  } else {
    populateBusDropdown();
  }
  loadComplaints(user);
});

async function populateBusDropdown() {
  try {
    const buses = await GET('/buses/');
    const sel = document.getElementById('comp-bus');
    sel.innerHTML = '<option value="">Select bus (optional)</option>' +
      buses.map(b => `<option value="${b.id}">${b.bus_number}</option>`).join('');
  } catch {}
}

async function loadComplaints(user) {
  if (!user) user = JSON.parse(localStorage.getItem('bt_user') || '{}');
  const list = document.getElementById('complaints-list');
  try {
    const complaints = await GET('/complaints/');
    if (!complaints.length) {
      list.innerHTML = emptyState('📋', 'No complaints found.');
      return;
    }
    list.innerHTML = complaints.map(c => `
      <div class="complaint-item">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:12px;flex-wrap:wrap;">
          <div>
            <strong style="color:var(--text-primary);font-size:0.95rem;">${c.subject}</strong>
            <div class="feedback-meta">
              <span>👤 ${c.user_name}</span>
              <span>📤 To: ${c.target}</span>
              <span>${formatTime(c.created_at)}</span>
            </div>
          </div>
          <div style="display:flex;align-items:center;gap:8px;flex-shrink:0;">
            <span class="badge badge-${c.status}">${c.status}</span>
            ${user.role === 'admin' ? `
              <select onchange="updateComplaintStatus(${c.id}, this.value)"
                class="form-input compact" style="font-size:0.8rem;padding:4px 8px;min-width:110px;">
                <option value="">Update...</option>
                <option value="reviewed">Reviewed</option>
                <option value="resolved">Resolved</option>
                <option value="rejected">Rejected</option>
              </select>
            ` : ''}
          </div>
        </div>
        <div class="feedback-msg" style="margin-top:8px;">${c.description}</div>
        ${c.admin_response ? `
          <div style="margin-top:10px;padding:10px 12px;background:var(--bg-elevated);border-radius:var(--radius-sm);font-size:0.83rem;color:var(--info);border-left:3px solid var(--info);">
            📝 Response: ${c.admin_response}
          </div>
        ` : ''}
      </div>
    `).join('');
  } catch {
    list.innerHTML = emptyState('📋', 'Failed to load complaints.');
  }
}

async function updateComplaintStatus(id, status) {
  if (!status) return;
  const response = prompt('Add a response to the complainant (optional):') || '';
  try {
    await PATCH(`/complaints/${id}/update/`, { status, admin_response: response });
    toast('Complaint updated!', 'success');
    const user = JSON.parse(localStorage.getItem('bt_user') || '{}');
    loadComplaints(user);
  } catch (err) { toast(extractError(err), 'error'); }
}

async function submitComplaint() {
  const subject = document.getElementById('comp-subject').value.trim();
  const desc    = document.getElementById('comp-desc').value.trim();
  if (!subject || !desc) { toast('Subject and description are required', 'error'); return; }

  const data = {
    subject,
    description: desc,
    target: document.getElementById('comp-target').value,
    bus:    document.getElementById('comp-bus').value || null,
  };
  try {
    await POST('/complaints/', data);
    toast('Complaint submitted successfully!', 'success');
    document.getElementById('comp-subject').value = '';
    document.getElementById('comp-desc').value    = '';
    const user = JSON.parse(localStorage.getItem('bt_user') || '{}');
    loadComplaints(user);
  } catch (err) { toast(extractError(err), 'error'); }
}
