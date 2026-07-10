const config = {
  port: Number(process.env.PORT || 3000),
  adminToken: process.env.ADMIN_TOKEN || '',
  paymentGatewayKey: process.env.PAYMENT_GATEWAY_KEY || '',
};

module.exports = config;
