import math
import base64
from flask import Blueprint, current_app, render_template, abort, request, redirect, url_for
from models import carta, colecao, carta_usuario

bp = Blueprint("controller", __name__)

# Usuário fixo (simulando login)
CURRENT_USER_ID = 1

@bp.route("/")
def index():
    conn = current_app.config.get("db_conn")
    if conn is None:
        abort(500, description="DB connection not configured")
    
    page = request.args.get("page", 1, type=int)
    pagesize = request.args.get("pagesize", 20, type=int)
    order_by = request.args.get("order_by", "id", type=str)
    order_dir = request.args.get("order_dir", "asc", type=str)
    search = request.args.get("search", "", type=str)
    
    page = max(1, page)
    pagesize = max(1, min(pagesize, 100))
    
    if order_by not in ["id", "nome", "colecao"]:
        order_by = "id"
    if order_dir not in ["asc", "desc"]:
        order_dir = "asc"
    
    total_cartas = carta.Carta.get_count(conn, search=search if search else None)
    total_paginas = math.ceil(total_cartas / pagesize) if total_cartas > 0 else 1
    cartas = carta.Carta.get_all(conn, pagesize, page, order_by=order_by, order_dir=order_dir, search=search if search else None)
    
    for c in cartas:
        if c.imagem:
            c.imagem_b64 = base64.b64encode(bytes(c.imagem)).decode('utf-8')
        else:
            c.imagem_b64 = None
    
    return render_template(
        "index.html",
        cartas=cartas,
        page=page,
        pagesize=pagesize,
        total_cartas=total_cartas,
        total_paginas=total_paginas,
        order_by=order_by,
        order_dir=order_dir,
        search=search
    )


@bp.route("/card")
def card():
    conn = current_app.config.get("db_conn")
    if conn is None:
        abort(500, description="DB connection not configured")
    
    card_id = request.args.get("id", type=str)
    if not card_id:
        abort(400, description="Card ID is required")
    
    c = carta.Carta.get_card(conn, card_id)
    if c is None:
        abort(404, description="Card not found")
    
    if c.imagem:
        c.imagem_b64 = base64.b64encode(bytes(c.imagem)).decode('utf-8')
    else:
        c.imagem_b64 = None
    
    na_colecao = carta_usuario.CartaUsuario.exists(conn, CURRENT_USER_ID, card_id)
    
    return render_template("card.html", carta=c, na_colecao=na_colecao)


@bp.route("/card/add", methods=["POST"])
def card_add_to_collection():
    conn = current_app.config.get("db_conn")
    if conn is None:
        abort(500, description="DB connection not configured")
    
    card_id = request.form.get("id", type=str)
    if not card_id:
        abort(400, description="Card ID is required")
    
    cu = carta_usuario.CartaUsuario(CURRENT_USER_ID, card_id, conn)
    cu.add()
    
    return redirect(url_for("controller.card", id=card_id))


@bp.route("/card/remove", methods=["POST"])
def card_remove_from_collection():
    conn = current_app.config.get("db_conn")
    if conn is None:
        abort(500, description="DB connection not configured")
    
    card_id = request.form.get("id", type=str)
    if not card_id:
        abort(400, description="Card ID is required")
    
    carta_usuario.CartaUsuario.remove(conn, CURRENT_USER_ID, card_id)
    
    return redirect(url_for("controller.card", id=card_id))


@bp.route("/colecao")
def colecao_usuario():
    conn = current_app.config.get("db_conn")
    if conn is None:
        abort(500, description="DB connection not configured")
    
    page = request.args.get("page", 1, type=int)
    pagesize = request.args.get("pagesize", 20, type=int)
    
    page = max(1, page)
    pagesize = max(1, min(pagesize, 100))
    
    total_cartas = carta_usuario.CartaUsuario.get_count(conn, CURRENT_USER_ID)
    total_paginas = math.ceil(total_cartas / pagesize) if total_cartas > 0 else 1
    items = carta_usuario.CartaUsuario.get_all(conn, CURRENT_USER_ID, pagesize, page)
    
    for item in items:
        if item.carta_obj and item.carta_obj.imagem:
            item.carta_obj.imagem_b64 = base64.b64encode(bytes(item.carta_obj.imagem)).decode('utf-8')
        elif item.carta_obj:
            item.carta_obj.imagem_b64 = None
    
    return render_template(
        "colecao.html",
        items=items,
        page=page,
        pagesize=pagesize,
        total_cartas=total_cartas,
        total_paginas=total_paginas
    )
