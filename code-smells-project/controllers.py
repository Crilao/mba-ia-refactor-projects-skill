"""Legacy compatibility wrappers for the refactored code-smells project."""

from src.controllers import (
    create_order as criar_pedido,
    create_product as criar_produto,
    create_user as criar_usuario,
    delete_product as deletar_produto,
    execute_query,
    get_product as buscar_produto,
    get_user as buscar_usuario,
    health_check,
    list_orders as listar_todos_pedidos,
    list_orders_by_user as listar_pedidos_usuario,
    list_products as listar_produtos,
    list_users as listar_usuarios,
    login,
    reset_database,
    sales_report as relatorio_vendas,
    search_products as buscar_produtos,
    update_order_status as atualizar_status_pedido,
    update_product as atualizar_produto,
)
