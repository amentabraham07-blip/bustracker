/* ── BUSTRACK UTILS ── shared across all pages ── */

const API = '/api';

async function apiFetch(method, endpoint, data = null) {
  const opts = {
    method,
    headers: { 'Content-Type': 'application/json' },
  };
  const token = localStorage.getItem('bt_token');
  if (token) opts.headers['Authorization'] = `Token ${token}`;
  if (data) opts.body = JSON.stringify(data);
  const res = await fetch(`${API}${endpoint}`, opts);
  const json = await res.json().catch(() => ({}));
  if (!res.ok) throw json;
  return json;
}

const GET  = (ep)    => apiFetch('GET',   ep);
const POST = (ep, d) => apiFetch('POST',  ep, d);
const PATCH= (ep, d) => apiFetch('PATCH', ep, d);

function formatTime(ts) {
  if (!ts) return '—';
  const d = new Date(ts);
  const diff = (Date.now() - d) / 1000;
  if (diff < 60)    return 'Just now';
  if (diff < 3600)  return `${Math.floor(diff/60)}m ago`;
  if (diff < 86400) return `${Math.floor(diff/3600)}h ago`;
  return d.toLocaleDateString('en-IN', { day:'numeric', month:'short', hour:'2-digit', minute:'2-digit' });
}

function extractError(err) {
  if (!err) return 'An error occurred.';
  if (typeof err === 'string') return err;
  const vals = Object.values(err);
  if (!vals.length) return 'An error occurred.';
  const first = vals[0];
  return Array.isArray(first) ? first[0] : String(first);
}

let _toastTimer = null;
function toast(msg, type = '') {
  const el = document.getElementById('toast');
  if (!el) return;
  el.textContent = msg;
  el.className = `toast ${type}`;
  el.classList.remove('hidden');
  clearTimeout(_toastTimer);
  _toastTimer = setTimeout(() => el.classList.add('hidden'), 3500);
}

function closeModal() {
  const ov = document.getElementById('modal-overlay');
  if (ov) ov.classList.add('hidden');
}

function toggleSidebar() {
  document.getElementById('sidebar').classList.toggle('open');
}

function emptyState(icon, msg) {
  return `<div class="empty-state"><div class="empty-icon">${icon}</div><p>${msg}</p></div>`;
}

// Poll notification count and update badge
async function pollNotifCount() {
  try {
    const notifs = await GET('/notifications/');
    const badge = document.getElementById('notif-count');
    if (!badge) return;
    if (notifs.length > 0) {
      badge.textContent = notifs.length;
      badge.classList.remove('hidden');
    } else {
      badge.classList.add('hidden');
    }
  } catch {}
}
