import tkinter as tk
from gui.styles import Estilos
from config import APP_BG_COLOR, PRIMARY_COLOR



class MenuScreen(tk.Frame):

    """
        Tela principal após o login, onde o usuário consulta o saldo e escolhe a operação que deseja realizar
    """

    def __init__(self, parent, controller, conta):

        super().__init__(parent, bg=APP_BG_COLOR)
        self.controller = controller
        self.conta = conta

        # Recupera dinamicamente o nome do titular
        nome_cliente = getattr(conta, 'titular', getattr(conta, 'nome', 'Cliente'))


        # --- Identidade Visual Santander ---
        tk.Label(self, text="ByteBank", font=("Arial", 26, "bold"), fg=PRIMARY_COLOR, bg=APP_BG_COLOR).pack(pady=(25, 2))
        tk.Label(self, text=f"Olá, {nome_cliente.upper()}", **Estilos.label(subtitulo=True)).pack(pady=(0, 2))
        tk.Label(self, text=f"Agência: 0001  |  Conta: {conta.numero}", font=("Arial", 11), fg="#666666", bg=APP_BG_COLOR).pack(pady=(0, 15))
        tk.Label(self, text=f"SALDO DISPONÍVEL: R$ {conta.saldo:.2f}", font=("Arial", 16, "bold"), fg=PRIMARY_COLOR, bg=APP_BG_COLOR).pack(pady=(0, 20))
        
        # --- Grade de Botões ---
        grid_frame = tk.Frame(self, bg=APP_BG_COLOR)
        grid_frame.pack(expand=True)

        # SOLUÇÃO DO BUG: Copia o estilo original e sobrescreve o tamanho com segurança para não dar conflito
        estilo_grande = Estilos.botao().copy()
        estilo_grande.update({
            "width": 22,
            "height": 3,
            "font": ("Arial", 14, "bold")
        })

        # Agora aplicamos o estilo preparado sem duplicar argumentos
        tk.Button(grid_frame, text="💰 SAQUE", command=lambda: controller.show_saque(conta), **estilo_grande).grid(row=0, column=0, padx=25, pady=20)
        tk.Button(grid_frame, text="📥 DEPÓSITO", command=lambda: controller.show_deposito(conta), **estilo_grande).grid(row=0, column=1, padx=25, pady=20)
        tk.Button(grid_frame, text="📄 EXTRATO", command=lambda: controller.show_extrato(conta), **estilo_grande).grid(row=1, column=0, padx=25, pady=20)
        tk.Button(grid_frame, text="💸 TRANSFERÊNCIA", command=lambda: controller.show_transferencia(conta), **estilo_grande).grid(row=1, column=1, padx=25, pady=20)

        # Retorno Seguro ao Login
        tk.Button(self, text="SAIR DA CONTA", command=controller.show_login, **Estilos.botao(principal=False)).pack(pady=35)
