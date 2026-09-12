
"""
    Centraliza as configurações gerais do sistema, identidade visual,
    fontes e limites das operações do caixa eletrônico.
"""


# Configurações gerais
APP_TITLE = "ByteBank ATM"
APP_WIDTH = 800
APP_HEIGHT = 600
APP_BG_COLOR = "#ffffff"       # Fundo Branco Puro
APP_FG_COLOR = "#262626"       # Texto Escuro para contraste

# Identidade Visual - Baseada no Santander (Light Mode)
PRIMARY_COLOR = "#ec0000"      # Vermelho Santander
SECONDARY_COLOR = "#f4f4f4"    # Cinza claro para painéis e cartões
ACCENT_COLOR = "#ec0000"       # Vermelho para destaques
ERROR_COLOR = "#b00020"        # Vermelho escuro para erros
SUCCESS_COLOR = "#2e7d32"      # Verde para sucesso

# Fontes
FONT_TITLE = ("Arial", 26, "bold")
FONT_SUBTITLE = ("Arial", 16, "bold")
FONT_BUTTON = ("Arial", 12, "bold")
FONT_TEXT = ("Arial", 12)
FONT_DIGITS = ("Arial", 22, "bold")

# Limites
MAX_WITHDRAWAL = 1000.0
MIN_WITHDRAWAL = 10.0
