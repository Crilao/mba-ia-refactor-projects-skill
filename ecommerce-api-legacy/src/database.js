const sqlite3 = require('sqlite3').verbose();

let db;

function getDb() {
  if (!db) {
    db = new sqlite3.Database(':memory:');
  }
  return db;
}

function run(sql, params = []) {
  const database = getDb();
  return new Promise((resolve, reject) => {
    database.run(sql, params, function runCallback(err) {
      if (err) return reject(err);
      resolve({ lastID: this.lastID, changes: this.changes });
    });
  });
}

function get(sql, params = []) {
  const database = getDb();
  return new Promise((resolve, reject) => {
    database.get(sql, params, (err, row) => {
      if (err) return reject(err);
      resolve(row);
    });
  });
}

function all(sql, params = []) {
  const database = getDb();
  return new Promise((resolve, reject) => {
    database.all(sql, params, (err, rows) => {
      if (err) return reject(err);
      resolve(rows);
    });
  });
}

function exec(sql) {
  const database = getDb();
  return new Promise((resolve, reject) => {
    database.exec(sql, (err) => {
      if (err) return reject(err);
      resolve();
    });
  });
}

async function initDb() {
  await exec(`
    CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY,
      name TEXT,
      email TEXT UNIQUE,
      pass TEXT
    );
    CREATE TABLE IF NOT EXISTS courses (
      id INTEGER PRIMARY KEY,
      title TEXT,
      price REAL,
      active INTEGER
    );
    CREATE TABLE IF NOT EXISTS enrollments (
      id INTEGER PRIMARY KEY,
      user_id INTEGER,
      course_id INTEGER
    );
    CREATE TABLE IF NOT EXISTS payments (
      id INTEGER PRIMARY KEY,
      enrollment_id INTEGER,
      amount REAL,
      status TEXT
    );
    CREATE TABLE IF NOT EXISTS audit_logs (
      id INTEGER PRIMARY KEY,
      action TEXT,
      created_at DATETIME
    );
  `);
}

async function seedDb() {
  const existingUsers = await get('SELECT COUNT(*) AS count FROM users');
  if (existingUsers.count > 0) return;

  await run("INSERT INTO users (name, email, pass) VALUES (?, ?, ?)", ['Leonan', 'leonan@fullcycle.com.br', '123']);
  await run(
    "INSERT INTO courses (title, price, active) VALUES (?, ?, ?), (?, ?, ?)",
    ['Clean Architecture', 997.0, 1, 'Docker', 497.0, 1]
  );
  await run("INSERT INTO enrollments (user_id, course_id) VALUES (?, ?)", [1, 1]);
  await run("INSERT INTO payments (enrollment_id, amount, status) VALUES (?, ?, ?)", [1, 997.0, 'PAID']);
}

module.exports = {
  getDb,
  run,
  get,
  all,
  initDb,
  seedDb,
};

