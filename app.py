from flask import Flask, render_template
from models import db
from auth import auth_bp
from vehicles import vehicles_bp
from reservations import reservations_bp

def create_app():
    app = Flask(__name__)

    # Configurações básicas
    app.config["SECRET_KEY"] = "uma_chave_segura_qualquer"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Inicializar a base de dados
    db.init_app(app)

    # Registar blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(vehicles_bp)
    app.register_blueprint(reservations_bp)

    # Página inicial → pesquisa de veículos
    @app.route("/")
    def index():
        return render_template("search.html")

    return app

# Só corre o servidor se este ficheiro for executado diretamente
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
