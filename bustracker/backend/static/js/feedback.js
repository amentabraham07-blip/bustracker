/* ── FEEDBACK PAGE ── */

let _feedbackRating = 0;

document.addEventListener('DOMContentLoaded', async () => {
  const user = await initPage();
  if (!user) return;

  // Admin and operators only view feedback, cannot submit
  if (user.role === 'admin' || user.role === 'operator') {
    document.getElementById('feedback-form-card').classList.add('hidden');
  } else {
    populateBusDropdown();
  }
  loadFeedback();
});

async function populateBusDropdown() {
  try {
    const buses = await GET('/buses/');
    const sel = document.getElementById('fb-bus');
    sel.innerHTML = '<option value="">Select bus (optional)</option>' +
      buses.map(b => `<option value="${b.id}">${b.bus_number}</option>`).join('');
  } catch {}
}

async function loadFeedback() {
  const list = document.getElementById('feedback-list');
  try {
    const feedbacks = await GET('/feedback/');
    if (!feedbacks.length) {
      list.innerHTML = emptyState('⭐', 'No feedback submitted yet.');
      return;
    }
    list.innerHTML = feedbacks.map(f => `
      <div class="feedback-item">
        <div class="feedback-stars">${'★'.repeat(f.rating)}${'☆'.repeat(5 - f.rating)}</div>
        <div class="feedback-msg">${f.message}</div>
        <div class="feedback-meta">
          <span>👤 ${f.user_name}</span>
          <span>🏷 ${f.category}</span>
          ${f.bus ? `<span>🚌 Bus ${f.bus}</span>` : ''}
          <span>${formatTime(f.created_at)}</span>
        </div>
      </div>
    `).join('');
  } catch {
    list.innerHTML = emptyState('⭐', 'Failed to load feedback.');
  }
}

function setRating(val) {
  _feedbackRating = val;
  document.querySelectorAll('.star').forEach((s, i) => {
    s.classList.toggle('active', i < val);
  });
}

async function submitFeedback() {
  if (!_feedbackRating) { toast('Please select a star rating', 'error'); return; }
  const msg = document.getElementById('fb-message').value.trim();
  if (!msg) { toast('Please write a message', 'error'); return; }

  const data = {
    rating:   _feedbackRating,
    category: document.getElementById('fb-category').value,
    message:  msg,
    bus:      document.getElementById('fb-bus').value || null,
  };
  try {
    await POST('/feedback/', data);
    toast('Thank you for your feedback!', 'success');
    document.getElementById('fb-message').value = '';
    _feedbackRating = 0;
    document.querySelectorAll('.star').forEach(s => s.classList.remove('active'));
    loadFeedback();
  } catch (err) { toast(extractError(err), 'error'); }
}
