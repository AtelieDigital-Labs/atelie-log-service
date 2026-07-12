# 🛡️ Microsserviço de Auditoria de Logs - Ateliê Digital

## 📖 Sobre o Projeto
O **Ateliê Digital** é um sistema web que funciona como um marketplace exclusivo para produtos artesanais. O objetivo da plataforma é conectar diretamente os artesãos independentes aos consumidores, oferecendo ferramentas para que os vendedores gerenciem seus negócios e os clientes encontrem produtos com facilidade e segurança.

Neste repositório encontra-se o microsserviço de **Auditoria de Logs**. Dentro da arquitetura orientada a eventos do sistema, este serviço é o principal responsável por garantir a rastreabilidade, compliance e segurança operacional. Ele opera de forma desacoplada, escutando eventos e mensagens disparadas pelos demais serviços do core do projeto através de mensageria assíncrona, registrando cada alteração crítica de forma imutável e estruturada em banco de dados.

Apesar de ser um serviço passivo no fluxo da jornada de compra do usuário, a Auditoria desempenha um papel fundamental para o ecossistema, consolidando o histórico de alterações dos serviços de *Catalog*, *Accounts* e *Orders*, além de fornecer uma interface administrativa para consulta e geração de relatórios de auditoria.

---

## 🎯 Escopo de Auditoria

O serviço monitora eventos emitidos pelos três microsserviços centrais do **Ateliê Digital**. Abaixo estão detalhadas as tabelas, ações e atributos monitorados em cada contexto:

### 🛍️ 1. Catalog (Catálogo de Produtos e Lojas)
Responsável pelo cadastro, exibição e gerenciamento dos produtos artesanais e informações das lojas dos artesãos.
* **`ProductVariation`** — `UPDATE` *(Atributo monitorado: **stock**)*  
  *Rastreabilidade de movimentação e alteração no estoque dos produtos.*
* **`ProductVariation`** — `UPDATE` *(Atributo monitorado: **price**)*  
  *Registro do histórico de variação de preços das variações.*
* **`Product`** — `UPDATE` *(Atributo monitorado: **is_deleted**)*  
  *Auditoria de exclusão lógica (Soft Delete) de produtos do catálogo.*
* **`Address`** — `UPDATE`  
  *Monitoramento de alterações no endereço cadastrado para a loja do artesão.*

### 📦 2. Orders (Pedidos e Carrinho)
Gerencia o fluxo de carrinho de compras, checkout e processamento dos pedidos dos clientes.
* **`Order`** — `INSERT`  
  *Auditoria de criação de novos pedidos na plataforma.*
* **`Order`** — `UPDATE` *(Atributo monitorado: **status**)*  
  *Rastreamento das mudanças de ciclo de vida do pedido (ex: Pendente, Pago, Enviado, Entregue, Cancelado).*

### 👤 3. Accounts (Usuários, Autenticação e Carteira)
Gerencia a identidade, autenticação dos usuários e as transações financeiras das carteiras dos artesãos.
* **`User`** — `INSERT` e `UPDATE`  
  *Auditoria de criação de contas e atualizações de dados de perfil.*
* **`Wallet`** — `INSERT` e `UPDATE`  
  *Registro da criação de carteiras para artesãos e alterações de saldo/status.*
* **`WalletTransaction`** — `INSERT` e `UPDATE`  
  *Rastreamento rigoroso de todas as movimentações financeiras de entrada.*
* **`Wallet`** — `SELECT`  
  *Auditoria de acesso à informação: monitora tanto consultas individuais a uma carteira quanto a listagem de carteiras (visando segurança e detecção de acessos indevidos a dados sensíveis).*

---

## 🏗️ Estrutura de Armazenamento da Auditoria

Os logs recebidos são estruturados e persistidos no banco de dados relacional tirando proveito de tipos avançados como `JSONB` para flexibilidade nos deltas de alteração, mantendo índices otimizados para consultas temporais e por entidade.

Abaixo está a definição dos dados da tabela de auditoria implementada com **SQLAlchemy 2.0**:

```python
    log_id: Mapped[int] 
    event_id: Mapped[str] # log_id único do evento
    user_id: Mapped[str] # ID do autor da ação 
    entity_type: Mapped[str] # Nome do recurso auditado 
    entity_id: Mapped[str] # ID do recurso alterado 
    service_source: Mapped[str] # Origem do evento 
    action: Mapped[str] # Tipo de operação (INSERT, UPDATE, SELECT, DELETE)
    delta: Mapped[Dict[str, Any]] # Objeto JSON com as mudanças 
    reason: Mapped[str] # Motivo ou contexto da operação
    event_timestamp: Mapped[datetime] # Data/hora original do evento
    ingested_at: Mapped[datetime] # Data/hora de processamento no serviço

    Index('ix_audit_logs_user_entity', 'user_id', 'entity_type'),
    Index('ix_audit_logs_time_service', 'event_timestamp', 'service_source')
    
```

---

## 📊 Dashboard Administrativo e Relatórios

