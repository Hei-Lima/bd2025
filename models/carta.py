import psycopg2
from . import colecao

class Carta:
    id: int
    id_colecao: int
    colecao_carta: colecao.Colecao | None
    nome: str
    imagem: bytearray
    conn: psycopg2.extensions.connection

    def __init__(self, id: int, id_colecao: int, nome: str, conn: psycopg2.extensions.connection, imagem=None, colecao_obj=None) -> None:
        self.id = id
        self.id_colecao = id_colecao
        self.colecao_carta = colecao_obj
        self.nome = nome
        self.conn = conn
        self.imagem = imagem

    def add(self, image=None):
        img = image if image is not None else self.imagem
        img_param = psycopg2.Binary(img) if img is not None else None

        sql = """
            INSERT INTO carta (id, id_colecao, nome, imagem)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
        """
        with self.conn.cursor() as cur:
            cur.execute(sql, (self.id, self.id_colecao, self.nome, img_param))
        self.conn.commit()

    @classmethod
    def get_all(cls, conn, pagesize: int = 20, page: int = 1, order_by: str = "id", order_dir: str = "asc", search: str = None):
        try:
            conn.rollback()  # Limpa transação anterior se houver erro
        except:
            pass
        
        offset = (max(1, int(page)) - 1) * int(pagesize)
        
        # Mapeamento das colunas
        order_columns = {
            "id": "ct.id",
            "nome": "ct.nome",
            "colecao": "cl.nome"
        }
        order_column = order_columns.get(order_by, "ct.id")
        order_direction = "DESC" if order_dir == "desc" else "ASC"
        
        sql = f"""
            SELECT ct.id, ct.id_colecao, ct.nome, ct.imagem,
                   cl.id AS cl_id, cl.nome AS cl_nome, cl.ano_lancamento
            FROM carta AS ct
            INNER JOIN colecao AS cl ON cl.id = ct.id_colecao
        """
        
        params = []
        if search:
            sql += " WHERE ct.nome ILIKE %s"
            params.append(f"%{search}%")
        
        sql += f" ORDER BY {order_column} {order_direction}"
        sql += " LIMIT %s OFFSET %s"
        params.extend([pagesize, offset])
        
        cartas = []
        with conn.cursor() as cur:
            cur.execute(sql, tuple(params))
            for row in cur.fetchall():
                id, id_colecao, nome, imagem, cl_id, cl_nome, cl_ano = row
                colecao_obj = colecao.Colecao(cl_id, cl_nome, cl_ano, conn)
                cartas.append(cls(id, id_colecao, nome, conn, imagem, colecao_obj=colecao_obj))

        return cartas
    
    @classmethod
    def get_count(cls, conn, search: str = None) -> int:
        try:
            conn.rollback()  # Limpa transação anterior se houver erro
        except:
            pass
        
        if search:
            sql = "SELECT COUNT(*) FROM carta WHERE nome ILIKE %s"
            params = (f"%{search}%",)
        else:
            sql = "SELECT COUNT(*) FROM carta"
            params = None
        
        with conn.cursor() as cur:
            if params:
                cur.execute(sql, params)
            else:
                cur.execute(sql)
            return cur.fetchone()[0]
        
    @classmethod
    def get_card(cls, conn: psycopg2.extensions.connection, id) -> "Carta | None":
        try:
            conn.rollback()
        except:
            pass
        
        sql = (
            "SELECT ct.id, ct.id_colecao, ct.nome, ct.imagem, "
            "cl.id AS cl_id, cl.nome AS cl_nome, cl.ano_lancamento "
            "FROM carta AS ct "
            "INNER JOIN colecao AS cl ON cl.id = ct.id_colecao "
            "WHERE ct.id = %s"
        )

        with conn.cursor() as cur:
            cur.execute(sql, (id,))
            row = cur.fetchone()
            if row is None:
                return None

            id, id_colecao, nome, imagem, cl_id, cl_nome, cl_ano = row
            colecao_obj = colecao.Colecao(cl_id, cl_nome, cl_ano, conn)
            return cls(id, id_colecao, nome, conn, imagem, colecao_obj=colecao_obj)