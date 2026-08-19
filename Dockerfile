# Imagem pro Hugging Face Space (SDK "Docker") — roda a app nova (webapp/,
# FastAPI), a mesma que está em produção no Render. "python -m uvicorn" em
# vez de só "uvicorn" de propósito: evita a mesma pegadinha de PATH que
# apareceu no corte de produção do Render (ver render.yaml).
FROM python:3.11-slim

WORKDIR /app

COPY requirements-webapp.txt .
RUN pip install --no-cache-dir -r requirements-webapp.txt

COPY database/ database/
COPY utils/ utils/
COPY modules/__init__.py modules/__init__.py
COPY modules/whatsapp.py modules/whatsapp.py
COPY webapp/ webapp/
COPY static/ static/
COPY assets/ assets/

# Hugging Face Spaces espera a app respondendo na porta 7860.
EXPOSE 7860

CMD ["python", "-m", "uvicorn", "webapp.main:app", "--host", "0.0.0.0", "--port", "7860"]
