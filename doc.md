# ByteBank ATM

## 1. Visão Geral do Projeto

O **ByteBank ATM** é uma aplicação desktop desenvolvida em Python com interface gráfica via Tkinter. Seu propósito é simular de forma realista as operações de um caixa eletrônico.

O software foi projetado com foco em terminais de autoatendimento (**Kiosk Mode**) e atua como a aplicação principal de uma remasterização acadêmica do sistema operacional **Linux Ubuntu 26 LTS**.

---

## 2. Arquitetura do Sistema

O projeto utiliza uma arquitetura baseada no padrão de **separação de responsabilidades**, dividindo a interface gráfica, a regra de negócio e a persistência de dados.

### Estrutura de Diretórios

- **`/gui` — Interface Gráfica:**  
  Contém todas as telas do sistema. Gerencia o que o usuário vê e como ele interage.

- **`/models` — Regras de Negócio:**  
  Contém as lógicas de movimentação de dinheiro, registro de histórico e contas bancárias.

- **`/data` — Persistência:**  
  Diretório gerado automaticamente para armazenar o "banco de dados" em JSON (`accounts.json`) e os comprovantes gerados (`/recibos`).

- **`main.py` e `config.py`:**  
  Arquivos localizados na raiz do projeto, responsáveis por iniciar a aplicação e centralizar as configurações globais, respectivamente.

---

## 3. Módulos e Classes Principais

### 3.1. Gerenciamento de Contas e Lógica (`models/account.py`)

- **Classe `Account`:**  
  Representa a conta de um cliente. É responsável por validar senhas e executar as operações financeiras isoladas (`sacar`, `depositar`, `transferir`). Também aciona a geração dos recibos físicos em arquivos `.txt`.

- **Classe `Transaction`:**  
  Modelo de dados responsável por estruturar cada operação, contendo informações como tipo, valor, saldo anterior, saldo novo e timestamp, formando o histórico do extrato.

- **Classe `AccountManager`:**  
  Atua como um mini banco de dados. Carrega e salva as informações no arquivo `accounts.json`, além de cuidar da autenticação (login).

### 3.2. Interface e Navegação (`gui/`)

- **`main_window.py` / `BancoApp`:**  
  É o "cérebro" da navegação. Controla qual tela está visível e gerencia o **Cronômetro de Segurança (Timeout)**.

- **`styles.py`:**  
  Centraliza a identidade visual, incluindo cores, fontes e estilos de botões, mantendo a padronização baseada no Design System escolhido (**Santander Light Mode**).

- **`transaction_screens.py`:**  
  Utiliza o conceito de **Herança** da Programação Orientada a Objetos. A classe `BaseTransactionScreen` cria o teclado numérico padrão, enquanto as telas filhas (`SaqueScreen` e `DepositoScreen`) implementam apenas a ação final de cada operação.

---

## 4. Regras de Negócio Implementadas

1. **Autenticação Restrita:**  
   O acesso ao menu só é permitido mediante a combinação correta de Número da Conta e Senha.

2. **Validação de Saldo:**  
   Operações de Saque e Transferência bloqueiam valores que excedam o saldo disponível.

3. **Segurança por Inatividade (Timeout):**  
   Se o terminal ficar **30 segundos** sem receber cliques ou interações de teclado, a sessão do usuário é imediatamente encerrada e o sistema retorna à tela de login.

4. **Registro de Transações Duplas:**  
   Nas transferências, o sistema gera o histórico detalhado tanto na conta de origem (dinheiro enviado) quanto na conta de destino (dinheiro recebido).

---

## 5. Integração com o Sistema Operacional (Ubuntu)

Para garantir o funcionamento em modo terminal de autoatendimento, o sistema implementa travas no nível do Sistema Operacional:

- **Tela Cheia Obrigatória:**  
  O método `self.attributes('-fullscreen', True)` garante que a aplicação cubra toda a área de trabalho.

- **Bloqueio de Saída:**  
  Comandos como `WM_DELETE_WINDOW` e a tecla `<Escape>` foram interceptados para impedir que o usuário feche a aplicação acidentalmente ou acesse o ambiente Linux por trás do caixa eletrônico.

- **Feedback Sonoro:**  
  Integração com o pacote `canberra-gtk-play`, nativo do Linux, para emitir sons a cada tecla pressionada no teclado numérico virtual.

---

## 6. Autoria e Contatos

- **Desenvolvedor:** Hallisson Eduardo Pires da Silva
- **Contato:** [hallissonedu08@gmail.com](mailto:hallissonedu08@gmail.com)