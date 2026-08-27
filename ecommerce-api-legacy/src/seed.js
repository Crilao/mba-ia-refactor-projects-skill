const { initDb, seedDb } = require('./database');

async function seed() {
  await initDb();
  await seedDb();
  console.info('Database seeded successfully.');
}

seed().catch((error) => {
  console.error('Failed to seed database:', error.message);
  process.exit(1);
});
