const crypto = require('crypto');

function hashPassword(pwd) {
  const salt = crypto.randomBytes(16).toString('hex');
  const derivedKey = crypto.scryptSync(String(pwd), salt, 64).toString('hex');
  return `scrypt$${salt}$${derivedKey}`;
}

module.exports = { hashPassword };
