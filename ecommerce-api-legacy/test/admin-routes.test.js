const assert = require('node:assert/strict');
const { after, before, test } = require('node:test');
const { existsSync, mkdtempSync, rmSync } = require('node:fs');
const { tmpdir } = require('node:os');
const { join } = require('node:path');

const databaseDirectory = mkdtempSync(join(tmpdir(), 'ecommerce-api-legacy-'));
process.env.ADMIN_TOKEN = 'test-admin-token';
process.env.SEED_USER_PASSWORD = 'seed-password-for-tests';
process.env.DATABASE_PATH = join(databaseDirectory, 'ecommerce.sqlite');

const createApp = require('../src/appFactory');
const database = require('../src/database');
const repository = require('../src/repositories');

let server;
let baseUrl;

before(async () => {
  await database.initDb();
  await database.seedDb();
  server = createApp().listen(0);
  await new Promise((resolve) => server.once('listening', resolve));
  baseUrl = `http://127.0.0.1:${server.address().port}`;
});

after(async () => {
  await new Promise((resolve, reject) => server.close((error) => (error ? reject(error) : resolve())));
  await database.closeDb();
  rmSync(databaseDirectory, { recursive: true, force: true });
});

test('administrative routes reject requests without a valid bearer token', async () => {
  const reportResponse = await fetch(`${baseUrl}/api/admin/financial-report`);
  assert.equal(reportResponse.status, 401);

  const deleteResponse = await fetch(`${baseUrl}/api/users/1`, { method: 'DELETE' });
  assert.equal(deleteResponse.status, 401);
  assert.ok(await repository.findUserById(1), 'the unauthorized request must not reach the deletion service');
});

test('the seed uses a salted password hash and checkout remains available', async () => {
  const seededUser = await repository.findUserById(1);
  assert.match(seededUser.pass, /^scrypt\$/);
  assert.notEqual(seededUser.pass, process.env.SEED_USER_PASSWORD);

  const checkoutResponse = await fetch(`${baseUrl}/api/checkout`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      usr: 'Leonan',
      eml: 'leonan@fullcycle.com.br',
      c_id: 2,
      card: '4111222233334444',
    }),
  });

  assert.equal(checkoutResponse.status, 200);
});

test('administrative routes accept the configured bearer token', async () => {
  const headers = { Authorization: 'Bearer test-admin-token' };

  const reportResponse = await fetch(`${baseUrl}/api/admin/financial-report`, { headers });
  assert.equal(reportResponse.status, 200);
  assert.ok(Array.isArray(await reportResponse.json()));

  const deleteResponse = await fetch(`${baseUrl}/api/users/1`, { method: 'DELETE', headers });
  assert.equal(deleteResponse.status, 200);
  assert.equal(await repository.findUserById(1), undefined);
  assert.ok(existsSync(process.env.DATABASE_PATH));
});
