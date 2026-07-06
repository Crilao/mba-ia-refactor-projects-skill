from werkzeug.security import check_password_hash, generate_password_hash

from src import repositories as repo
from src.database import get_db


VALID_CATEGORIES = ["informatica", "moveis", "vestuario", "geral", "eletronicos", "livros"]
ALLOWED_STATUSES = ["pendente", "aprovado", "enviado", "entregue", "cancelado"]


def validate_product(data):
    if not data:
        return None, "Dados inválidos"
    for field in ["nome", "preco", "estoque"]:
        if field not in data:
            return None, f"{field.capitalize()} é obrigatório"
    nome = data["nome"]
    descricao = data.get("descricao", "")
    preco = data["preco"]
    estoque = data["estoque"]
    categoria = data.get("categoria", "geral")
    if not isinstance(preco, (int, float)) or preco < 0:
        return None, "Preço não pode ser negativo"
    if not isinstance(estoque, int) or estoque < 0:
        return None, "Estoque não pode ser negativo"
    if len(nome) < 2 or len(nome) > 200:
        return None, "Nome deve ter entre 2 e 200 caracteres"
    if categoria not in VALID_CATEGORIES:
        return None, f"Categoria inválida. Válidas: {VALID_CATEGORIES}"
    return {"nome": nome, "descricao": descricao, "preco": preco, "estoque": estoque, "categoria": categoria}, None


def create_product(data):
    payload, error = validate_product(data)
    if error:
        return None, error
    product_id = repo.create_product(**payload)
    return {"id": product_id}, None


def update_product(product_id, data):
    payload, error = validate_product(data)
    if error:
        return None, error
    if not repo.get_product(product_id):
        return None, "Produto não encontrado"
    repo.update_product(product_id, **payload)
    return True, None


def delete_product(product_id):
    if not repo.get_product(product_id):
        return None, "Produto não encontrado"
    repo.delete_product(product_id)
    return True, None


def create_user(data):
    if not data:
        return None, "Dados inválidos"
    nome = data.get("nome", "").strip()
    email = data.get("email", "").strip()
    senha = data.get("senha", "")
    tipo = data.get("tipo", "cliente")
    if not nome or not email or not senha:
        return None, "Nome, email e senha são obrigatórios"
    if "@" not in email:
        return None, "Email inválido"
    if len(senha) < 4:
        return None, "Senha deve ter no mínimo 4 caracteres"
    if repo.get_user_by_email(email, include_password=True):
        return None, "Email já cadastrado"
    user_id = repo.create_user(nome, email, generate_password_hash(senha), tipo)
    return {"id": user_id}, None


def login(email, senha):
    user = repo.get_user_by_email(email, include_password=True)
    if not user or not check_password_hash(user["senha"], senha):
        return None, "Email ou senha inválidos"
    return {"id": user["id"], "nome": user["nome"], "email": user["email"], "tipo": user["tipo"]}, None


def create_order(usuario_id, items):
    if not usuario_id:
        return None, "Usuario ID é obrigatório"
    if not repo.get_user(usuario_id):
        return None, "Usuário não encontrado"
    if not items:
        return None, "Pedido deve ter pelo menos 1 item"
    db = get_db()
    cursor = db.cursor()
    try:
        total = 0
        staged_items = []
        for item in items:
            cursor.execute("SELECT * FROM produtos WHERE id = ?", (item["produto_id"],))
            product = cursor.fetchone()
            if not product:
                return None, f"Produto {item['produto_id']} não encontrado"
            if product["estoque"] < item["quantidade"]:
                return None, f"Estoque insuficiente para {product['nome']}"
            staged_items.append((product, item["quantidade"]))
            total += product["preco"] * item["quantidade"]
        order_id = repo.create_order(usuario_id, total)
        for product, quantity in staged_items:
            repo.add_order_item(order_id, product["id"], quantity, product["preco"])
            cursor.execute("UPDATE produtos SET estoque = estoque - ? WHERE id = ?", (quantity, product["id"]))
        db.commit()
        return {"pedido_id": order_id, "total": round(total, 2)}, None
    except Exception as exc:
        db.rollback()
        return None, str(exc)


def list_orders():
    return [attach_items(order) for order in repo.list_orders()]


def list_orders_by_user(user_id):
    return [attach_items(order) for order in repo.list_orders_by_user(user_id)]


def update_order_status(order_id, status):
    if status not in ALLOWED_STATUSES:
        return None, "Status inválido"
    if not repo.get_order(order_id):
        return None, "Pedido não encontrado"
    repo.update_order_status(order_id, status)
    return True, None


def attach_items(order):
    db = get_db()
    cursor = db.cursor()
    items = repo.list_order_items(order["id"])
    order["itens"] = []
    for item in items:
        cursor.execute("SELECT nome FROM produtos WHERE id = ?", (item["produto_id"],))
        product = cursor.fetchone()
        order["itens"].append(
            {
                "produto_id": item["produto_id"],
                "produto_nome": product["nome"] if product else "Desconhecido",
                "quantidade": item["quantidade"],
                "preco_unitario": item["preco_unitario"],
            }
        )
    return order


def sales_report():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM pedidos")
    total_pedidos = cursor.fetchone()[0]
    cursor.execute("SELECT SUM(total) FROM pedidos")
    faturamento = cursor.fetchone()[0] or 0
    cursor.execute("SELECT COUNT(*) FROM pedidos WHERE status = 'pendente'")
    pendentes = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM pedidos WHERE status = 'aprovado'")
    aprovados = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM pedidos WHERE status = 'cancelado'")
    cancelados = cursor.fetchone()[0]
    desconto = 0
    if faturamento > 10000:
        desconto = faturamento * 0.1
    elif faturamento > 5000:
        desconto = faturamento * 0.05
    elif faturamento > 1000:
        desconto = faturamento * 0.02
    return {
        "total_pedidos": total_pedidos,
        "faturamento_bruto": round(faturamento, 2),
        "desconto_aplicavel": round(desconto, 2),
        "faturamento_liquido": round(faturamento - desconto, 2),
        "pedidos_pendentes": pendentes,
        "pedidos_aprovados": aprovados,
        "pedidos_cancelados": cancelados,
        "ticket_medio": round(faturamento / total_pedidos, 2) if total_pedidos else 0,
    }

