// Service worker mínimo — existe apenas para o navegador considerar o site
// "instalável" como app (é um dos requisitos técnicos do Chrome/Android).
// Não guardamos nada em cache de propósito: como o conteúdo da plataforma
// muda o tempo todo (novos cursos, provas, materiais), um app 100% offline
// mostraria informação desatualizada para o aluno. Por isso, cada clique
// no app continua buscando os dados atuais no servidor, exatamente como no navegador.

self.addEventListener('install', (event) => {
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  self.clients.claim();
});

self.addEventListener('fetch', () => {
  // Propositalmente vazio: deixa toda requisição seguir normal pela rede.
});
