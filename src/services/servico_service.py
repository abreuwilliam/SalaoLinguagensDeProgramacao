from src import db
from src.models.servico_model import ServicoModel


def cadastrar_servico(servico):
    servico_db = ServicoModel(
        nome=servico['nome'],
        preco=servico['preco'],
        duracao_minutos=servico['duracao_minutos']
    )
    db.session.add(servico_db)
    db.session.commit()
    return servico_db


def listar_servico():
    return ServicoModel.query.all()


def listar_servico_id(id):
    return ServicoModel.query.get(id)


def editar_servico(id, dados):
    servico = ServicoModel.query.get(id)
    if servico:
        servico.nome = dados['nome']
        servico.preco = dados['preco']
        servico.duracao_minutos = dados['duracao_minutos']
        db.session.commit()
        return servico
    return None


def deletar_servico(id):
    servico = ServicoModel.query.get(id)
    if servico:
        db.session.delete(servico)
        db.session.commit()
        return True
    return False
