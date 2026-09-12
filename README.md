# Desenvolvimento de um Terminal de Autoatendimento Bancário Seguro: Aplicação de *OS Hardening* e *Interface Kiosk*

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-yellow)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey)
![Ubuntu](https://img.shields.io/badge/OS-Ubuntu%2026%20LTS-orange)
![License](https://img.shields.io/badge/license-MIT-green)

## Sumário

- [Resumo](#1-resumo-abstract)
- [Introdução e Justificativa](#2-introdução-e-justificativa)
- [Arquitetura e Metodologia](#3-arquitetura-e-metodologia)
  - [Infraestrutura e Sistema Operacional](#31-infraestrutura-e-sistema-operacional-customização-da-iso)
  - [Lógica de Negócios e Persistência](#32-lógica-de-negócios-e-persistência-back-end-em-python-poo)
  - [Interface Gráfica](#33-interface-gráfica-front-end-em-python-tkinter)
- [Mecanismos de Segurança Implementados](#4-mecanismos-de-segurança-implementados)
- [Como Executar](#5-como-executar-instruções-da-iso)
- [Considerações Finais e Referências](#6-considerações-finais-e-referências)

---

## 1. Resumo (Abstract)

Este projeto descreve a concepção e o desenvolvimento de um simulador de Caixa Eletrônico (ATM) focado em alta segurança. O sistema utiliza uma versão remasterizada do Ubuntu Linux (26 LTS) para operar em ambiente restrito, empregando técnicas avançadas de isolamento operacional. A aplicação principal foi construída com interface gráfica em Python Tkinter e lógica de negócios estruturada em Programação Orientada a Objetos (POO), acoplada a um banco de dados SQLite local para persistência de dados. O objetivo principal é demonstrar um ambiente imune a intervenções físicas externas através do bloqueio de periféricos de entrada não autorizados, limitando a interação estritamente ao uso do mouse em um teclado virtual, e da redução drástica dos recursos do sistema operacional.

## 2. Introdução e Justificativa

Terminais de autoatendimento (ATMs) são alvos constantes de ataques físicos e lógicos, exigindo camadas rigorosas de segurança. A construção deste projeto baseia-se na necessidade de mitigar vulnerabilidades em nível de Sistema Operacional (SO) e de aplicação.

O projeto justifica-se pela aplicação de três conceitos fundamentais da segurança da informação:

- **OS Hardening (Endurecimento de Sistema):** processo de garantir que o sistema operacional execute estritamente o necessário. O sistema base foi despojado de serviços irrelevantes (como gerenciadores de rede e conectividade) para evitar escalonamento de privilégios e ataques remotos.
- **Redução da Superfície de Ataque:** ao desabilitar portas USB e o uso do teclado físico, o vetor de ataque local é praticamente eliminado, impedindo a injeção de *malwares* via *hardware* ou a execução de atalhos de sistema.
- **Interface Kiosk:** o ambiente de desktop padrão (Gnome) foi substituído pelo Openbox, configurado para aprisionar o usuário final unicamente na tela da aplicação, sem barra de tarefas, atalhos de janela ou menus de contexto.

## 3. Arquitetura e Metodologia

O projeto foi dividido em camadas de *software* independentes e uma camada de infraestrutura de Sistema Operacional isolada.

### 3.1. Infraestrutura e Sistema Operacional (Customização da ISO)

A base do ambiente é uma ISO customizada do Ubuntu 26 LTS, construída e homologada em máquina virtual (VirtualBox). A edição da imagem do sistema foi realizada utilizando a ferramenta **Cubic** (Custom Ubuntu ISO Creator).

A metodologia de endurecimento incluiu:

- Substituição do ambiente Gnome pelo gerenciador de janelas **Openbox**, configurado via `~/.config/openbox/autostart` para inicializar o aplicativo em modo tela cheia (*fullscreen*), limitando a interação do usuário apenas à janela do caixa.
- Criação de um usuário inicial com permissões severamente restritas, incapaz de executar comandos administrativos (`sudo`).
- Remoção em massa de pacotes não essenciais, isolando o terminal de qualquer rede externa.
- Desabilitação via *kernel/udev* dos mapeamentos de teclado, restringindo a interação física estritamente ao uso do clique esquerdo do *mouse*.

### 3.2. Lógica de Negócios e Persistência (Back-end em Python POO)

O núcleo financeiro do simulador (presente no módulo `models/account.py`) foi estruturado utilizando Programação Orientada a Objetos em Python.

- **Encapsulamento em Memória:** os dados sensíveis da conta são protegidos como atributos privados da classe, garantindo que o front-end interaja com os dados apenas por meio de métodos validados, evitando corrupção de estado.
- **Persistência de Dados Offline (SQLite):** como o sistema opera de forma isolada e sem conexões de rede, todas as transações, saldos e históricos são registrados de forma segura e local utilizando um banco de dados SQLite, garantindo a integridade dos registros mesmo após a reinicialização da máquina.

### 3.3. Interface Gráfica (Front-end em Python Tkinter)

A interface de usuário foi concebida de forma modular no diretório `gui/`, separando responsabilidades:

- **Módulos Independentes:** telas específicas gerenciam contextos isolados, como `login_screen.py`, `menu_screen.py`, `extrato_screen.py` e `transaction_screens.py`. O módulo `main_window.py` serve como orquestrador de janelas.
- **Teclado Virtual Seguro:** devido à ausência de teclado físico por restrições de SO, a interface Tkinter implementa um teclado numérico/alfanumérico virtual na própria tela. A entrada de dados (como senhas e valores de saque) é realizada exclusivamente através de cliques com o botão esquerdo do *mouse*.

## 4. Mecanismos de Segurança Implementados

- Isolamento de interface gráfica em modo Kiosk com Openbox (*fullscreen* obrigatório).
- Bloqueio em nível de *kernel/OS* para portas USB e teclado físico.
- Desativação de *daemons* e serviços de rede para operação *offline*.
- Armazenamento local autônomo através de banco de dados SQLite.
- Sanitização e encapsulamento de estado da aplicação em Python (POO).
- Inicialização da aplicação ligada a um usuário sem privilégios administrativos.

## 5. Como Executar (Instruções da ISO)

1. Faça o *download* da ISO customizada do sistema.
2. Crie uma nova Máquina Virtual no VirtualBox.
3. Aloque um mínimo de 2GB de RAM e 1 VCPU.
4. Anexe a ISO como disco de *boot*.
5. Inicie a máquina. O sistema fará o *logon* automático no usuário restrito e, através do *autostart* do Openbox, executará o interpretador Python chamando o arquivo `main.py` em tela cheia.


## 💿 ISO do Ubuntu Customizada

O ByteBank ATM faz parte de um ecossistema maior, sendo o software principal de uma distribuição Linux remasterizada.
- **Download da ISO:** [Clique aqui para baixar a ISO do Ubuntu 26 LTS Customizado](https://drive.google.com/drive/folders/1uvSzPTsW___l3kGXn5YfClX2yKXkoyHY?usp=sharing)

## 💻 Como executar o projeto localmente

### Pré-requisitos
Certifique-se de ter o Python 3.x instalado em sua máquina. O projeto utiliza o `tkinter`, que geralmente já vem embutido nas instalações padrão do Python.

### Passos para execução
1. Clone este repositório:
   ```bash
   git clone [https://github.com/HallissonEduardo/ByteBank-ATM---Simulador-de-Caixa-Eletronico.git](https://github.com/HallissonEduardo/ByteBank-ATM---Simulador-de-Caixa-Eletronico.git)

> **Nota:** o uso do teclado físico estará inoperante pela configuração de segurança. Toda a navegação e digitação de valores deve ser feita pelo teclado virtual na tela usando o botão esquerdo do mouse.

## 6. Considerações Finais e Referências

O projeto alcança seu objetivo ao demonstrar na prática como a combinação de boas práticas de engenharia de *software* (Python POO + SQLite) com a configuração agressiva de sistema operacional (*Hardening* em Linux) pode criar dispositivos de uso público altamente resilientes a invasões físicas.

**Referências:**

- ISO/IEC 27001 — Tecnologia da Informação — Técnicas de Segurança.
- Documentação Oficial do Python (PEP 8, Tkinter, SQLite3).
- Documentação do Openbox e Ubuntu OS.