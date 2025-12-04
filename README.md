# README.md

## Visão Geral
Este repositório contém uma aplicação **Flask** que usa **PostgreSQL** como banco de dados. O projeto já inclui `Dockerfile`, `docker-compose.yaml` e `requirements.txt`. Este README explica, de forma direta, como preparar o ambiente e executar a aplicação tanto **localmente** quanto com **Docker**, além de como inicializar e popular o banco de dados.

---

## Requisitos
- **Python 3.11+** (a imagem Docker usa 3.13-slim)  
- **pip** instalado  
- **Docker** e **docker-compose** se optar por containers  
- Portas **5000** e **5432** livres

**Credenciais padrão do banco**
- **user**: `postgres`  
- **password**: `postgres`  
- **database**: `postgres`

---

## Instalação local
#### 1. Criar e ativar ambiente virtual
```bash
python -m venv venv
# Linux macOS
source venv/bin/activate
# Windows PowerShell
venv\Scripts\Activate.ps1
```

#### 2. Instalar dependências
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 3. Configurar variáveis de ambiente
Crie um arquivo `.env` na raiz (opcional) com, por exemplo:
```
DB_HOST=localhost
```
Se `DB_HOST` não estiver definido, o código usa `localhost` por padrão.

#### 4. Iniciar banco de dados local
- Garanta que um servidor PostgreSQL esteja rodando e acessível em `DB_HOST` na porta `5432`.
- Se preferir, use Docker para o banco (veja seção Docker).

#### 5. Rodar a aplicação
```bash
python main.py
```
O `main.py` tenta conectar ao banco, executar `db.init(conn)` e `db.populate(conn)` para criar tabelas e popular dados de exemplo.

---

## Rodando com Docker
#### 1. Subir os serviços
```bash
docker-compose up --build
```
- O `docker-compose.yaml` define dois serviços: **db** (Postgres) e **app**.
- O serviço **app** depende de **db** e só inicia quando o banco estiver saudável.
- Portas expostas: **app** → `5000:5000`, **db** → `5432:5432`.

#### 2. Parar e remover containers
```bash
docker-compose down
```

---

## Executando e testando a aplicação
- Acesse a aplicação em: `http://localhost:5000`  
- Verifique os logs no terminal para confirmar que a conexão com o banco, a criação de tabelas e a população de dados ocorreram com sucesso.  
- Arquivos importantes:
  - **requirements.txt** para dependências Python  
  - **Dockerfile** para imagem da aplicação  
  - **docker-compose.yaml** para orquestração dos serviços  
  - Diretórios de dados e populadores: `ssds/populate` e `ssds/cartimages` (verifique se os JSONs e imagens necessários existem)

---

## Troubleshooting e notas
- **Erro de conexão com o banco**: confirme `DB_HOST`, se o Postgres está rodando e se a porta `5432` está liberada.  
- **Falha ao instalar psycopg2**: instale dependências do sistema antes de `pip install`:
```bash
# Debian Ubuntu
sudo apt-get update && sudo apt-get install -y libpq-dev gcc
```
- **Arquivos de população faltando**: a função `db.populate` depende de arquivos em `ssds/populate` e imagens em `ssds/cartimages`. Confirme que esses arquivos estão no repositório.  
- **Logs**: use os prints e o terminal do container para identificar erros. No Docker, veja logs com:
```bash
docker-compose logs -f app
```
- **Modo debug**: `main.py` inicia Flask com `debug=True` por padrão; em produção, altere essa configuração.

---

Posso gerar o conteúdo pronto do arquivo `README.md` para você copiar e colar no repositório.
