from src import db

class ServicoModel(db.Model):
    __tablename__ = "servico"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(120), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    duracao_minutos = db.Column(db.Integer, nullable=False)  # duração em minutos