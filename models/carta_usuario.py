import psycopg2
from . import carta, colecao

class CartaUsuario:
    id_usuario: int
    id_carta: str
    carta_obj: carta.Carta | None
    conn: psycopg2.extensions.connection

    def __init__(self, id_usuario: int, id_carta: str, conn: psycopg2.extensions.connection, carta_obj=None) -> None:
        self.id_usuario = id_usuario
        self.id_carta = id_carta
        self.conn = conn
        self.carta_obj = carta_obj

    def add(self):
        if self.exists(self.conn, self.id_usuario, self.id_carta):
            return
        
        sql = """
            INSERT INTO cartausuario (id_usuario, id_carta)
            VALUES (%s, %s);
        """
        try:
            self.conn.rollback()
        except:
            pass
        with self.conn.cursor() as cur:
            cur.execute(sql, (self.id_usuario, self.id_carta))
        self.conn.commit()

    @classmethod
    def remove(cls, conn, id_usuario: int, id_carta: str):
        sql = 'DELETE FROM cartausuario WHERE id_usuario = %s AND id_carta = %s'
        try:
            conn.rollback()
        except:
            pass
        with conn.cursor() as cur:
            cur.execute(sql, (id_usuario, id_carta))
        conn.commit()

    @classmethod
    def exists(cls, conn, id_usuario: int, id_carta: str) -> bool:
        sql = 'SELECT 1 FROM cartausuario WHERE id_usuario = %s AND id_carta = %s'
        try:
            conn.rollback()
        except:
            pass
        with conn.cursor() as cur:
            cur.execute(sql, (id_usuario, id_carta))
            return cur.fetchone() is not None

    @classmethod
    def get_count(cls, conn, id_usuario: int) -> int:
        sql = 'SELECT COUNT(*) FROM cartausuario WHERE id_usuario = %s'
        try:
            conn.rollback()
        except:
            pass
        with conn.cursor() as cur:
            cur.execute(sql, (id_usuario,))
            return cur.fetchone()[0]

    @classmethod
    def get_all(cls, conn, id_usuario: int, pagesize: int = 20, page: int = 1):
        offset = (max(1, int(page)) - 1) * int(pagesize)
        
        sql = """
            SELECT cu.id_usuario, cu.id_carta,
                   ct.id, ct.id_colecao, ct.nome, ct.imagem,
                   cl.id AS cl_id, cl.nome AS cl_nome, cl.ano_lancamento
            FROM cartausuario cu
            INNER JOIN carta ct ON ct.id = cu.id_carta
            INNER JOIN colecao cl ON cl.id = ct.id_colecao
            WHERE cu.id_usuario = %s
            ORDER BY ct.nome ASC
            LIMIT %s OFFSET %s
        """
        
        try:
            conn.rollback()
        except:
            pass
        
        items = []
        with conn.cursor() as cur:
            cur.execute(sql, (id_usuario, pagesize, offset))
            for row in cur.fetchall():
                id_usuario, id_carta, ct_id, ct_id_colecao, ct_nome, ct_imagem, cl_id, cl_nome, cl_ano = row
                
                colecao_obj = colecao.Colecao(cl_id, cl_nome, cl_ano, conn)
                carta_obj = carta.Carta(ct_id, ct_id_colecao, ct_nome, conn, ct_imagem, colecao_obj=colecao_obj)
                
                items.append(cls(id_usuario, id_carta, conn, carta_obj=carta_obj))
        
        return items