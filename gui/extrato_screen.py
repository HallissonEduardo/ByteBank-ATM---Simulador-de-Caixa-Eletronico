import tkinter as tk

from gui.styles import Estilos
from config import PRIMARY_COLOR, SUCCESS_COLOR


class ExtratoScreen(tk.Frame):

    """
        Tela responsável por exibir o histórico de movimentações e o saldo atual da conta
    """

    def __init__(self, parent, controller, conta):

        super().__init__(parent, bg=parent['bg'])
        self.controller = controller
        self.conta = conta


        # Título Principal
        tk.Label(self, text="EXTRATO BANCÁRIO", **Estilos.label(titulo=True)).pack(pady=20)
        

        # Área do Extrato (Moldura Confortável)
        folha_extrato = tk.Frame(self, bg="#fafafa", bd=1, relief="solid")
        folha_extrato.pack(expand=True, fill="both", padx=60, pady=10)


        # Cabeçalhos Redimensionados para preenchimento completo
        headers_frame = tk.Frame(folha_extrato, bg="#e0e0e0")
        headers_frame.pack(fill="x", side="top")
        

        tk.Label(headers_frame, text="Data / Hora", font=("Arial", 11, "bold"), bg="#e0e0e0", fg="#444444", width=25, anchor="w").pack(side="left", padx=15, pady=8)
        tk.Label(headers_frame, text="Operação realizado", font=("Arial", 11, "bold"), bg="#e0e0e0", fg="#444444", width=25, anchor="w").pack(side="left", padx=5, pady=8)
        tk.Label(headers_frame, text="Valor Líquido", font=("Arial", 11, "bold"), bg="#e0e0e0", fg="#444444", width=20, anchor="e").pack(side="right", padx=15, pady=8)


        lista_frame = tk.Frame(folha_extrato, bg="#fafafa")
        lista_frame.pack(expand=True, fill="both", pady=10)

        if not conta.historico:
            tk.Label(lista_frame, text="Nenhuma movimentação registrada nesta conta bancária.", font=("Arial", 12, "italic"), bg="#fafafa", fg="#888888").pack(expand=True)


        else:
            # Apresenta até as 8 últimas transações de forma assíncrona
            for transacao in reversed(conta.historico[-8:]):
                linha = tk.Frame(lista_frame, bg="#fafafa")
                linha.pack(fill="x", pady=4, ipady=4)
                
                cor_valor = SUCCESS_COLOR if "recebida" in transacao.tipo or transacao.tipo == "deposito" else PRIMARY_COLOR
                sinal = "+" if "recebida" in transacao.tipo or transacao.tipo == "deposito" else "-"

                tk.Label(linha, text=transacao.timestamp, font=("Arial", 11), bg="#fafafa", fg="#262626", width=25, anchor="w").pack(side="left", padx=15)
                tk.Label(linha, text=transacao.tipo.upper(), font=("Arial", 10), bg="#fafafa", fg="#555555", width=25, anchor="w").pack(side="left", padx=5)
                tk.Label(linha, text=f"{sinal} R$ {transacao.valor:.2f}", font=("Arial", 11, "bold"), bg="#fafafa", fg=cor_valor, width=20, anchor="e").pack(side="right", padx=15)

        # Rodapé Dinâmico

        rodape = tk.Frame(folha_extrato, bg="#e0e0e0", height=50)
        rodape.pack(fill="x", side="bottom")
        tk.Label(rodape, text="SALDO DISPONÍVEL:", font=("Arial", 11, "bold"), bg="#e0e0e0", fg="#262626").pack(side="left", padx=20, pady=12)
        tk.Label(rodape, text=f"R$ {conta.saldo:.2f}", font=("Arial", 14, "bold"), bg="#e0e0e0", fg=PRIMARY_COLOR).pack(side="right", padx=20, pady=12)

        # Garantia de retorno obrigatório em todas as telas
        tk.Button(self, text="VOLTAR AO MENU", command=lambda: controller.show_menu(conta), **Estilos.botao(principal=True)).pack(pady=20)
