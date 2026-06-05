from src import ma
from src.models import agendamento_model
from marshmallow import fields

class ServicoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = agendamento_model.AgendamentoModel
        filds = ('id', 'data_hora', 'servico_id', 'usuario_id', 'status')

        id = fields.Integer(dump_only=True)
        data_hora = fields.DateTime(required=True)
        servico_id = fields.Integer(required=True)
        usuario_id = fields.Integer(required=True)
        status = fields.String(required=True)