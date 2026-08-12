// App de desktop: uma casca (BrowserWindow) que abre a Plataforma de
// Treinamentos em Telecomunicações publicada no Streamlit Cloud. Não guarda
// nenhum dado nem lógica de negócio — tudo acontece no site; aqui só
// cuidamos de detalhes que um navegador comum resolveria sozinho: manter a
// janela com cara de app (sem barra de endereço), abrir links externos no
// navegador padrão em vez de dentro do app, e lembrar a sessão entre uma
// abertura e outra.
const { app, BrowserWindow, shell, session, Menu, dialog, clipboard } = require("electron");
const path = require("path");
const fs = require("fs");

const URL_APP = "https://cursos-telecom.streamlit.app/";
const DOMINIO_PERMITIDO = "cursos-telecom.streamlit.app";
const ARQUIVO_ESTADO = path.join(app.getPath("userData"), "ultima-sessao.json");

function lerUltimaUrl() {
  try {
    const conteudo = JSON.parse(fs.readFileSync(ARQUIVO_ESTADO, "utf-8"));
    if (conteudo.url && new URL(conteudo.url).hostname === DOMINIO_PERMITIDO) {
      return conteudo.url;
    }
  } catch (_) {
    // primeira vez rodando o app, ou arquivo corrompido: usa a URL padrão.
  }
  return URL_APP;
}

function salvarUltimaUrl(url) {
  try {
    if (new URL(url).hostname === DOMINIO_PERMITIDO) {
      fs.writeFileSync(ARQUIVO_ESTADO, JSON.stringify({ url }));
    }
  } catch (_) {
    // ignora falha ao persistir — não é crítico.
  }
}

// Abre um link no navegador padrão do Windows. Em algumas máquinas (ex:
// antivírus/política corporativa restringindo o app, sem navegador padrão
// definido) o shell.openExternal pode falhar silenciosamente — nesse caso
// copiamos o link e avisamos o usuário em vez de simplesmente não fazer nada.
function abrirLinkExterno(janela, url) {
  shell.openExternal(url).catch(() => {
    clipboard.writeText(url);
    dialog.showMessageBox(janela, {
      type: "warning",
      title: "Não foi possível abrir o link",
      message: "Não consegui abrir o navegador automaticamente. Copiei o endereço abaixo para a área de transferência — cole em qualquer navegador para acessar:",
      detail: url,
    });
  });
}

function criarJanelaPrincipal() {
  const janela = new BrowserWindow({
    width: 1280,
    height: 800,
    minWidth: 360,
    minHeight: 500,
    icon: path.join(__dirname, "build", "icon.png"),
    title: "Treinamentos Telecom",
    autoHideMenuBar: true,
    backgroundColor: "#0F2E56",
    webPreferences: {
      contextIsolation: true,
      nodeIntegration: false,
      preload: path.join(__dirname, "preload.js"),
    },
  });

  Menu.setApplicationMenu(null);

  // Links que abririam em nova aba (ex: target="_blank", como o botão
  // "Abrir" dos Materiais) vão pro navegador padrão.
  janela.webContents.setWindowOpenHandler(({ url }) => {
    abrirLinkExterno(janela, url);
    return { action: "deny" };
  });

  // Navegação de página inteira pra fora do domínio do app também vai pro navegador padrão.
  janela.webContents.on("will-navigate", (evento, url) => {
    const destino = new URL(url);
    if (destino.hostname !== DOMINIO_PERMITIDO) {
      evento.preventDefault();
      abrirLinkExterno(janela, url);
    }
  });

  janela.webContents.on("did-navigate", (_evento, url) => salvarUltimaUrl(url));
  janela.webContents.on("did-navigate-in-page", (_evento, url) => salvarUltimaUrl(url));

  janela.loadURL(lerUltimaUrl());

  return janela;
}

app.whenReady().then(() => {
  // Downloads (ex: certificado de capacitação em PDF) caem direto na pasta
  // Downloads do usuário, com o nome sugerido pela própria página.
  session.defaultSession.on("will-download", (_evento, item) => {
    item.once("done", (_e, estado) => {
      if (estado !== "completed") {
        console.warn("Download não concluído:", estado);
      }
    });
  });

  criarJanelaPrincipal();

  app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      criarJanelaPrincipal();
    }
  });
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});
