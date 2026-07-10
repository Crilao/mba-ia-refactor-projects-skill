const crypto = require('crypto');
const config = require('./config');

let globalCache = {};
let totalRevenue = 0;

function logAndCache(key, data) {
  console.log(`[LOG] Salvando no cache: ${key}`);
  globalCache[key] = data;
}

function hashPassword(pwd) {
  const salt = crypto.randomBytes(16).toString('hex');
  const derivedKey = crypto.scryptSync(String(pwd), salt, 64).toString('hex');
  return `scrypt$${salt}$${derivedKey}`;
}

module.exports = { config, logAndCache, hashPassword, globalCache, totalRevenue };
