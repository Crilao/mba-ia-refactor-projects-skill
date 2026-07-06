const express = require('express');
const registerRoutes = require('./routes');

function createApp() {
  const app = express();
  app.use(express.json());
  registerRoutes(app);
  return app;
}

module.exports = createApp;

