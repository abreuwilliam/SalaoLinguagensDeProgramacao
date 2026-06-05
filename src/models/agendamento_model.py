
from src import db

class AgendamentoModel(db.Model):
    __tablename__ = "agendamento"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data_hora = db.Column(db.DateTime, nullable=False)
    servico_id = db.Column(db.Integer, db.ForeignKey('servico.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='agendado')

    usuario = db.relationship('UsuarioModel', backref=db.backref('agendamentos', lazy=True))
    servico = db.relationship('ServicoModel', backref=db.backref('agendamentos', lazy=True))