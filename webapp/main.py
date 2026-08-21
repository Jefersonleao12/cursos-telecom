"""
Ponto de entrada da Plataforma de Treinamentos em Telecomunicações
(FastAPI). Roda como serviço systemd no VPS — ver scripts/setup-vps.sh.

Para rodar localmente:  uvicorn webapp.main:app --reload
"""
from fastapi import FastAPI
from fastapi.responses import FileResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles

from webapp.auth.routes import router as auth_router
from webapp.middleware import AutenticacaoMiddleware
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
from webapp.routers.admin.provas import router as admin_provas_router
from webapp.routers.certificados import router as certificados_router
from webapp.routers.cursos import router as cursos_router
from webapp.routers.inicio import router as inicio_router
from webapp.routers.jogo import router as jogo_router
from webapp.routers.materiais import router as materiais_router
from webapp.routers.perfil import router as perfil_router
from webapp.routers.ranking import router as ranking_router

app = FastAPI(title="Treinamentos Telecom")

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

app.add_middleware(AutenticacaoMiddleware)

app.include_router(auth_router)
app.include_router(inicio_router)
app.include_router(jogo_router)
app.include_router(cursos_router)
app.include_router(materiais_router)
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
