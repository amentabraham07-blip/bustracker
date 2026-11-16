/* ── APPROVALS PAGE ── */

document.addEventListener('DOMContentLoaded', async () => {
  const user = await initPage();
  if (!user) return;
  if (user.role !== 'admin') { window.location.href = '/dashboard/'; return; }
  loadApprovals();
});

async function loadApprovals() {
  const grid = document.getElementById('approvals-grid');
  try {
    const users = await GET('/admin/pending/');
    if (!users.length) {
      grid.innerHTML = emptyState('✅', 'No pending approvals — all caught up!');
      return;
    }
    const roleIcons = { driver: '🚌', police: '👮', operator: '🏢' };
    grid.innerHTML = users.map(u => `
      <div class="approval-card" id="approval-${u.id}">
        <div class="approval-header">
          <div>
            <div class="approval-name">${u.first_name} ${u.last_name}</div>
            <div class="approval-username">@${u.username}</div>
          </div>
          <span class="badge badge-medium">${roleIcons[u.role] || ''} ${u.role}</span>
        </div>
        <div class="approval-details">
          <div>📧 <strong>${u.email || '—'}</strong></div>
          <div>📱 <strong>${u.phone || '—'}</strong></div>
          ${u.license_number ? `<div>🪪 License: <strong>${u.license_number}</strong></div>` : ''}
          ${u.badge_number   ? `<div>🔷 Badge: <strong>${u.badge_number}</strong> · Station: ${u.station}</div>` : ''}
          ${u.operator_company ? `<div>🏢 Company: <strong>${u.operator_company}</strong> · ID: ${u.operator_id}</div>` : ''}
          <div>📅 Registered: <strong>${formatTime(u.created_at)}</strong></div>
        </div>
        <div class="approval-actions">
          <button class="btn-success" onclick="approveUser(${u.id})">✅ Approve</button>
          <button class="btn-danger"  onclick="rejectUser(${u.id})">✕ Reject</button>
        </div>
      </div>
    `).join('');
  } catch {
    grid.innerHTML = emptyState('⚠️', 'Failed to load pending approvals.');
  }
}

async function approveUser(id) {
  try {
    await POST(`/admin/approve/${id}/`);
    toast('User approved successfully!', 'success');
    // Remove card with animation
    const card = document.getElementById(`approval-${id}`);
    if (card) { card.style.opacity = '0'; card.style.transition = '0.3s'; setTimeout(() => loadApprovals(), 350); }
  } catch (err) { toast(extractError(err), 'error'); }
}

async function rejectUser(id) {
  if (!confirm('Reject this registration? The user will not be able to login.')) return;
  try {
    await POST(`/admin/reject/${id}/`);
    toast('Registration rejected.', 'warning');
    loadApprovals();
  } catch (err) { toast(extractError(err), 'error'); }
}
