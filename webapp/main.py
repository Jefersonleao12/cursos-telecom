"""
Ponto de entrada da Plataforma de Treinamentos em Telecomunicações
(FastAPI). Roda como serviço systemd no VPS — ver scripts/setup-vps.sh.

Para rodar localmente:  uvicorn webapp.main:app --reload
"""
import os

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, PlainTextResponse
from starlette.middleware.gzip import GZipMiddleware

from webapp.auth.routes import router as auth_router
from webapp.cache_html import CacheDeHtmlMiddleware
from webapp.middleware import AutenticacaoMiddleware
from webapp.seguranca.cabecalhos import CabecalhosDeSegurancaMiddleware
from webapp.seguranca.upload import ArquivoGrandeDemaisError
from webapp.static_cache import EstaticosComCache
from webapp.routers.admin.alunos import router as admin_alunos_router
from webapp.routers.admin.aulas import router as admin_aulas_router
from webapp.routers.admin.avisos import router as admin_avisos_router
from webapp.routers.admin.cursos import router as admin_cursos_router
from webapp.routers.admin.dashboard import router as admin_dashboard_router
from webapp.routers.admin.destaques import router as admin_destaques_router
from webapp.routers.admin.duvidas import router as admin_duvidas_router
from webapp.routers.admin.filiais import router as admin_filiais_router
from webapp.routers.admin.materiais import router as admin_materiais_router
from webapp.routers.admin.modulos import router as admin_modulos_router
from webapp.routers.admin.novidades import router as admin_novidades_router
from webapp.routers.admin.provas import router as admin_provas_router
from webapp.routers.certificados import router as certificados_router
from webapp.routers.cursos import router as cursos_router
from webapp.routers.inicio import router as inicio_router
from webapp.routers.jogo import router as jogo_router
from webapp.routers.jogo_suporte import router as jogo_suporte_router
from webapp.routers.jogo_suporte_ia import router as jogo_suporte_ia_router
from webapp.routers.simuladores import router as simuladores_router
from webapp.routers.materiais import router as materiais_router
from webapp.routers.novidades import router as novidades_router
from webapp.routers.perfil import router as perfil_router
from webapp.routers.ranking import router as ranking_router

# A documentação automática do FastAPI (/docs, /redoc, /openapi.json) lista
# TODAS as rotas da plataforma, inclusive as de administração, com os campos
# que cada uma espera. Qualquer aluno logado poderia abrir esse mapa e usá-lo
# como roteiro para tentar chamar rotas que não são dele. Como esta app não é
# uma API pública, a documentação fica desligada; para depurar em uma máquina
# de teste, suba com DOCS_ABERTAS=1.
_DOCS_LIGADAS = os.getenv("DOCS_ABERTAS") == "1"

app = FastAPI(
    title="Treinamentos Telecom",
    docs_url="/docs" if _DOCS_LIGADAS else None,
    redoc_url="/redoc" if _DOCS_LIGADAS else None,
    openapi_url="/openapi.json" if _DOCS_LIGADAS else None,
)

app.mount("/static", EstaticosComCache(directory="static"), name="static")
app.mount("/assets", EstaticosComCache(directory="assets"), name="assets")


@app.exception_handler(ArquivoGrandeDemaisError)
def arquivo_grande_demais(request: Request, erro: ArquivoGrandeDemaisError):
    """Rede de segurança: se algum envio novo esquecer de tratar o limite, o
    aluno vê a explicação em vez de uma tela de erro sem sentido."""
    return PlainTextResponse(str(erro), status_code=413)


app.add_middleware(AutenticacaoMiddleware)
# Manda o navegador conferir com o servidor antes de reusar uma página já
# vista. Sem isso, depois de um deploy o aluno continuava vendo a tela antiga
# (e o CSS antigo junto) até limpar o cache na mão.
app.add_middleware(CacheDeHtmlMiddleware)
# Comprime o HTML antes de mandar pro aluno. As páginas da plataforma têm
# bastante marcação repetida (classes do Tailwind, SVGs dos ícones), então a
# compressão costuma cortar o tamanho em ~5x — diferença grande no 4G.
# Fica DEPOIS do middleware de autenticação na lista porque, no Starlette, o
# último adicionado é o primeiro a rodar: assim a compressão é a camada mais
# externa e pega a resposta já pronta, venha ela de onde vier.
app.add_middleware(GZipMiddleware, minimum_size=500)
# Última camada adicionada, portanto a primeira a rodar e a última a tocar na
# resposta: garante que os cabeçalhos de proteção saiam em TODA resposta, até
# nos redirecionamentos do middleware de autenticação e nas páginas de erro.
app.add_middleware(CabecalhosDeSegurancaMiddleware)

app.include_router(auth_router)
app.include_router(inicio_router)
app.include_router(jogo_router)
app.include_router(jogo_suporte_router)
app.include_router(jogo_suporte_ia_router)
app.include_router(simuladores_router)
app.include_router(cursos_router)
app.include_router(materiais_router)
app.include_router(novidades_router)
app.include_router(ranking_router)
app.include_router(certificados_router)
app.include_router(perfil_router)
app.include_router(admin_dashboard_router)
app.include_router(admin_cursos_router)
app.include_router(admin_modulos_router)
app.include_router(admin_aulas_router)
app.include_router(admin_provas_router)
app.include_router(admin_alunos_router)
app.include_router(admin_filiais_router)
app.include_router(admin_materiais_router)
app.include_router(admin_novidades_router)
app.include_router(admin_avisos_router)
app.include_router(admin_destaques_router)
app.include_router(admin_duvidas_router)


@app.get("/sw.js", include_in_schema=False)
def service_worker():
    """
    Serve o service worker na raiz (não em /static/sw.js) para que o
    navegador assuma escopo "/" por padrão — igual ao "scope": "/" do
    manifest.json.
    """
    return FileResponse("static/sw.js", media_type="application/javascript")


@app.get("/healthz", response_class=PlainTextResponse)
def healthz():
    """Confirma que o processo está de pé — usado por monitores externos
    (ex: uptime checks). Não depende do banco de propósito, pra continuar
    respondendo mesmo se o Supabase estiver com problema."""
    return "ok"
