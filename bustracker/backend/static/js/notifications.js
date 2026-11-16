/* ── NOTIFICATIONS PAGE ── */

document.addEventListener('DOMContentLoaded', async () => {
  await initPage();
  loadNotifications();
});

async function loadNotifications() {
  const list = document.getElementById('notifications-list');
  try {
    const notifs = await GET('/notifications/');

    // Update badge
    const badge = document.getElementById('notif-count');
    if (badge) {
      if (notifs.length > 0) { badge.textContent = notifs.length; badge.classList.remove('hidden'); }
      else badge.classList.add('hidden');
    }

    if (!notifs.length) {
      list.innerHTML = `<div class="card">${emptyState('🔔', 'No new notifications — you\'re all caught up!')}</div>`;
      return;
    }

    const icons = { traffic: '🚧', system: 'ℹ️', complaint: '📋', route: '🛣' };
    list.innerHTML = `
      <div class="card">
        ${notifs.map(n => `
          <div class="notif-item">
            <div class="notif-icon ${n.type}">${icons[n.type] || '🔔'}</div>
            <div style="flex:1;min-width:0;">
              <div class="notif-title">${n.title}</div>
              <div class="notif-msg">${n.message}</div>
              <div class="notif-time">${formatTime(n.created_at)}</div>
            </div>
          </div>
        `).join('')}
      </div>
    `;
  } catch {
    list.innerHTML = emptyState('🔔', 'Failed to load notifications.');
  }
}

async function markAllRead() {
  try {
    await POST('/notifications/read/');
    const badge = document.getElementById('notif-count');
    if (badge) badge.classList.add('hidden');
    toast('All notifications marked as read');
    loadNotifications();
  } catch (err) { toast(extractError(err), 'error'); }
}
