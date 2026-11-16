/* ── BUSTRACK AUTH ── */

const NAV_ITEMS = {
  admin: [
    { href:'/dashboard/', label:'Dashboard',      icon:'⊞' },
    { href:'/map/',        label:'Live Map',       icon:'🗺' },
    { href:'/approvals/',  label:'Approvals',      icon:'✅' },
    { href:'/users/',      label:'Users',          icon:'👥' },
    { href:'/buses/',      label:'Buses',          icon:'🚌' },
    { href:'/routes/',     label:'Routes',         icon:'🛣' },
    { href:'/stops/',      label:'Bus Stops',      icon:'📍' },
    { href:'/traffic/',    label:'Traffic Blocks', icon:'🚧' },
    { href:'/complaints/', label:'Complaints',     icon:'📋' },
    { href:'/feedback/',   label:'Feedback',       icon:'⭐' },
    { href:'/notifications/', label:'Notifications', icon:'🔔' },
  ],
  user: [
    { href:'/dashboard/', label:'Dashboard',  icon:'⊞' },
    { href:'/map/',        label:'Live Map',   icon:'🗺' },
    { href:'/stops/',      label:'Bus Stops',  icon:'📍' },
    { href:'/routes/',     label:'Routes',     icon:'🛣' },
    { href:'/feedback/',   label:'Feedback',   icon:'⭐' },
    { href:'/complaints/', label:'Complaints', icon:'📋' },
    { href:'/notifications/', label:'Notifications', icon:'🔔' },
  ],
  driver: [
    { href:'/dashboard/', label:'Dashboard',    icon:'⊞' },
    { href:'/driver/',     label:'My Tracking',  icon:'📡' },
    { href:'/map/',        label:'Live Map',     icon:'🗺' },
    { href:'/traffic/',    label:'Traffic Alerts', icon:'🚧' },
    { href:'/notifications/', label:'Notifications', icon:'🔔' },
  ],
  police: [
    { href:'/dashboard/', label:'Dashboard',    icon:'⊞' },
    { href:'/map/',        label:'Live Map',     icon:'🗺' },
    { href:'/traffic/',    label:'Traffic Blocks', icon:'🚧' },
    { href:'/complaints/', label:'Complaints',   icon:'📋' },
    { href:'/notifications/', label:'Notifications', icon:'🔔' },
  ],
  operator: [
    { href:'/dashboard/', label:'Dashboard',  icon:'⊞' },
    { href:'/map/',        label:'Live Map',   icon:'🗺' },
    { href:'/buses/',      label:'My Buses',   icon:'🚌' },
    { href:'/routes/',     label:'My Routes',  icon:'🛣' },
    { href:'/stops/',      label:'Bus Stops',  icon:'📍' },
    { href:'/feedback/',   label:'Feedback',   icon:'⭐' },
    { href:'/notifications/', label:'Notifications', icon:'🔔' },
  ],
};

function buildSidebar(user) {
  const navEl = document.getElementById('sidebar-nav');
  if (!navEl) return;

  // Superusers are always treated as admin regardless of role field
  const effectiveRole = (user.is_superuser || user.role === 'admin') ? 'admin' : user.role;
  const items = NAV_ITEMS[effectiveRole] || NAV_ITEMS.user;
  const current = window.location.pathname;

  navEl.innerHTML = items.map(item => `
    <li>
      <a href="${item.href}" class="${current === item.href ? 'active' : ''}">
        <i class="nav-icon">${item.icon}</i>
        <span>${item.label}</span>
      </a>
    </li>
  `).join('');

  // User info
  const avatarEl = document.getElementById('sidebar-avatar');
  const nameEl   = document.getElementById('sidebar-name');
  const roleEl   = document.getElementById('sidebar-role');
  if (avatarEl) avatarEl.textContent = (user.first_name || user.username)[0].toUpperCase();
  if (nameEl)   nameEl.textContent   = user.first_name ? `${user.first_name} ${user.last_name}` : user.username;
  const roleLabels = { admin:'Administrator', user:'Passenger', driver:'Driver', police:'Police Officer', operator:'Bus Operator' };
  if (roleEl) roleEl.textContent = roleLabels[effectiveRole] || effectiveRole;

  // Add class to body for app layout
  document.body.classList.add('app-body');
}

async function initPage() {
  const token = localStorage.getItem('bt_token');
  if (!token) { window.location.href = '/login/'; return; }
  try {
    const user = await GET('/auth/me/');
    localStorage.setItem('bt_user', JSON.stringify(user));
    buildSidebar(user);
    pollNotifCount();
    setInterval(pollNotifCount, 30000);
    return user;
  } catch {
    localStorage.removeItem('bt_token');
    localStorage.removeItem('bt_user');
    window.location.href = '/login/';
  }
}

async function handleLogout() {
  try { await POST('/auth/logout/'); } catch {}
  localStorage.removeItem('bt_token');
  localStorage.removeItem('bt_user');
  window.location.href = '/login/';
}

// ── LOGIN PAGE ───────────────────────────────────────────
async function handleLogin() {
  const username = document.getElementById('login-username')?.value.trim();
  const password = document.getElementById('login-password')?.value;
  const errEl = document.getElementById('login-error');
  if (errEl) errEl.classList.add('hidden');

  if (!username || !password) {
    if (errEl) { errEl.textContent = 'Please enter your username and password.'; errEl.classList.remove('hidden'); }
    return;
  }
  try {
    const res = await POST('/auth/login/', { username, password });
    localStorage.setItem('bt_token', res.token);
    localStorage.setItem('bt_user', JSON.stringify(res.user));
    window.location.href = '/dashboard/';
  } catch (err) {
    const msg = extractError(err);
    if (errEl) { errEl.textContent = msg; errEl.classList.remove('hidden'); }
  }
}

// ── REGISTER PAGE ────────────────────────────────────────
async function handleRegister() {
  const errEl = document.getElementById('reg-error');
  const sucEl = document.getElementById('reg-success');
  if (errEl) errEl.classList.add('hidden');
  if (sucEl) sucEl.classList.add('hidden');

  const role = document.getElementById('reg-role')?.value || 'user';
  const data = {
    first_name: document.getElementById('reg-first')?.value.trim() || '',
    last_name:  document.getElementById('reg-last')?.value.trim()  || '',
    username:   document.getElementById('reg-username')?.value.trim() || '',
    email:      document.getElementById('reg-email')?.value.trim()    || '',
    phone:      document.getElementById('reg-phone')?.value.trim()    || '',
    role,
    password:   document.getElementById('reg-pass')?.value  || '',
    password2:  document.getElementById('reg-pass2')?.value || '',
  };

  if (role === 'driver')   data.license_number   = document.getElementById('reg-license')?.value.trim() || '';
  if (role === 'police') {
    data.badge_number = document.getElementById('reg-badge')?.value.trim()   || '';
    data.station      = document.getElementById('reg-station')?.value.trim() || '';
  }
  if (role === 'operator') {
    data.operator_company = document.getElementById('reg-company')?.value.trim() || '';
    data.operator_id      = document.getElementById('reg-opid')?.value.trim()    || '';
  }

  if (!data.username || !data.password) {
    if (errEl) { errEl.textContent = 'Username and password are required.'; errEl.classList.remove('hidden'); }
    return;
  }

  try {
    const res = await POST('/auth/register/', data);
    if (sucEl) { sucEl.textContent = res.message; sucEl.classList.remove('hidden'); }
    setTimeout(() => window.location.href = '/login/', 2500);
  } catch (err) {
    if (errEl) { errEl.textContent = extractError(err); errEl.classList.remove('hidden'); }
  }
}
