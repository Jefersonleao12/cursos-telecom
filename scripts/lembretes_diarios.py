#!/usr/bin/env python3
"""
Lembrete de curso parado: roda uma vez por dia (via cron no VPS) e manda um
e-mail pra cada aluno que começou um curso e ficou alguns dias sem voltar.

Não faz parte do processo web (webapp/main.py) — é chamado separadamente
pelo cron, porque é uma tarefa periódica, não uma resposta a uma requisição.
Ver README.md para o comando do crontab.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.repositorio import cursos_parados, registrar_lembrete_enviado
from webapp.integrations.email import notificar_curso_parado

DIAS_PARA_LEMBRETE = 3


def main():
    parados = cursos_parados(dias=DIAS_PARA_LEMBRETE)
    if not parados:
        print("[lembretes] nenhum curso parado hoje.")
        return

    for item in parados:
        aluno, curso = item["aluno"], item["curso"]
        enviado = notificar_curso_parado(aluno, curso, item["dias_parado"])
        if enviado:
            registrar_lembrete_enviado(aluno["id"], curso["id"])
            print(f"[lembretes] enviado para {aluno['email']} — curso \"{curso['titulo']}\" ({item['dias_parado']}d parado)")
        else:
            print(f"[lembretes] FALHOU para {aluno['email']} — curso \"{curso['titulo']}\"")


if __name__ == "__main__":
    main()
