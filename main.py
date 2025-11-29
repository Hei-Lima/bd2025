from flask import Flask
import os
import db.db as db
from dotenv import load_dotenv
from controller import controller

load_dotenv()

# Sim, em plaintext. Não é uma api séria, porra!
user = "postgres"
password = "postgres"
db_name = "postgres"
# No Docker, o host é o nome do serviço "db", não "localhost"
db_host = os.environ.get("DB_HOST") or "localhost"

print(f"Conectando ao banco em: {db_host}")

# Inicialização do DB e criação do objeto conn
conn = db.connect(user, password, db_name, host=db_host)
db.init(conn)
db.populate(conn)

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev"

app.config["db_conn"] = conn
app.register_blueprint(controller.bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)