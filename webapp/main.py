"""
Ponto de entrada da nova app (FastAPI, sem Streamlit).

Roda lado a lado com a app antiga (app.py, Streamlit) enquanto dura a
migração — ver o plano faseado combinado com o Jeferson (fases 0 a 8).
A app antiga continua no ar, sem nenhuma alteração de comportamento,
até a nova estar validada numa URL separada.

Para rodar localmente:  uvicorn webapp.main:app --reload
"""
from fastapi import FastAPI
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles

from database.repositorio import listar_cursos
from webapp.auth.routes import router as auth_router
from webapp.middleware import AutenticacaoMiddleware
from webapp.routers.admin.dashboard import router as admin_dashboard_router
from webapp.routers.certificados import router as certificados_router
from webapp.routers.cursos import router as cursos_router
from webapp.routers.inicio import router as inicio_router
from webapp.routers.materiais import router as materiais_router
from webapp.routers.perfil import router as perfil_router
from webapp.routers.ranking import router as ranking_router

app = FastAPI(title="Treinamentos Telecom (nova versão)")

# Reaproveita as mesmas pastas static/ (ícones, manifest do PWA) e assets/
# (logo) da app antiga — nenhum arquivo precisou ser duplicado.
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

app.add_middleware(AutenticacaoMiddleware)

app.include_router(auth_router)
app.include_router(inicio_router)
app.include_router(cursos_router)
app.include_router(materiais_router)
app.include_router(ranking_router)
app.include_router(certificados_router)
app.include_router(perfil_router)
app.include_router(admin_dashboard_router)


@app.get("/healthz", response_class=PlainTextResponse)
def healthz():
    """Endpoint simples pro Render (ou qualquer monitor) confirmar que o
    processo está de pé — não depende do banco."""
    return "ok"


@app.get("/healthz/banco")
def healthz_banco():
    """
    Confirma a cadeia completa: FastAPI -> repositorio.py ->
    supabase_client.py -> Supabase de verdade. Só existe pra validar a
    Fase 0 da migração (ver critério "app sobe local e consulta o banco
    real" no plano) — pode ser removido depois que o resto da app
    estiver pronto e essa verificação ficar redundante.
    """
    cursos = listar_cursos()
    return JSONResponse({"ok": True, "cursos_encontrados": len(cursos)})


@app.get("/healthz/rotas")
def healthz_rotas():
    """
    Diagnóstico temporário: lista todas as rotas realmente registradas
    nesse processo e se o middleware de autenticação está de pé. Existe só
    pra investigar um caso em que o Render marcava um deploy como "live"
    mas servia rotas de uma versão anterior do código — pode ser removido
    depois que essa dúvida for resolvida.
    """
    rotas = sorted(
        f"{','.join(sorted(r.methods))} {r.path}"
        for r in app.routes
        if hasattr(r, "methods")
    )
    return JSONResponse(
        {
            "rotas": rotas,
            "middlewares": [m.cls.__name__ for m in app.user_middleware],
        }
    )
