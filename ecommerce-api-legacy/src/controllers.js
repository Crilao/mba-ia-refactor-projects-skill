const services = require('./services');

async function checkout(req, res) {
  try {
    const result = await services.processCheckout(req.body);
    return res.status(result.status).send(result.body);
  } catch (error) {
    return res.status(500).send(error.message || 'Erro interno');
  }
}

async function financialReport(req, res) {
  try {
    const report = await services.getFinancialReport();
    return res.json(report);
  } catch (error) {
    return res.status(500).send(error.message || 'Erro interno');
  }
}

async function deleteUser(req, res) {
  try {
    const message = await services.deleteUserAndKeepAudit(req.params.id);
    return res.send(message);
  } catch (error) {
    return res.status(500).send(error.message || 'Erro interno');
  }
}

module.exports = {
  checkout,
  financialReport,
  deleteUser,
};

