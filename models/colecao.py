import psycopg2

class Colecao:
    id: int
    nome: str
    ano_lancamento: int
    conn: psycopg2.extensions.connection

    def __init__(self, id: int, nome: str, ano_lancamento: int, conn: psycopg2.extensions.connection) -> None:
        self.id = id
        self.nome = nome
        self.ano_lancamento = ano_lancamento
        self.conn = conn

    def add(self):
        sql = """
            INSERT INTO colecao (id, nome, ano_lancamento)
            VALUES (%s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
        """
        with self.conn.cursor() as cur:
            cur.execute(sql, (self.id, self.nome, self.ano_lancamento))
        self.conn.commit()