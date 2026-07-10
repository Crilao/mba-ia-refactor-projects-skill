"""Legacy compatibility wrappers for the refactored data access layer."""

from src import repositories as repo
from src import services


get_todos_produtos = repo.list_products
get_produto_por_id = repo.get_product
criar_produto = repo.create_product
atualizar_produto = repo.update_product
deletar_produto = repo.delete_product
get_todos_usuarios = repo.list_users
get_usuario_por_id = repo.get_user
buscar_produtos = repo.search_products
relatorio_vendas = services.sales_report
atualizar_status_pedido = repo.update_order_status


def login_usuario(email, senha):
    user, error = services.login(email, senha)
    return user if not error else None


def criar_usuario(nome, email, senha, tipo="cliente"):
    payload, error = services.create_user(
        {"nome": nome, "email": email, "senha": senha, "tipo": tipo}
    )
    return payload["id"] if payload else None


def criar_pedido(usuario_id, itens):
    payload, error = services.create_order(usuario_id, itens)
    if error:
        return {"erro": error}
    return payload


def get_pedidos_usuario(usuario_id):
    return services.list_orders_by_user(usuario_id)


def get_todos_pedidos():
    return services.list_orders()
