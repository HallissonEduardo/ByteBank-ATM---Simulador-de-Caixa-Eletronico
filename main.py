import tkinter as tk
from config import APP_BG_COLOR
from models.account import AccountManager

# Importação das telas do ecossistema visual
from gui.login_screen import LoginScreen
from gui.menu_screen import MenuScreen
from gui.transaction_screens import SaqueScreen, DepositoScreen, TransferenciaScreen
from gui.extrato_screen import ExtratoScreen


class BancoApp(tk.Tk):

    """
        Classe principal que inicializa o caixa eletrônico, controla as telas,
        o cronômetro de segurança e o fluxo de navegação do sistema.
    """

    def __init__(self):
        super().__init__()
        
        self.title("ByteBank")
        self.configure(bg=APP_BG_COLOR)
        
        # --- 1. Inicialização do Banco de Dados Real ---
        self.db = AccountManager() 
        
        # --- 2. Container Principal ---
        self.container = tk.Frame(self, bg=APP_BG_COLOR)
        self.container.pack(expand=True, fill="both")
        
        self.tela_atual = None
        self.timer_inatividade = None # Guarda a referência do cronômetro de 30s

        # --- 3. Vigia de Inatividade (Global) ---
        # Qualquer clique de mouse ou tecla pressionada chama o reset do cronômetro
        self.bind_all("<Any-ButtonPress>", self.resetar_cronometro)
        self.bind_all("<Any-KeyPress>", self.resetar_cronometro)
        
        # --- 4. Ativação do Kiosk Mode Inteligente ---
        self.after(100, lambda: self.attributes('-fullscreen', True))
        self.protocol("WM_DELETE_WINDOW", self.bloquear_saida)
        self.bind("<Escape>", lambda event: "break")

        # Inicializa o Caixa na Tela de Login
        self.show_login()

    def iniciar_cronometro(self):

        """
            Inicia a contagem regressiva de 30 segundos (30000 milissegundos)
        """

        self.parar_cronometro()
        # Se passar 30 segundos sem interrupção, desloga o usuário
        self.timer_inatividade = self.after(30000, self.encerrar_sessao_por_timeout)

    def parar_cronometro(self):

        """
            Cancela o cronômetro atual se ele existir
        """

        if self.timer_inatividade:
            self.after_cancel(self.timer_inatividade)
            self.timer_inatividade = None

    def resetar_cronometro(self, event=None):

        """
            Zera o cronômetro a cada ação do usuário (mas apenas se estiver logado)
        """

        if self.tela_atual and not isinstance(self.tela_atual, LoginScreen):
            self.iniciar_cronometro()

    def encerrar_sessao_por_timeout(self):

        """
            Corta o acesso e joga o sistema de volta para a tela inicial de segurança
        """

        if self.tela_atual and not isinstance(self.tela_atual, LoginScreen):
            self.show_login()

    def mudar_tela(self, classe_tela, *args):

        """
            Gerenciador de fluxo de telas
        """

        if self.tela_atual is not None:
            self.tela_atual.destroy()
        
        self.tela_atual = classe_tela(self.container, self, *args)
        self.tela_atual.pack(expand=True, fill="both")


    # --- Rotas de Navegação ---
    def show_login(self):

        self.parar_cronometro() # Não precisa contar tempo na tela de login vazia
        self.mudar_tela(LoginScreen)


    def show_menu(self, conta):

        self.mudar_tela(MenuScreen, conta)
        self.iniciar_cronometro() # Começa a contar assim que entra no menu


    def show_saque(self, conta):

        self.mudar_tela(SaqueScreen, conta)
        self.iniciar_cronometro()


    def show_deposito(self, conta):

        self.mudar_tela(DepositoScreen, conta)
        self.iniciar_cronometro()

    def show_extrato(self, conta):

        self.mudar_tela(ExtratoScreen, conta)
        self.iniciar_cronometro()

    def show_transferencia(self, conta):
        self.mudar_tela(TransferenciaScreen, conta)
        self.iniciar_cronometro()

    def bloquear_saida(self):
        pass

if __name__ == "__main__":
    app = BancoApp()
    app.mainloop()
