const config = require('./config');
const createApp = require('./appFactory');
const { initDb } = require('./database');

async function bootstrap() {
  await initDb();

  const app = createApp();
  app.listen(config.port, () => {
    console.log(`Frankenstein LMS rodando na porta ${config.port}...`);
  });
}

bootstrap().catch((error) => {
  console.error('Falha ao iniciar a aplicação:', error);
  process.exit(1);
});
