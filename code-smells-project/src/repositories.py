from src.database import get_db


def product_to_dict(row):
    return {
        "id": row["id"],
        "nome": row["nome"],
        "descricao": row["descricao"],
        "preco": row["preco"],
        "estoque": row["estoque"],
        "categoria": row["categoria"],
        "ativo": row["ativo"],
        "criado_em": row["criado_em"],
    }


def user_to_dict(row, include_password=False):
    data = {
        "id": row["id"],
        "nome": row["nome"],
        "email": row["email"],
        "tipo": row["tipo"],
        "criado_em": row["criado_em"],
    }
    if include_password:
        data["senha"] = row["senha"]
    return data


def order_to_dict(row):
    return {
        "id": row["id"],
        "usuario_id": row["usuario_id"],
        "status": row["status"],
        "total": row["total"],
        "criado_em": row["criado_em"],
        "itens": [],
    }


def list_products():
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM produtos")
    return [product_to_dict(row) for row in cursor.fetchall()]


def get_product(product_id):
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM produtos WHERE id = ?", (product_id,))
    row = cursor.fetchone()
    return product_to_dict(row) if row else None


def search_products(term="", category=None, price_min=None, price_max=None):
    query = "SELECT * FROM produtos WHERE 1=1"
    params = []
    if term:
        query += " AND (nome LIKE ? OR descricao LIKE ?)"
        like = f"%{term}%"
        params.extend([like, like])
    if category:
        query += " AND categoria = ?"
        params.append(category)
    if price_min is not None:
        query += " AND preco >= ?"
        params.append(price_min)
    if price_max is not None:
        query += " AND preco <= ?"
        params.append(price_max)
    cursor = get_db().cursor()
    cursor.execute(query, params)
    return [product_to_dict(row) for row in cursor.fetchall()]


def create_product(nome, descricao, preco, estoque, categoria):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO produtos (nome, descricao, preco, estoque, categoria) VALUES (?, ?, ?, ?, ?)",
        (nome, descricao, preco, estoque, categoria),
    )
    db.commit()
    return cursor.lastrowid


def update_product(product_id, nome, descricao, preco, estoque, categoria):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        """
        UPDATE produtos
        SET nome = ?, descricao = ?, preco = ?, estoque = ?, categoria = ?
        WHERE id = ?
        """,
        (nome, descricao, preco, estoque, categoria, product_id),
    )
    db.commit()


def delete_product(product_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM produtos WHERE id = ?", (product_id,))
    db.commit()


def list_users():
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM usuarios")
    return [user_to_dict(row) for row in cursor.fetchall()]


def get_user(user_id, include_password=False):
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM usuarios WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    return user_to_dict(row, include_password=include_password) if row else None


def get_user_by_email(email, include_password=False):
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
    row = cursor.fetchone()
    return user_to_dict(row, include_password=include_password) if row else None


def create_user(nome, email, hashed_password, tipo="cliente"):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO usuarios (nome, email, senha, tipo) VALUES (?, ?, ?, ?)",
        (nome, email, hashed_password, tipo),
    )
    db.commit()
    return cursor.lastrowid


def create_order(usuario_id, total):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO pedidos (usuario_id, status, total) VALUES (?, 'pendente', ?)",
        (usuario_id, total),
    )
    return cursor.lastrowid


def add_order_item(pedido_id, produto_id, quantidade, preco_unitario):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        """
        INSERT INTO itens_pedido (pedido_id, produto_id, quantidade, preco_unitario)
        VALUES (?, ?, ?, ?)
        """,
        (pedido_id, produto_id, quantidade, preco_unitario),
    )


def list_orders():
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM pedidos")
    return [order_to_dict(row) for row in cursor.fetchall()]


def list_orders_by_user(user_id):
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM pedidos WHERE usuario_id = ?", (user_id,))
    return [order_to_dict(row) for row in cursor.fetchall()]


def get_order(order_id):
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM pedidos WHERE id = ?", (order_id,))
    row = cursor.fetchone()
    return order_to_dict(row) if row else None


def list_order_items(order_id):
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM itens_pedido WHERE pedido_id = ?", (order_id,))
    return cursor.fetchall()


def update_order_status(order_id, status):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("UPDATE pedidos SET status = ? WHERE id = ?", (status, order_id))
    db.commit()


def clear_database():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM itens_pedido")
    cursor.execute("DELETE FROM pedidos")
    cursor.execute("DELETE FROM produtos")
    cursor.execute("DELETE FROM usuarios")
    db.commit()

