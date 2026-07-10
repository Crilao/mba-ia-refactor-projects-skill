import os
from datetime import datetime

from flask import Flask
from flask_cors import CORS

from database import db
from routes.report_routes import report_bp
from routes.task_routes import task_bp
from routes.user_routes import user_bp

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///tasks.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', '')
app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'

CORS(app)
db.init_app(app)

app.register_blueprint(task_bp)
app.register_blueprint(user_bp)
app.register_blueprint(report_bp)

@app.route('/health')
def health():
    return {'status': 'ok', 'timestamp': datetime.utcnow().isoformat()}

@app.route('/')
def index():
    return {'message': 'Task Manager API', 'version': '1.0'}

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], host='0.0.0.0', port=int(os.getenv('PORT', '5000')))
