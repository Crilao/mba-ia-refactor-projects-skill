from flask import Blueprint

from src import controllers


api = Blueprint("api", __name__)

api.add_url_rule("/produtos", "listar_produtos", controllers.list_products, methods=["GET"])
api.add_url_rule("/produtos/busca", "buscar_produtos", controllers.search_products, methods=["GET"])
api.add_url_rule("/produtos/<int:product_id>", "buscar_produto", controllers.get_product, methods=["GET"])
api.add_url_rule("/produtos", "criar_produto", controllers.create_product, methods=["POST"])
api.add_url_rule("/produtos/<int:product_id>", "atualizar_produto", controllers.update_product, methods=["PUT"])
api.add_url_rule("/produtos/<int:product_id>", "deletar_produto", controllers.delete_product, methods=["DELETE"])
api.add_url_rule("/usuarios", "listar_usuarios", controllers.list_users, methods=["GET"])
api.add_url_rule("/usuarios/<int:user_id>", "buscar_usuario", controllers.get_user, methods=["GET"])
api.add_url_rule("/usuarios", "criar_usuario", controllers.create_user, methods=["POST"])
api.add_url_rule("/login", "login", controllers.login, methods=["POST"])
api.add_url_rule("/pedidos", "criar_pedido", controllers.create_order, methods=["POST"])
api.add_url_rule("/pedidos", "listar_todos_pedidos", controllers.list_orders, methods=["GET"])
api.add_url_rule("/pedidos/usuario/<int:usuario_id>", "listar_pedidos_usuario", controllers.list_orders_by_user, methods=["GET"])
api.add_url_rule("/pedidos/<int:order_id>/status", "atualizar_status_pedido", controllers.update_order_status, methods=["PUT"])
api.add_url_rule("/relatorios/vendas", "relatorio_vendas", controllers.sales_report, methods=["GET"])
api.add_url_rule("/health", "health_check", controllers.health_check, methods=["GET"])
api.add_url_rule("/admin/reset-db", "reset_database", controllers.reset_database, methods=["POST"])
api.add_url_rule("/admin/query", "executar_query", controllers.execute_query, methods=["POST"])

