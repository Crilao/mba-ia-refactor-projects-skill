const controllers = require('./controllers');
const requireAdmin = require('./middlewares/requireAdmin');

function registerRoutes(app) {
  app.post('/api/checkout', controllers.checkout);
  app.get('/api/admin/financial-report', requireAdmin, controllers.financialReport);
  app.delete('/api/users/:id', requireAdmin, controllers.deleteUser);
}

module.exports = registerRoutes;
