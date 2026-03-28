/* =============================================
   TICKET MANAGEMENT — API ENGINE (api.js)
   Supports real backend (fetch)
   ============================================= */

// ── Configuration ─────────────────────────
const API_BASE = 'http://127.0.0.1:5000/api';

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

// ══════════════════════════════════════════
//  FETCH-BASED API
// ══════════════════════════════════════════

async function fetchTickets(department) {
  const res = await fetch(`${API_BASE}/tickets/dept/${department}`);
  if (!res.ok) throw new Error('Failed to fetch tickets');
  return res.json();
}

async function resolveTicket(ticketId, reply, department) {
  const res = await fetch(`${API_BASE}/tickets/resolve/${ticketId}`, { 
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ reply, department })
  });
  if (!res.ok) throw new Error('Failed to resolve ticket');
  return res.json();
}

async function rerouteTicket(ticketId, newDepartment) {
  const res = await fetch(`${API_BASE}/tickets/reroute`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ticket_id: ticketId, new_department: newDepartment })
  });
  if (!res.ok) throw new Error('Failed to reroute ticket');
  return res.json();
}

async function createTicket(name, regNo, query) {
  const res = await fetch(`${API_BASE}/tickets/create`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, regNo, query })
  });
  if (!res.ok) {
     const errorData = await res.json();
     throw new Error(errorData.error || 'Failed to create ticket');
  }
  return res.json();
}

async function getTicketsByRegNo(regNo) {
  const res = await fetch(`${API_BASE}/tickets/student/${regNo}`);
  if (!res.ok) throw new Error('Failed to fetch user tickets');
  return res.json();
}

// ── Auth Helpers ────────────────────────────

const SESSION_KEY = 'ticket_system_session';

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
  return data.user;
}

function logoutUser() {
  sessionStorage.removeItem(SESSION_KEY);
}

function getCurrentUser() {
  return JSON.parse(sessionStorage.getItem(SESSION_KEY));
}