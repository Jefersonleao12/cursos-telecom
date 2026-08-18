"""Instância única do Jinja2Templates, compartilhada por todos os routers."""
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="webapp/templates")
