from config import *


class Estilos:

    """
        Classe de estilos para o sistemaCentraliza as configurações visuais dos botões,
        textos e campos de entrada da interface.
    """

    @staticmethod
    def botao(principal=False, perigo=False, saque_rapido=False):

        """
            Define e retorna as configurações visuais dos botões conforme sua função ou nível de destaque
        """

        if perigo:
            bg_color = ERROR_COLOR
            fg_color = "#ffffff"
        elif principal:
            bg_color = PRIMARY_COLOR
            fg_color = "#ffffff"
        elif saque_rapido:
            bg_color = "#e0e0e0"   # Botões de saque cinza claro
            fg_color = "#262626"
        else:
            bg_color = "#767676"
            fg_color = "#ffffff"
            
        return {
            'bg': bg_color, 'fg': fg_color, 'font': FONT_BUTTON,
            'padx': 20, 'pady': 12, 'bd': 0, 'cursor': 'hand2',
            'activebackground': "#ff3333" if principal else "#cccccc",
            'activeforeground': "#ffffff" if principal else "#262626"
        }
    

    @staticmethod
    def label(titulo=False, subtitulo=False, card=False):

        """
            Define e retorna as configurações visuais dos textos e rótulos conforme o tipo de destaque desejado.
        """

        font = FONT_TITLE if titulo else (FONT_SUBTITLE if subtitulo else FONT_TEXT)
        bg = SECONDARY_COLOR if card else APP_BG_COLOR
        return {'bg': bg, 'fg': APP_FG_COLOR, 'font': font}
    
    @staticmethod
    def entrada():
        return {
            'bg': "#ffffff", 'fg': "#262626", 'font': FONT_DIGITS,
            'insertbackground': PRIMARY_COLOR, 'bd': 1, 'relief': 'solid', 'justify': 'center'
        }
