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

app = FastAPI(title="Treinamentos Telecom (nova versão)")

# Reaproveita a mesma pasta static/ da app antiga (ícones e manifest do
# PWA) — nenhum arquivo precisou ser duplicado.
app.mount("/static", StaticFiles(directory="static"), name="static")


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
