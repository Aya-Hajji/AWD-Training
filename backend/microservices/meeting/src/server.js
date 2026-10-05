const app = require('./app');
const { Eureka } = require('eureka-js-client');

const PORT = Number(process.env.PORT) || 8085;
const HOST = 'localhost';

// ---- Eureka client ----
const eurekaClient = new Eureka({
  instance: {
    app: 'MEETING',
    // instanceId unique par port, pour pouvoir lancer plusieurs instances
    instanceId: `meeting:${PORT}`,
    hostName: HOST,
    ipAddr: '127.0.0.1',
    port: { '$': PORT, '@enabled': true },
    vipAddress: 'meeting',
    statusPageUrl: `http://${HOST}:${PORT}/swagger-ui`,
    dataCenterInfo: {
      '@class': 'com.netflix.appinfo.InstanceInfo$DefaultDataCenterInfo',
      name: 'MyOwn',
    },
  },
  eureka: {
    host: 'localhost',
    port: 8761,
    servicePath: '/eureka/apps/',
  },
});

const server = app.listen(PORT, () => {
  console.log(`meeting microservice running on http://localhost:${PORT}`);
  console.log(`Swagger UI: http://localhost:${PORT}/swagger-ui`);

  // Enregistrement auprès d'Eureka une fois le serveur démarré
  eurekaClient.start((error) => {
    console.log(error ? `Eureka registration failed: ${error}` : 'Registered with Eureka as MEETING');
  });
});

// ---- Désenregistrement propre à l'arrêt ----
process.on('SIGINT', () => {
  console.log('Stopping meeting service, unregistering from Eureka...');
  eurekaClient.stop(() => {
    server.close(() => process.exit(0));
  });
});