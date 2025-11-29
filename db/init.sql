CREATE TABLE IF NOT EXISTS colecao (
    id SERIAL,
    nome VARCHAR(100) NOT NULL,
    ano_lancamento INTEGER,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS carta (
    id SERIAL,
    id_colecao INTEGER,
    nome VARCHAR(100) NOT NULL,
    imagem BYTEA,
    PRIMARY KEY (id),
    FOREIGN KEY (id_colecao) REFERENCES colecao(id)
);

CREATE TABLE IF NOT EXISTS administrador (
    id SERIAL,
    nome VARCHAR(100) NOT NULL,
    login VARCHAR(100) UNIQUE NOT NULL,
    senha VARCHAR(100) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS usuario (
    id SERIAL,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha VARCHAR(100) NOT NULL,
    cpf VARCHAR(11) UNIQUE NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS anuncio (
    id SERIAL,
    id_carta INTEGER,
    id_anunciante INTEGER,
    valor NUMERIC(10, 2) NOT NULL,
    imagem_frente BYTEA NULL,
    imagem_verso BYTEA NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (id_anunciante) REFERENCES usuario(id),
    FOREIGN KEY (id_carta) REFERENCES carta(id)
);

CREATE TABLE IF NOT EXISTS cartaUsuario (
    id SERIAL PRIMARY KEY,
    id_usuario INTEGER NOT NULL,
    id_carta INTEGER NOT NULL,
    extra VARCHAR(100),
    condicao VARCHAR(100),
    idioma VARCHAR(100),
    FOREIGN KEY (id_usuario) REFERENCES usuario(id),
    FOREIGN KEY (id_carta) REFERENCES carta(id)
);

CREATE TABLE IF NOT EXISTS estado(
    id SERIAL,
    nome VARCHAR(100) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS cidade(
    id SERIAL,
    id_estado INTEGER NOT NULL,
    nome VARCHAR(100) NOT NULL,
    FOREIGN KEY (id_estado) REFERENCES estado(id),
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS endereco(
    id SERIAL,
    id_usuario INTEGER,
    id_cidade INTEGER,
    cep VARCHAR(20) NOT NULL,
    tipo_logradouro VARCHAR(20) NOT NULL,
    logradouro VARCHAR(100) NOT NULL,
    numero VARCHAR(20) NOT NULL,
    bairro VARCHAR(100) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (id_usuario) REFERENCES usuario(id),
    FOREIGN KEY (id_cidade) REFERENCES cidade(id)
);

CREATE TABLE IF NOT EXISTS dadosBancarios(
    id SERIAL,
    id_usuario INTEGER,
    numero_conta VARCHAR(100) NOT NULL,
    nome_titular VARCHAR(100) NOT NULL,
    agencia VARCHAR(10) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (id_usuario) REFERENCES usuario(id)
);

CREATE TABLE IF NOT EXISTS venda (
    id SERIAL,
    id_anuncio INTEGER,
    id_comprador INTEGER,
    id_vendedor INTEGER,
    id_carta INTEGER,
    status VARCHAR(100) NOT NULL,
    data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    valor NUMERIC(10, 2) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (id_anuncio) REFERENCES anuncio(id),
    FOREIGN KEY (id_comprador) REFERENCES usuario(id),
    FOREIGN KEY (id_vendedor) REFERENCES usuario(id),
    FOREIGN KEY (id_carta) REFERENCES carta(id)
);