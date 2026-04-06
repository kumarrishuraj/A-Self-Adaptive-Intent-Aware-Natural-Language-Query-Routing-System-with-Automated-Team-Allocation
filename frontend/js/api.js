/* =============================================
   TICKET MANAGEMENT — API ENGINE (api.js)
   Supports real backend (fetch)
   ============================================= */

// ── Configuration ─────────────────────────
// Dynamically determine API_BASE based on hostname or protocol (for local files)
const isLocal = window.location.hostname === '127.0.0.1' || window.location.hostname === 'localhost' || window.location.protocol === 'file:';

// ⚠️ IMPORTANT: BEFORE DEPLOYING TO VERCEL, REPLACE THIS STRING WITH YOUR LIVE RENDER URL!
// Example: 'https://nlp-routing-backend.onrender.com/api'
const API_BASE = isLocal ? 'http://127.0.0.1:5000/api' : '/api';

// ── Reroute Department List ───────────────
const REROUTE_DEPARTMENTS = [
  'Academics',
  'Admissions',
  'Examination',
  'Fees_and_Account',
  'International_Affair',
  'IT',
  'Residential_Services',
  'Security_and_Safety',
  'Placements',
  'Division_of_Research_and_Development',
  'Library',
  'HOD_ML',
  'HOD_MATH',
  'EDU_REV'
];

// ── Auth Helpers ────────────────────────────
const SESSION_KEY = 'ticket_system_session';
const TOKEN_KEY = 'ticket_system_token';

function getAuthHeaders() {
  const headers = { 'Content-Type': 'application/json' };
  const token = sessionStorage.getItem(TOKEN_KEY);
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  return headers;
}

// ══════════════════════════════════════════
//  FETCH-BASED API
// ══════════════════════════════════════════

async function fetchTickets(department) {
  const res = await fetch(`${API_BASE}/tickets/dept/${department}`, {
    headers: getAuthHeaders()
  });
  if (!res.ok) throw new Error('Failed to fetch tickets');
  return res.json();
}

async function resolveTicket(ticketId, reply, department) {
  const res = await fetch(`${API_BASE}/tickets/resolve/${ticketId}`, { 
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify({ reply, department })
  });
  if (!res.ok) throw new Error('Failed to resolve ticket');
  return res.json();
}

async function rerouteTicket(ticketId, newDepartment) {
  const res = await fetch(`${API_BASE}/tickets/reroute`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify({ ticket_id: ticketId, new_department: newDepartment })
  });
  if (!res.ok) throw new Error('Failed to reroute ticket');
  return res.json();
}

async function createTicket(name, regNo, query) {
  const res = await fetch(`${API_BASE}/tickets/create`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify({ name, regNo, query })
  });
  if (!res.ok) {
     const errorData = await res.json();
     throw new Error(errorData.error || 'Failed to create ticket');
  }
  return res.json();
}

async function getTicketsByRegNo(regNo) {
  const res = await fetch(`${API_BASE}/tickets/student/${regNo}`, {
    headers: getAuthHeaders()
  });
  if (!res.ok) {
     const errorData = await res.json();
     throw new Error(errorData.error || 'Failed to fetch user tickets');
  }
  return res.json();
}

async function registerUser(name, regNo, password) {
  const res = await fetch(`${API_BASE}/signup`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, regNo, password })
  });
  if (!res.ok) {
     const errorData = await res.json();
     throw new Error(errorData.error || 'Registration failed');
  }
  const data = await res.json();
  // Optional: auto login on signup
  if (data.token) {
    // We can store token, but the UI redirects to login right now
  }
}

async function loginUser(regNo, password) {
  const res = await fetch(`${API_BASE}/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ regNo, password })
  });
  if (!res.ok) {
     const errorData = await res.json();
     throw new Error(errorData.error || 'Login failed');
  }
  const data = await res.json();
  sessionStorage.setItem(SESSION_KEY, JSON.stringify(data.user));
  sessionStorage.setItem(TOKEN_KEY, data.token);
  return data.user;
}

function logoutUser() {
  sessionStorage.removeItem(SESSION_KEY);
  sessionStorage.removeItem(TOKEN_KEY);
}

function getCurrentUser() {
  const user = sessionStorage.getItem(SESSION_KEY);
  return user ? JSON.parse(user) : null;
}