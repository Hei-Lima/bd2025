import psycopg2
import json
from models import colecao, carta
import os
import sys

images_dir = "db/cardimages"


def connect(user: str, password: str, db_name: str, host: str = "localhost"):
    conn = psycopg2.connect(
        host=host,
        database=db_name,
        user=user,
        password=password
    )
    return conn

selfconn: psycopg2.extensions.connection = None

def init(conn: psycopg2.extensions.connection = selfconn, sql_path="db/init.sql"):
    with open(sql_path, "r", encoding="utf-8") as f:
        sql = f.read()

    with conn.cursor() as cur:
        cur.execute(sql)
    conn.commit()
    
    # cria usuário padrão para testes
    create_default_user(conn)

def create_default_user(conn):
    sql = """
        INSERT INTO usuario (id, nome, email, senha, cpf)
        VALUES (1, 'Usuário Teste', 'teste@teste.com', '123456', '12345678901')
        ON CONFLICT (id) DO NOTHING;
    """
    with conn.cursor() as cur:
        cur.execute(sql)
    conn.commit()

def populate(conn: psycopg2.extensions.connection = selfconn):
    populate_sets(conn)
    populate_cards(conn)

def populate_sets(conn: psycopg2.extensions.connection = selfconn):
    with open("db/populate/sets_converted.json", "r", encoding="utf-8") as f:
        sets = json.load(f)
        for set in sets:
            id = set["id"]
            nome = set["label"]["en"]
            ano_lancamento = int(set["releaseDate"][:4])
            c = colecao.Colecao(id, nome, ano_lancamento, conn)
            c.add()

def populate_cards(conn: psycopg2.extensions.connection = selfconn):
    with open("db/populate/cards_converted.json", "r", encoding="utf-8") as f:
        cards = json.load(f)
        for card in cards:
            id = card["id"]
            id_colecao = card["set"]
            nome = card["label"]["eng"]
            image_path = card["imageName"]
            c = carta.Carta(id, id_colecao, nome, conn)
            c.add(get_image(image_path))

def get_image(p):
    if not p:
        return None

    # já são bytes
    if isinstance(p, (bytes, bytearray)):
        return bytes(p)

    # tenta caminho absoluto/relativo direto primeiro
    candidate = p
    if not os.path.isabs(candidate):
        candidate = os.path.join(images_dir, p)

    if not os.path.isfile(candidate):
        # fallback: se p for um caminho relativo diferente, tenta diretamente
        if os.path.isfile(p):
            candidate = p
        else:
            print(f"[AVISO] Imagem não encontrada: {p}", file=sys.stderr)
            return None

    with open(candidate, "rb") as f:
        return f.read()
