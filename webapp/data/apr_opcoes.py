"""
Opções fixas do formulário de APR (Análise Preliminar de Risco) do
Simulador de Campo — baseadas no formulário real usado pelo provedor.
Ficam separadas da lógica (webapp/services/jogo_campo.py) e do gabarito
de cada O.S. (campo "apr_gabarito" em webapp/data/jogo_campo_missoes.py),
seguindo o mesmo padrão do restante do jogo.
"""

ATIVIDADES = [
    "Instalação, manutenção ou retirada de rede Fibra Optica",
    "Infraestrutura de Fibra",
    "Infraestrutura de torre",
    "Ampliação ou manutenção CTO",
    "Manutenção de cabo drop",
    "Instalação ou mudança de endereço fibra optica",
    "Instalação ou mudança de endereço via à rádio",
    "Manutenção casa do cliente (internet lenta, sem internet, configuração)",
]

RISCOS = [
    "Presença de corrente elétrica nas partes metálicas do poste",
    "Transformador com defeito ou aterramento (Perigo de descarga elétrica)",
    "Fiação exposta ou cabos soltos, Cruzetas ou Roldanas danificadas",
    "Cordoalha metálica ou Drop Metálico energizado",
    "Existência de ligações clandestinas",
    "Rede elétrica baixa ou com catenária irregular",
    "Maquinário danificado ou sem proteção elétrica",
    "Rede da Telecomunicação fora da ABNT",
    "Uso de adornos (Ex.: Aliança, Corrente, Crachá, Relógio...)",
]
RISCO_NENHUM = "Não há"

EPIS = [
    "Calçados de proteção",
    "Capacete de proteção classe A tipo II com jugular",
    "Cinto tipo paraquedas com ancoragem dorsal, torácica, ponto de ancoragem para posicionamento e suspensão",
    "Luvas de vaqueta ou tátil black",
    "Óculos de proteção contra impactos e raios uv",
    "Trava quedas 12mm",
    "Corda para trabalhos em altura de poliéster 12mm",
    "Talabarte de posicionamento",
    "Mosquetão (D) assimétrico",
    "Fita de ancoragem 1,5 metros",
    "Luva isolante elétrica",
]
EPI_NENHUM = "Não há necessidade"
