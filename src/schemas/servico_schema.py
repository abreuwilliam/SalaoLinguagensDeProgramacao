from src import ma
from src.models import servico_model
from marshmallow import fields

class ServicoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = servico_model.ServicoModel
        fields = ('id', 'nome', 'preco', 'duracao_minutos')

    nome =  fields.String(required=True)
    preco = fields.Float(required=True)
    duracao_minutos = fields.Integer(required=True)