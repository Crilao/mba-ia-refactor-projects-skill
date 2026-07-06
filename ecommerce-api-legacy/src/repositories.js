const db = require('./database');

async function findCourseById(courseId) {
  return db.get('SELECT * FROM courses WHERE id = ? AND active = 1', [courseId]);
}

async function findUserByEmail(email) {
  return db.get('SELECT * FROM users WHERE email = ?', [email]);
}

async function findUserById(userId) {
  return db.get('SELECT * FROM users WHERE id = ?', [userId]);
}

async function createUser(name, email, pass) {
  const result = await db.run('INSERT INTO users (name, email, pass) VALUES (?, ?, ?)', [name, email, pass]);
  return result.lastID;
}

async function createEnrollment(userId, courseId) {
  const result = await db.run('INSERT INTO enrollments (user_id, course_id) VALUES (?, ?)', [userId, courseId]);
  return result.lastID;
}

async function createPayment(enrollmentId, amount, status) {
  return db.run('INSERT INTO payments (enrollment_id, amount, status) VALUES (?, ?, ?)', [enrollmentId, amount, status]);
}

async function createAuditLog(action) {
  return db.run("INSERT INTO audit_logs (action, created_at) VALUES (?, datetime('now'))", [action]);
}

async function getCourses() {
  return db.all('SELECT * FROM courses', []);
}

async function getEnrollmentsByCourse(courseId) {
  return db.all('SELECT * FROM enrollments WHERE course_id = ?', [courseId]);
}

async function findUserBasicById(userId) {
  return db.get('SELECT name, email FROM users WHERE id = ?', [userId]);
}

async function findPaymentByEnrollment(enrollmentId) {
  return db.get('SELECT amount, status FROM payments WHERE enrollment_id = ?', [enrollmentId]);
}

async function deleteUser(userId) {
  return db.run('DELETE FROM users WHERE id = ?', [userId]);
}

module.exports = {
  findCourseById,
  findUserByEmail,
  findUserById,
  createUser,
  createEnrollment,
  createPayment,
  createAuditLog,
  getCourses,
  getEnrollmentsByCourse,
  findUserBasicById,
  findPaymentByEnrollment,
  deleteUser,
};

