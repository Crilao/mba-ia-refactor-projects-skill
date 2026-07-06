const config = {
  port: Number(process.env.PORT || 3000),
  adminToken: process.env.ADMIN_TOKEN || 'admin-token',
  paymentGatewayKey: process.env.PAYMENT_GATEWAY_KEY || 'pk_test_demo_gateway',
};

module.exports = config;

