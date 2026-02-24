const api = {
  async login(email, password) {
    const r = await fetch('/api/auth/login', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ email, password }) });
    if (!r.ok) throw new Error('Login failed');
    return r.json();
  },
  getServices: () => fetch('/api/services').then(r => r.json()),
  createBooking: body => fetch('/api/bookings', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) }).then(r => r.json()),
  clientBookings: id => fetch(`/api/client/${id}/bookings`).then(r => r.json()),
  partnerBookings: id => fetch(`/api/partner/${id}/bookings`).then(r => r.json()),
  partnerPayouts: id => fetch(`/api/partner/${id}/payouts`).then(r => r.json()),
  adminOverview: () => fetch('/api/admin/overview').then(r => r.json()),
  adminBookings: () => fetch('/api/admin/bookings').then(r => r.json()),
  adminUsers: () => fetch('/api/admin/users').then(r => r.json()),
  updateBooking: (id, body) => fetch(`/api/admin/bookings/${id}`, { method: 'PATCH', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) }).then(r => r.json())
};

function saveSession(user) { localStorage.setItem('kp_user', JSON.stringify(user)); }
function getSession() { try { return JSON.parse(localStorage.getItem('kp_user')); } catch { return null; } }
function logout() { localStorage.removeItem('kp_user'); location.href = '/login.html'; }

window.KP = { api, saveSession, getSession, logout };
