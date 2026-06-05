from src import db
from src.models.agendamento_model import AgendamentoModel
from datetime import datetime

def cadastrar_agendamento(agendamento):
    data = agendamento['data_hora']
    if isinstance(data, str):
        data = datetime.fromisoformat(data)

    agendamento_db = AgendamentoModel(
        data_hora=data,
        servico_id=agendamento['servico_id'],
        usuario_id=agendamento['usuario_id'],
        status=agendamento.get('status', 'agendado')
    )
    db.session.add(agendamento_db)
    db.session.commit()
    return agendamento_db

def listar_agendamento():
    return AgendamentoModel.query.all() 

def listar_agendamento_id(id):
    return AgendamentoModel.query.get(id)

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
        data = novo_agendamento['data_hora']
        if isinstance(data, str):
            data = datetime.fromisoformat(data)
            
        agendamento.data_hora = data
        agendamento.servico_id = novo_agendamento['servico_id']
        agendamento.usuario_id = novo_agendamento['usuario_id']
        agendamento.status = novo_agendamento['status']

        db.session.commit()
        return agendamento
    return None 

def listar_agendamento_usuario(usuario_id):
    return AgendamentoModel.query.filter_by(usuario_id=usuario_id).all()