from src import db
from ..models.agendamento_model import AgendamentoModel
from ..schemas.agendamento_schema import ServicoSchema
from flask import jsonify

def cadastrar_agendamento(agendamento):
    agendamento_db = AgendamentoModel(
        data_hora=agendamento.data_hora,
        servico_id=agendamento.servico_id,
        usuario_id=agendamento.usuario_id,
        status=agendamento.status
    )
    db.session.add(agendamento_db)
    db.session.commit()
    return agendamento_db

def listar_agendamento():
    return AgendamentoModel.query.all() 

def listar_agendamento_id(id):
    agendamento_encontrado = AgendamentoModel.query.get(id)
    return agendamento_encontrado

def deletar_agendamento(id):
    agendamento = AgendamentoModel.query.get(id)
    if agendamento:
        db.session.delete(agendamento)
        db.session.commit()
        return True
    return False

def editar_agendamento(id, novo_agendamento):
    agendamento = AgendamentoModel.query.get(id)
    if agendamento:
        agendamento.data_hora = novo_agendamento['data_hora']
        agendamento.servico_id = novo_agendamento['servico_id']
        agendamento.usuario_id = novo_agendamento['usuario_id']
        agendamento.status = novo_agendamento['status']

        db.session.commit()
        return agendamento
    return None 
def listar_agendamento_usuario(usuario_id):
    return AgendamentoModel.query.filter_by(usuario_id=usuario_id).all()    