/**
 * Configuração do Tailwind usada para GERAR o arquivo static/css/app.css.
 *
 * Antes o site carregava o "Play CDN" (https://cdn.tailwindcss.com), que
 * baixa o compilador inteiro do Tailwind e monta o CSS dentro do navegador
 * do aluno a cada abertura de página — é a própria documentação do Tailwind
 * que diz que isso não deve ser usado em produção. Agora o CSS é gerado
 * aqui, uma vez, e servido pronto pelo nosso servidor.
 *
 * Como regerar depois de mexer em qualquer template:
 *     npm install
 *     npm run build:css
 * (e commitar o static/css/app.css atualizado)
 */
module.exports = {
  content: [
    "./webapp/templates/**/*.html",
    "./static/js/**/*.js",
  ],
  theme: {
    extend: {
      colors: {
        "norte-azul": "#143C6E",
        "norte-azul-escuro": "#0F2E56",
        "norte-azul-claro": "#1F5AA8",
        "bg-dark": "#0b0f19",
      },
    },
  },
  plugins: [],
};
