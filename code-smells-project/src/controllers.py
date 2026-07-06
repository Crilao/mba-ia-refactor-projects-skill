from flask import jsonify, request

from src import services


def list_products():
    return jsonify({"dados": services.repo.list_products(), "sucesso": True}), 200


def search_products():
    term = request.args.get("q", "")
    category = request.args.get("categoria")
    price_min = request.args.get("preco_min")
    price_max = request.args.get("preco_max")
    if price_min is not None:
        price_min = float(price_min)
    if price_max is not None:
        price_max = float(price_max)
    results = services.repo.search_products(term, category, price_min, price_max)
    return jsonify({"dados": results, "total": len(results), "sucesso": True}), 200


def get_product(product_id):
    product = services.repo.get_product(product_id)
    if not product:
        return jsonify({"erro": "Produto não encontrado", "sucesso": False}), 404
    return jsonify({"dados": product, "sucesso": True}), 200


def create_product():
    payload, error = services.create_product(request.get_json())
    if error:
        return jsonify({"erro": error}), 400
    return jsonify({"dados": payload, "sucesso": True, "mensagem": "Produto criado"}), 201


def update_product(product_id):
    _, error = services.update_product(product_id, request.get_json())
    if error:
        return jsonify({"erro": error}), 404 if error == "Produto não encontrado" else 400
    return jsonify({"sucesso": True, "mensagem": "Produto atualizado"}), 200


def delete_product(product_id):
    _, error = services.delete_product(product_id)
    if error:
        return jsonify({"erro": error}), 404
    return jsonify({"sucesso": True, "mensagem": "Produto deletado"}), 200


def list_users():
    return jsonify({"dados": services.repo.list_users(), "sucesso": True}), 200


def get_user(user_id):
    user = services.repo.get_user(user_id)
    if not user:
        return jsonify({"erro": "Usuário não encontrado", "sucesso": False}), 404
    return jsonify({"dados": user, "sucesso": True}), 200


def create_user():
    payload, error = services.create_user(request.get_json())
    if error:
        return jsonify({"erro": error}), 409 if error == "Email já cadastrado" else 400
    return jsonify({"dados": payload, "sucesso": True}), 201


def login():
    data = request.get_json() or {}
    email = data.get("email", "")
    senha = data.get("senha", "")
    if not email or not senha:
        return jsonify({"erro": "Email e senha são obrigatórios"}), 400
    user, error = services.login(email, senha)
    if error:
        return jsonify({"erro": error, "sucesso": False}), 401
    return jsonify({"dados": user, "sucesso": True, "mensagem": "Login OK"}), 200


def create_order():
    data = request.get_json() or {}
    result, error = services.create_order(data.get("usuario_id"), data.get("itens", []))
    if error:
        return jsonify({"erro": error, "sucesso": False}), 400
    return jsonify({"dados": result, "sucesso": True, "mensagem": "Pedido criado com sucesso"}), 201


def list_orders():
    return jsonify({"dados": services.list_orders(), "sucesso": True}), 200


def list_orders_by_user(usuario_id):
    return jsonify({"dados": services.list_orders_by_user(usuario_id), "sucesso": True}), 200


def update_order_status(order_id):
    data = request.get_json() or {}
    _, error = services.update_order_status(order_id, data.get("status", ""))
    if error:
        return jsonify({"erro": error}), 400
    return jsonify({"sucesso": True, "mensagem": "Status atualizado"}), 200


def sales_report():
    return jsonify({"dados": services.sales_report(), "sucesso": True}), 200


def health_check():
    db = services.get_db()
    cursor = db.cursor()
    cursor.execute("SELECT 1")
    cursor.execute("SELECT COUNT(*) FROM produtos")
    produtos = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    usuarios = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM pedidos")
    pedidos = cursor.fetchone()[0]
    return jsonify({"status": "ok", "database": "connected", "counts": {"produtos": produtos, "usuarios": usuarios, "pedidos": pedidos}}), 200


def reset_database():
    data = request.get_json(silent=True) or {}
    token = request.headers.get("X-Admin-Token") or data.get("token", "")
    from src.config.settings import Settings

    if token != Settings.ADMIN_TOKEN:
        return jsonify({"erro": "Não autorizado"}), 401
    services.repo.clear_database()
    return jsonify({"mensagem": "Banco de dados resetado", "sucesso": True}), 200


def execute_query():
    from src.config.settings import Settings

    token = request.headers.get("X-Admin-Token", "")
    if token != Settings.ADMIN_TOKEN:
        return jsonify({"erro": "Não autorizado"}), 401
    data = request.get_json() or {}
    query = data.get("sql", "").strip()
    if not query:
        return jsonify({"erro": "Query não informada"}), 400
    if not query.upper().startswith("SELECT"):
        return jsonify({"erro": "Apenas SELECT é permitido"}), 400
    db = services.get_db()
    cursor = db.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    return jsonify({"dados": [dict(row) for row in rows], "sucesso": True}), 200
