import tkinter as tk
import os
from tkinter import messagebox
from gui.styles import Estilos
from config import PRIMARY_COLOR, APP_BG_COLOR


class BaseTransactionScreen(tk.Frame):

    """
        Classe base responsável por reunir a estrutura e os comportamentos comuns às telas de transações bancárias.
    """

    def __init__(self, parent, controller, conta, titulo):
        super().__init__(parent, bg=APP_BG_COLOR)
        self.controller = controller
        self.conta = conta

        tk.Label(self, text=titulo, **Estilos.label(titulo=True)).pack(pady=20)

        self.main_container = tk.Frame(self, bg=APP_BG_COLOR)
        self.main_container.pack(expand=True, fill="both", padx=40)

        # Mantém o Teclado Numérico Lateral do Layout Original
        self.pad_frame = tk.Frame(self.main_container, bg="#f0f0f0", bd=1, relief="solid", padx=15, pady=15)
        self.pad_frame.pack(side="right", padx=40, pady=20)

        botoes = [
            ('1', 0, 0), ('2', 0, 1), ('3', 0, 2),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2),
            ('Limpar', 3, 0), ('0', 3, 1), ('Confirma', 3, 2)
        ]

        for (texto, l, c) in botoes:
            if texto == 'Limpar':
                b = tk.Button(self.pad_frame, text=texto, width=8, height=2, bg="#ffb81c", font=("Arial", 10, "bold"), bd=0, command=self.limpar)
            elif texto == 'Confirma':
                b = tk.Button(self.pad_frame, text=texto, width=8, height=2, bg="#2e7d32", fg="#ffffff", font=("Arial", 10, "bold"), bd=0, command=self.confirmar_com_loading)
            else:
                b = tk.Button(self.pad_frame, text=texto, width=8, height=2, bg="#ffffff", font=("Arial", 12, "bold"), bd=1, relief="groove", command=lambda t=texto: self.inserir_num(t))
            b.grid(row=l, column=c, padx=4, pady=4)


    def tocar_som(self):
        os.system("canberra-gtk-play --id='button-pressed' &")


    def inserir_num(self, num):
        self.tocar_som()
        alvo = self.focus_get()
        if isinstance(alvo, tk.Entry):
            alvo.insert(tk.END, num)


    def limpar(self):
        self.tocar_som()
        alvo = self.focus_get()
        if isinstance(alvo, tk.Entry):
            alvo.delete(0, tk.END)

    def confirmar_com_loading(self):

        """
            Bloqueia a tela temporariamente e exibe a mensagem de comunicação com o banco
        """

        self.tocar_som()
        alvo_valor = getattr(self, 'ent_valor', None)
        
        if alvo_valor and not alvo_valor.get().strip():
            messagebox.showerror("Erro de Entrada", "Por favor, preencha o valor antes de confirmar.", parent=self)
            return

        # Painel de transição interno
        self.loading_frame = tk.Frame(self, bg="#ffffff", bd=1, relief="solid")
        self.loading_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Interação solicitada: "Checando o banco..."
        lbl = tk.Label(self.loading_frame, text="⏳ Checando o banco...\nPor favor, aguarde o processamento.", 
                       font=("Arial", 16, "bold"), fg=PRIMARY_COLOR, bg="#ffffff")
        lbl.pack(expand=True)

        # Aguarda 2 segundos e chama a execução do banco de dados
        self.after(2000, self.finalizar_loading)


    def finalizar_loading(self):

        if hasattr(self, 'loading_frame'):
            self.loading_frame.destroy()
        self.executar()


    def ejecutar(self):
        pass # Fallback estrutural


    def executar(self):
        pass


