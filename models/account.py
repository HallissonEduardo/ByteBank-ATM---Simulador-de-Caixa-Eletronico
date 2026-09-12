import json
import os
from datetime import datetime

class Transaction:
    def __init__(self, tipo, valor, saldo_anterior, saldo_novo, detalhes=""):
        self.tipo = tipo
        self.valor = valor
        self.saldo_anterior = saldo_anterior
        self.saldo_novo = saldo_novo
        self.detalhes = detalhes
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "tipo": self.tipo, "valor": self.valor,
            "saldo_anterior": self.saldo_anterior, "saldo_novo": self.saldo_novo,
            "detalhes": self.detalhes, "timestamp": self.timestamp
        }

class Account:
    def __init__(self, numero, titular, senha, saldo=0.0):
        self.numero = numero
        self.titular = titular
        self.senha = senha
        self.saldo = saldo
        self.historico = []

    def verificar_senha(self, senha_digitada):
        return self.senha == senha_digitada

    def gerar_recibo_txt(self, tipo, valor, detalhes_extras=""):
        """Simula a impressão física de um comprovante do ATM"""
        os.makedirs("data/recibos", exist_ok=True)
        timestamp_arq = datetime.now().strftime("%Y%m%d_%H%M%S")
        timestamp_recibo = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        nome_arquivo = f"data/recibos/comprovante_{tipo}_{timestamp_arq}.txt"
        
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            f.write("========================================\n")
            f.write("               ByteBank                 \n")
            f.write(f"         COMPROVANTE: {tipo.upper()}\n")
            f.write("========================================\n")
            f.write(f"DATA/HORA: {timestamp_recibo}\n")
            f.write(f"CONTA:     {self.numero}\n")
            f.write(f"CLIENTE:   {self.titular}\n")
            if detalhes_extras:
                f.write(f"{detalhes_extras}\n")
            print("----------------------------------------\n", file=f)
            f.write(f"VALOR:     R$ {valor:.2f}\n")
            f.write(f"SALDO:     R$ {self.saldo:.2f}\n")
            f.write("----------------------------------------\n")
            f.write(f" TXT ID:   {timestamp_arq}\n")
            f.write("========================================\n")

    def sacar(self, valor):
        if valor <= 0: return False, "Valor inválido"
        if valor > self.saldo: return False, "Saldo insuficiente"
        
        saldo_antigo = self.saldo
        self.saldo -= valor
        self.historico.append(Transaction("saque", valor, saldo_antigo, self.saldo))
        self.gerar_recibo_txt("saque", valor)
        return True, f"Saque de R$ {valor:.2f} realizado."

    def depositar(self, valor):
        if valor <= 0: return False, "Valor inválido"
        
        saldo_antigo = self.saldo
        self.saldo += valor
        self.historico.append(Transaction("deposito", valor, saldo_antigo, self.saldo))
        self.gerar_recibo_txt("deposito", valor)
        return True, f"Depósito de R$ {valor:.2f} realizado."

    def transferir(self, valor, conta_destino):
        if valor <= 0: return False, "Valor inválido"
        if valor > self.saldo: return False, "Saldo insuficiente"
        if self.numero == conta_destino.numero: return False, "Não é possível transferir para si mesmo"
        
        saldo_antigo_origem = self.saldo
        saldo_antigo_destino = conta_destino.saldo
        
        self.saldo -= valor
        conta_destino.saldo += valor
        
        # Registra histórico detalhado em ambas as contas
        self.historico.append(Transaction("transferência enviada", valor, saldo_antigo_origem, self.saldo, f"Para: {conta_destino.titular} (CC {conta_destino.numero})"))
        conta_destino.historico.append(Transaction("transferência recebida", valor, saldo_antigo_destino, conta_destino.saldo, f"De: {self.titular} (CC {self.numero})"))
        
        self.gerar_recibo_txt("transferência", valor, f"DESTINO:   {conta_destino.numero} - {conta_destino.titular}")
        return True, f"Transferência de R$ {valor:.2f} enviada para {conta_destino.titular}."

class AccountManager:
    def __init__(self):
        os.makedirs("data", exist_ok=True)
        self.arquivo = "data/accounts.json"
        self.contas = {}
        self.carregar_contas()

    def carregar_contas(self):
        try:
            with open(self.arquivo, 'r') as f:
                dados = json.load(f)
                for num, info in dados.items():
                    conta = Account(num, info['titular'], info['senha'], info['saldo'])
                    # Reconstrói histórico básico se houver persistência futura estendida
                    self.contas[num] = conta
        except FileNotFoundError:
            self._criar_contas_padrao()

    def _criar_contas_padrao(self):
        contas_teste = {
            "001": {"titular": "João Silva", "senha": "1234", "saldo": 5000.00},
            "002": {"titular": "Maria Santos", "senha": "5678", "saldo": 3500.00}
        }
        for num, info in contas_teste.items():
            self.contas[num] = Account(num, info['titular'], info['senha'], info['saldo'])
        self.salvar_contas()

    def salvar_contas(self):
        dados = {}
        for num, conta in self.contas.items():
            dados[num] = {"titular": conta.titular, "senha": conta.senha, "saldo": conta.saldo}
        with open(self.arquivo, 'w') as f:
            json.dump(dados, f, indent=2)

    def autenticar(self, numero, senha):
        conta = self.contas.get(numero)
        if conta and conta.verificar_senha(senha):
            return True, conta
        return False, None
