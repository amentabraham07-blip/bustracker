/* ── USERS PAGE ── */

document.addEventListener('DOMContentLoaded', async () => {
  const user = await initPage();
  if (!user) return;
  if (user.role !== 'admin') { window.location.href = '/dashboard/'; return; }
  loadUsers();
});

async function loadUsers() {
  const role = document.getElementById('user-role-filter')?.value || '';
  const container = document.getElementById('users-table-container');
  container.innerHTML = '<div class="empty-state"><p>Loading...</p></div>';
  try {
    const users = await GET(`/admin/users/${role ? '?role=' + role : ''}`);
    if (!users.length) {
      container.innerHTML = emptyState('👥', 'No users found.');
      return;
    }
    const roleColors = { admin:'info', user:'active', driver:'medium', police:'warning', operator:'low' };
    container.innerHTML = `
      <div class="table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Username</th>
              <th>Role</th>
              <th>Email</th>
              <th>Phone</th>
              <th>Approval</th>
              <th>Joined</th>
            </tr>
          </thead>
          <tbody>
            ${users.map(u => `
              <tr>
                <td><strong>${u.first_name} ${u.last_name}</strong></td>
                <td style="font-family:var(--font-mono);font-size:0.82rem;color:var(--text-secondary);">@${u.username}</td>
                <td><span class="badge badge-${roleColors[u.role] || 'active'}">${u.role}</span></td>
                <td style="font-size:0.85rem;">${u.email || '—'}</td>
                <td>${u.phone || '—'}</td>
                <td>
                  <span class="badge badge-${u.is_approved ? 'active' : 'pending'}">
                    ${u.is_approved ? 'Approved' : 'Pending'}
                  </span>
                </td>
                <td style="font-size:0.8rem;color:var(--text-muted);">${formatTime(u.created_at)}</td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>
    `;
  } catch {
    container.innerHTML = emptyState('👥', 'Failed to load users.');
  }
}