Para possibilitar a análise visual e a extração de evidências, o serviço disponibiliza uma interface administrativa interativa utilizando **Starlette Admin**.

* **Acesso:** O painel fica disponível diretamente na rota `/admin/` do serviço.
* **Funcionalidades:**
  * **Visualização Avançada:** Navegação intuitiva com suporte a filtros dinâmicos por serviço de origem (`service_source`), tipo de entidade (`entity_type`), identificador da entendidade (`entity_id`), usuário (`user_id`), ação (`action`) e intervalos de data (`event_timestamp`).
  * **Inspeção de Diferenciais (Deltas):** Visualização clara do payload em formato JSON demonstrando exatamente o estado anterior e posterior das propriedades alteradas.
  * **Exportação de Relatórios:** Capacidade nativa de extrair os registros de logs filtrados em múltiplos formatos de arquivo para fins de compliance e relatórios externos:
    * 📑 **.PDF** (Documentos paginados para relatórios formais)
    * 📈 **.XLSX** (Planilhas Excel para auditorias analíticas)
    * 📄 **.CSV** (Arquivos de texto separado por vírgula para processamento em outras ferramentas)

---

## 🚀 Tecnologias e Recursos
Este microsserviço foi construído focando em alta performance de ingestão assíncrona e confiabilidade no armazenamento, utilizando as seguintes tecnologias:

* **FastStream com RabbitMQ:** Framework moderno e ultrarrápido para mensageria assíncrona, responsável por consumir os eventos emitidos nas filas do RabbitMQ sem bloquear a thread principal.
* **FastAPI:** Framework web para estruturação da aplicação e disponibilização do painel admin.
* **PostgreSQL:** Banco de dados relacional robusto para armazenamento permanente dos registros de auditoria.
* **psycopg:** Driver PostgreSQL moderno e de altíssimo desempenho para Python, com excelente suporte ao tipo nativo JSONB.
* **itsdangerous:** Biblioteca para envio de dados com segurança.
* **Starlette Admin:** Biblioteca para geração do dashboard administrativo de visualização e exportação de relatórios.
* **Ferramentas de Suporte:**
    * **uv:** Gerenciador de pacotes e ambientes virtuais ultrarrápido.
    * **Alembic:** Ferramenta robusta de migração de banco de dados
    * **Ruff:** Linter e formatador de código para manter o padrão de qualidade e PEP 8.
    * **Taskipy:** Executor de tarefas para automatizar scripts e comandos rotineiros no terminal.

---

## ⚙️ Configuração do Ambiente

Para rodar este projeto no seu ambiente local, utilizaremos o **uv** para gerenciar as dependências e o ambiente virtual de forma otimizada.

### 1. Instalação do uv
Caso ainda não tenha o `uv` instalado em sua máquina, abra o terminal e execute o comando de acordo com o seu sistema operacional:

**No Linux (ou macOS):**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**No Windows (PowerShell):**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Criando o Ambiente Virtual
Na pasta raiz do projeto de auditoria, crie um ambiente virtual limpo executando:
```bash
uv venv
```

Após a criação, **ative o ambiente virtual**:
* **Linux / macOS:**
    ```bash
    source .venv/bin/activate
    ```
* **Windows:**
    ```cmd
    .venv\Scripts\activate
    ```

### 3. Instalando as Bibliotecas
Com o ambiente virtual ativo, instale todas as dependências do projeto com o comando:

```bash
uv pip install -r requirements.txt
```

*Caso deseje instalar as principais bibliotecas manualmente, execute:*
```bash
uv pip install faststream[rabbitmq] fastapi uvicorn sqlalchemy psycopg starlette-admin pytest ruff taskipy alembic
```

---

## ▶️ Como Executar o Serviço

Você pode rodar o serviço em modo local de desenvolvimento diretamente via terminal ou de forma conteinerizada utilizando o Docker Compose para emular o ecossistema completo do Ateliê Digital.

### Opção 1: Execução Local 
Com o ambiente virtual ativado e as variáveis de ambiente (como conexão do banco de dados e URL do RabbitMQ) configuradas no arquivo `.env`, execute o comando:

```bash
fastapi dev main.py
```

### Opção 2: Execução via Docker Compose (Recomendado)
Para integrar o serviço de auditoria aos demais microsserviços do **Ateliê Digital** (como o RabbitMQ e o banco de dados PostgreSQL), a execução via Docker Compose garante que todos os containers compartilhem a mesma rede de comunicação interna.

1. **Crie a rede de comunicação global do projeto** (caso ainda não tenha sido criada no seu ambiente docker):
   ```bash
   docker network create atelie-network
   ```

2. **Inicie o serviço construindo a imagem do container**:
   Na raiz do repositório, execute o comando abaixo para realizar o build da imagem Docker e subir o serviço em background ou anexado ao terminal:
   ```bash
   docker compose up --build
   ```

Com o container em execução, o serviço começará automaticamente a escutar os eventos do RabbitMQ na rede `atelie-network` e o painel administrativo estará acessível no navegador através de `http://localhost:8000/admin/` (ou na porta configurada em seu `docker-compose.yml`).
