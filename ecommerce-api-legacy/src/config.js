const path = require('path');

const config = {
  port: Number(process.env.PORT || 3000),
  adminToken: process.env.ADMIN_TOKEN || '',
  databasePath: process.env.DATABASE_PATH || path.resolve(__dirname, '..', 'data', 'ecommerce.sqlite'),
  seedUserPassword: process.env.SEED_USER_PASSWORD || '',
};

module.exports = config;
