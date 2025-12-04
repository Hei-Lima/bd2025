# README.md

## Visão Geral
Este repositório contém uma aplicação **Flask** que usa **PostgreSQL** como banco de dados. O projeto já inclui `Dockerfile`, `docker-compose.yaml` e `requirements.txt`. Este README explica, de forma direta, como preparar o ambiente e executar a aplicação tanto **localmente** quanto com **Docker**, além de como inicializar e popular o banco de dados.

---

## Requisitos
- **Docker** e **docker-compose** se optar por containers
  
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