class SaqueScreen(BaseTransactionScreen):


    def __init__(self, parent, controller, conta):
        super().__init__(parent, controller, conta, "SAQUE")
        
        left_frame = tk.Frame(self.main_container, bg=APP_BG_COLOR)
        left_frame.pack(side="left", expand=True, fill="both", padx=20)

        tk.Label(left_frame, text="Digite o valor do Saque:", **Estilos.label(subtitulo=True)).pack(pady=10)
        self.ent_valor = tk.Entry(left_frame, **Estilos.entrada())
        self.ent_valor.pack(pady=10, ipady=5)
        self.ent_valor.focus_set()

        tk.Button(left_frame, text="VOLTAR AO MENU", command=lambda: controller.show_menu(conta), **Estilos.botao()).pack(pady=30)


    def executar(self):

        try:
            val = float(self.ent_valor.get())
            sucesso, msg = self.conta.sacar(val)
            if sucesso:
                self.controller.db.salvar_contas()
                messagebox.showinfo("Sucesso", msg, parent=self)
                self.controller.show_menu(self.conta)
            else:
                messagebox.showerror("Erro", msg, parent=self)
        except ValueError:
            messagebox.showerror("Erro", "Insira um valor numérico válido.", parent=self)


class DepositoScreen(BaseTransactionScreen):

    def __init__(self, parent, controller, conta):
        super().__init__(parent, controller, conta, "DEPÓSITO")
        
        left_frame = tk.Frame(self.main_container, bg=APP_BG_COLOR)
        left_frame.pack(side="left", expand=True, fill="both", padx=20)

        tk.Label(left_frame, text="Digite o valor do Depósito:", **Estilos.label(subtitulo=True)).pack(pady=10)
        self.ent_valor = tk.Entry(left_frame, **Estilos.entrada())
        self.ent_valor.pack(pady=10, ipady=5)
        self.ent_valor.focus_set()

        tk.Button(left_frame, text="VOLTAR AO MENU", command=lambda: controller.show_menu(conta), **Estilos.botao()).pack(pady=30)


    def executar(self):

        try:
            val = float(self.ent_valor.get())
            sucesso, msg = self.conta.depositar(val)
            if sucesso:
                self.controller.db.salvar_contas()
                messagebox.showinfo("Sucesso", msg, parent=self)
                self.controller.show_menu(self.conta)
            else:
                messagebox.showerror("Erro", msg, parent=self)
        except ValueError:
            messagebox.showerror("Erro", "Insira um valor numérico válido.", parent=self)



class TransferenciaScreen(BaseTransactionScreen):

    def __init__(self, parent, controller, conta):
        super().__init__(parent, controller, conta, "TRANSFERÊNCIA")
        
        left_frame = tk.Frame(self.main_container, bg=APP_BG_COLOR)
        left_frame.pack(side="left", expand=True, fill="both", padx=20)

        tk.Label(left_frame, text="Conta do Destinatário:", **Estilos.label()).pack(pady=(10, 2))
        self.ent_destino = tk.Entry(left_frame, **Estilos.entrada())
        self.ent_destino.pack(pady=5, ipady=3)
        self.ent_destino.focus_set()

        tk.Label(left_frame, text="Valor da Transferência (R$):", **Estilos.label()).pack(pady=(15, 2))
        self.ent_valor = tk.Entry(left_frame, **Estilos.entrada())
        self.ent_valor.pack(pady=5, ipady=3)

        tk.Button(left_frame, text="VOLTAR AO MENU", command=lambda: controller.show_menu(conta), **Estilos.botao()).pack(pady=30)

    def executar(self):
        num_destino = self.ent_destino.get()
        try:
            val = float(self.ent_valor.get())
            manager = self.controller.db
            conta_dest = manager.contas.get(num_destino)
            
            if not conta_dest:
                messagebox.showerror("Erro", "Conta de destino não localizada.", parent=self)
                return
                
            sucesso, msg = self.conta.transferir(val, conta_dest)
            if sucesso:
                manager.salvar_contas()
                messagebox.showinfo("Sucesso", msg, parent=self)
                self.controller.show_menu(self.conta)
            else:
                messagebox.showerror("Erro", msg, parent=self)
        except ValueError:
            messagebox.showerror("Erro", "Preencha os campos com valores válidos.", parent=self)
