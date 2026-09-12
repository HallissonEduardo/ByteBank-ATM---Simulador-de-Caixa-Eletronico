import tkinter as tk
from tkinter import messagebox
from gui.styles import Estilos
from config import PRIMARY_COLOR

class LoginScreen(tk.Frame):

    """
        Tela de login que permite informar conta e senha usando os campos de entrada ou o teclado numérico do caixa eletrônico
    """

    def __init__(self, parent, controller):

        super().__init__(parent, bg=parent['bg'])
        self.controller = controller


        # Container Principal dividido em duas metades (Esquerda: Campos / Direita: Teclado)
        main_box = tk.Frame(self, bg=parent['bg'])
        main_box.place(relx=0.5, rely=0.5, anchor="center")


        # Coluna da Esquerda (Identidade e Inputs)
        left_col = tk.Frame(main_box, bg=parent['bg'])
        left_col.pack(side="left", padx=40)


        tk.Label(left_col, text="ByteBank", font=("Arial", 38, "bold"), fg=PRIMARY_COLOR, bg=parent['bg']).pack(pady=(0, 0))
        tk.Label(left_col, text="CAIXA ELETRÔNICO", font=("Arial", 14, "bold"), fg="#555555", bg=parent['bg']).pack(pady=(0, 25))


        tk.Label(left_col, text="Número da Conta", **Estilos.label()).pack(pady=2)
        self.ent_conta = tk.Entry(left_col, **Estilos.entrada())
        self.ent_conta.pack(pady=5, ipadx=10, ipady=3)
        self.ent_conta.focus_set() # Inicia focado aqui


        tk.Label(left_col, text="Senha do Cartão", **Estilos.label()).pack(pady=2)
        self.ent_senha = tk.Entry(left_col, show="*", **Estilos.entrada())
        self.ent_senha.pack(pady=5, ipadx=10, ipady=3)

        # Coluna da Direita (Teclado Físico do ATM)
        right_col = tk.Frame(main_box, bg="#f0f0f0", bd=1, relief="solid", padx=15, pady=15)
        right_col.pack(side="left", padx=20)

        # Grade do Teclado Numérico
        botoes_num = [
            ('1', 0, 0), ('2', 0, 1), ('3', 0, 2),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2),
            ('Limpar', 3, 0), ('0', 3, 1), ('Entrar', 3, 2)
        ]


        for (texto, linha, coluna) in botoes_num:
            if texto == 'Limpar':
                btn = tk.Button(right_col, text=texto, width=8, height=2, bg="#ffb81c", fg="#000000", font=("Arial", 10, "bold"), bd=0, command=self.limpar_campo)
            elif texto == 'Entrar':
                btn = tk.Button(right_col, text=texto, width=8, height=2, bg=PRIMARY_COLOR, fg="#ffffff", font=("Arial", 10, "bold"), bd=0, command=self.login)
            else:
                btn = tk.Button(right_col, text=texto, width=8, height=2, bg="#ffffff", fg="#262626", font=("Arial", 12, "bold"), bd=1, relief="groove", command=lambda t=texto: self.pressionar_num(t))
            
            btn.grid(row=linha, column=coluna, padx=5, pady=5)

        # Botão Administrativo de Manutenção (Canto superior)
       # tk.Button(self, text="⚙ Desligar Terminal", command=controller.root.quit, **Estilos.botao(perigo=True)).place(x=20, y=20)


    def pressionar_num(self, numero):

        """
            Insere o número no campo de texto ativo (com foco)
        """

        alvo = self.focus_get()
        if isinstance(alvo, tk.Entry):
            alvo.insert(tk.END, numero)

    def limpar_campo(self):

        """
            Limpa o campo ativo
        """

        alvo = self.focus_get()

        if isinstance(alvo, tk.Entry):
            alvo.delete(0, tk.END)


    def login(self):
        conta = self.ent_conta.get()
        senha = self.ent_senha.get()
        
        # CORRIGIDO: Removido o 'senate =' que quebrava a função
        sucesso, obj_conta = self.controller.db.autenticar(conta, senha)
        
        if sucesso:
            self.controller.show_menu(obj_conta)
        else:
            messagebox.showerror("Erro de Autenticação", "Conta ou senha incorretos.", parent=self)
