/* =============================================
   TICKET MANAGEMENT — API ENGINE (api.js)
   Supports real backend (fetch) or localStorage mock.
   ============================================= */

// ── Configuration ─────────────────────────
const API_BASE = 'http://127.0.0.1:5000';   // Change to your backend URL
const USE_MOCK = true;                        // Set false when backend is running

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
  'HOD_MATH'
];

// ══════════════════════════════════════════
//  FETCH-BASED API  (used when USE_MOCK = false)
// ══════════════════════════════════════════

async function apiFetchTickets(department) {
  const res = await fetch(`${API_BASE}/tickets/${department}`);
  if (!res.ok) throw new Error('Failed to fetch tickets');
  return res.json();
}

async function apiResolveTicket(ticketId) {
  const res = await fetch(`${API_BASE}/resolve/${ticketId}`, { method: 'POST' });
  if (!res.ok) throw new Error('Failed to resolve ticket');
  return res.json();
}

async function apiRerouteTicket(ticketId, newDepartment) {
  const res = await fetch(`${API_BASE}/reroute`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ticket_id: ticketId, new_department: newDepartment })
  });
  if (!res.ok) throw new Error('Failed to reroute ticket');
  return res.json();
}

// ══════════════════════════════════════════
//  LOCAL-STORAGE MOCK  (used when USE_MOCK = true)
// ══════════════════════════════════════════

const STORAGE_KEY = 'ticket_system_data';

const PLACEMENT_KEYWORDS = ['placement', 'internship', 'company', 'package', 'recruit', 'hiring', 'offer', 'ctc', 'lpa', 'job'];
const ACADEMIC_KEYWORDS = ['attendance', 'exam', 'marks', 'grade', 'schedule', 'syllabus', 'cgpa', 'sgpa', 'result', 'revaluation', 'assignment', 'lecture', 'class', 'timetable', 'semester', 'subject', 'faculty', 'professor', 'teacher'];

function _load() {
  try { return JSON.parse(localStorage.getItem(STORAGE_KEY)) || { tickets: [], counter: 1000 }; }
  catch { return { tickets: [], counter: 1000 }; }
}

function _save(data) { localStorage.setItem(STORAGE_KEY, JSON.stringify(data)); }

function _now() { return new Date().toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit', hour12: false }); }
function _today() { return new Date().toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' }); }

function classifyQuery(text) {
  const lower = text.toLowerCase();
  const depts = [];
  if (PLACEMENT_KEYWORDS.some(k => lower.includes(k))) depts.push('Placements');
  if (ACADEMIC_KEYWORDS.some(k => lower.includes(k))) depts.push('Academics');
  if (depts.length === 0) depts.push('Academics');
  return depts;
}

function createTicket(name, regNo, query) {
  const data = _load();
  data.counter = (data.counter || 1000) + 1;
  const id = 'T' + data.counter;
  const departments = classifyQuery(query);
  const ticket = {
    id, name: name.trim(), regNo: regNo.trim(), query: query.trim(),
    time: _now(), date: _today(), createdAt: new Date().toISOString(),
    departments: [...departments], currentDepartments: [...departments],
    status: 'Open', resolvedBy: null, reply: null,
    log: [
      { event: 'Created', time: _now(), date: _today(), detail: `Ticket created by ${name.trim()}` },
      { event: 'Routed', time: _now(), date: _today(), detail: `Routed to ${departments.join(', ')}` }
    ]
  };
  data.tickets.push(ticket);
  _save(data);
  return ticket;
}

function mockFetchTickets(department) {
  return _load().tickets.filter(t => t.currentDepartments.includes(department));
}

function mockResolveTicket(ticketId, reply, department) {
  const data = _load();
  const t = data.tickets.find(t => t.id === ticketId);
  if (!t) return null;
  t.status = 'Resolved';
  t.resolvedBy = department || t.currentDepartments[0] || 'System';
  t.resolvedAt = new Date().toISOString();
  t.reply = reply || '';
  t.log.push({ event: 'Resolved', time: _now(), date: _today(), detail: `Resolved by ${t.resolvedBy}${reply ? ': "' + reply + '"' : ''}` });
  _save(data);
  return t;
}

function mockRerouteTicket(ticketId, newDepartment) {
  const data = _load();
  const t = data.tickets.find(t => t.id === ticketId);
  if (!t) return null;
  const from = t.currentDepartments.join(', ');
  const oldDepts = [...t.currentDepartments];
  t.currentDepartments = [newDepartment];
  t.status = 'Open';
  t.log.push({ event: 'Rerouted', time: _now(), date: _today(), detail: `Rerouted from ${from} to ${newDepartment}` });
  _save(data);
  return t;
}

// ── Lookup Helpers (for student tracking) ─
function getTicketById(ticketId) {
  return _load().tickets.find(t => t.id === ticketId) || null;
}

function getTicketsByRegNo(regNo) {
  return _load().tickets.filter(t => t.regNo === regNo);
}

function getAllTickets() {
  return _load().tickets;
}

// ══════════════════════════════════════════
//  UNIFIED PUBLIC API
// ══════════════════════════════════════════

async function fetchTickets(department) {
  if (USE_MOCK) return mockFetchTickets(department);
  return apiFetchTickets(department);
}

async function resolveTicket(ticketId, reply, department) {
  if (USE_MOCK) return mockResolveTicket(ticketId, reply, department);
  return apiResolveTicket(ticketId);
}

async function rerouteTicket(ticketId, newDepartment) {
  if (USE_MOCK) return mockRerouteTicket(ticketId, newDepartment);
  return apiRerouteTicket(ticketId, newDepartment);
}
