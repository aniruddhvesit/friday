import { createServer } from 'vite';

async function start() {
  const server = await createServer({
    configFile: './vite.config.ts',
  });
  await server.listen();
  console.log('Tyler Frontend dev server running on port 1420');
}

start().catch((err) => {
  console.error('Failed to start dev server:', err);
  process.exit(1);
});
