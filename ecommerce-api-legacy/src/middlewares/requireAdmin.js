const crypto = require('crypto');
const config = require('../config');

function hasMatchingToken(providedToken, expectedToken) {
  const provided = Buffer.from(providedToken || '');
  const expected = Buffer.from(expectedToken || '');

  return provided.length === expected.length
    && provided.length > 0
    && crypto.timingSafeEqual(provided, expected);
}

function requireAdmin(req, res, next) {
  if (!config.adminToken) {
    return res.status(503).json({ error: 'Admin authorization is not configured' });
  }

  const [scheme, token] = (req.get('authorization') || '').split(' ');
  if (scheme !== 'Bearer' || !hasMatchingToken(token, config.adminToken)) {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  return next();
}

module.exports = requireAdmin;
