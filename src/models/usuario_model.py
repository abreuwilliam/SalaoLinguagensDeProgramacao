

from src import db
from passlib.context import CryptContext

class UsuarioModel(db.Model):
    __tablename__ = "usuario"


    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    senha = db.Column(db.String(255), nullable=False)
    

    pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

    def gen_senha(self, senha):
        self.senha = self.pwd_context.hash(senha)

     
        

    def verifica_senha(self, senha):
        return self.pwd_context.verify(senha, self.senha)
    

