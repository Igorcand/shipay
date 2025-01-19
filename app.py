from flask import Flask
from src.api.database import engine, DATABASE_URL, SessionLocal, Base
from src.api.role.controller import bp as role_blueprint
from src.api.claim.controller import bp as claim_blueprint
from src.api.user.controller import bp as user_blueprint
from flasgger import Swagger


# Função de criação do app
def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    # Registra o blueprint de roles
    app.register_blueprint(role_blueprint)
    app.register_blueprint(claim_blueprint)
    app.register_blueprint(user_blueprint)


    # Cria as tabelas no banco de dados (caso não existam)
    Base.metadata.create_all(bind=engine)

    swagger = Swagger(app)   
    return app, SessionLocal

if __name__ == '__main__':
    app, _ = create_app() 
    app.run(debug=True)
