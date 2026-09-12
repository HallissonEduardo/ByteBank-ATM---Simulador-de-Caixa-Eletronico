import tkinter as tk
from tkinter import messagebox
from config import *
from models.account import AccountManager


class MainWindow:

    """
        Classe principal que controla a janela do sistema, as telas e o tempo de sessão do usuário
    """

    def __init__(self):
        self.root = tk.Tk()
        self.root.title(APP_TITLE)
        self.root.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
        self.root.configure(bg=APP_BG_COLOR)
        self.root.attributes('-fullscreen', True) # Trava tela cheia no Ubuntu
        
        self.db = AccountManager()
        self.current_frame = None
        
        # --- Configurações do Temporizador ---
        self.is_logged_in = False
        self.timer_id = None
        
        # Escuta qualquer clique ou tecla para zerar o tempo de inatividade
        self.root.bind_all("<ButtonPress>", self.reset_timer)
        self.root.bind_all("<KeyRelease>", self.reset_timer)
        
        self.show_login()

    def reset_timer(self, event=None):

        """
            Zera e reinicia a contagem regressiva de segurança
        """

        if not self.is_logged_in:
            return
            
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            
        # 30000 milissegundos = 30 segundos
        self.timer_id = self.root.after(30000, self.trigger_logout)

    def trigger_logout(self):

        """
            Desloga o usuário automaticamente
        """

        self.is_logged_in = False
        self.show_login()
        messagebox.showwarning("Sessão Expirada", "Sua sessão foi encerrada por inatividade para sua segurança.")

    def clear_frame(self):

        if self.current_frame:
            self.current_frame.destroy()


    def show_login(self):

        self.is_logged_in = False
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            
        self.clear_frame()
        from gui.login_screen import LoginScreen
        self.current_frame = LoginScreen(self.root, self)
        self.current_frame.pack(fill="both", expand=True)


    def show_menu(self, conta):

        self.is_logged_in = True
        self.reset_timer()
        
        self.clear_frame()
        from gui.menu_screen import MenuScreen
        self.current_frame = MenuScreen(self.root, self, conta)
        self.current_frame.pack(fill="both", expand=True)


    def show_saque(self, conta):

        self.reset_timer()
        self.clear_frame()
        from gui.transaction_screens import SaqueScreen
        self.current_frame = SaqueScreen(self.root, self, conta)
        self.current_frame.pack(fill="both", expand=True)


    def show_deposito(self, conta):

        self.reset_timer()
        self.clear_frame()
        from gui.transaction_screens import DepositoScreen
        self.current_frame = DepositoScreen(self.root, self, conta)
        self.current_frame.pack(fill="both", expand=True)

    def show_extrato(self, conta):

        self.reset_timer()
        self.clear_frame()
        from gui.extrato_screen import ExtratoScreen
        self.current_frame = ExtratoScreen(self.root, self, conta)
        self.current_frame.pack(fill="both", expand=True)

    def show_transferencia(self, conta):

        """
            Carrega a tela de transferências bancárias
        """

        self.reset_timer()
        self.clear_frame()

        from gui.transaction_screens import TransferenciaScreen
        self.current_frame = TransferenciaScreen(self.root, self, conta)
        self.current_frame.pack(fill="both", expand=True)


    def run(self):
        self.root.mainloop()
