const controllers = require('./controllers');

function registerRoutes(app) {
  app.post('/api/checkout', controllers.checkout);
  app.get('/api/admin/financial-report', controllers.financialReport);
  app.delete('/api/users/:id', controllers.deleteUser);
}

module.exports = registerRoutes;

