from flask_restful import Resource
from marshmallow import ValidationError
from flask import request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.schemas import agendamento_schema
from src.models.agendamento_model import AgendamentoModel
from src.services import agendamento_service
from flask_restful import Resource
from src import api


class AgendamentoList(Resource):
    @jwt_required()
    def get(self):
        """
        Lista todos os agendamentos
        ---
        tags: [Agendamento]
        security: [{Bearer: []}]
        responses:
          200: {description: Lista retornada com sucesso}
        """
        agendamentos = agendamento_service.listar_agendamento()
        schema = agendamento_schema.AgendamentoSchema(many=True)
        return make_response(jsonify(schema.dump(agendamentos)), 200)

    @jwt_required()
    def post(self):
        """
        Cria um novo agendamento
        ---
        tags: [Agendamento]
        security: [{Bearer: []}]
        parameters:
          - in: body
            name: body
            schema:
              type: object
              properties:
                data: {type: string}
                servico_id: {type: integer}
        responses:
          201: {description: Agendamento criado}
        """
        schema = agendamento_schema.AgendamentoSchema()
        try:
            dados = schema.load(request.json)
            # Adiciona o usuário logado ao agendamento se necessário
            usuario_id = get_jwt_identity()
            dados['usuario_id'] = usuario_id
            
            resultado = agendamento_service.cadastrar_agendamento(dados)
            return make_response(jsonify(schema.dump(resultado)), 201)
        except ValidationError as err:
            return make_response(jsonify(err.messages), 400)

class AgendamentoResource(Resource):
    @jwt_required()
    def get(self, id_agendamento):
        """
        Busca um agendamento por ID
        ---
        tags:
          - Agendamento
        security:
          - Bearer: []
        parameters:
          - name: id_agendamento
            in: path
            type: integer
            required: true
        responses:
          200:
            description: Agendamento encontrado com sucesso
          404:
            description: Agendamento não encontrado
        """
        agendamento = agendamento_service.listar_agendamento_id(id_agendamento)
        if not agendamento:
            return make_response(jsonify({'message': 'Não encontrado'}), 404)
        
        schema = agendamento_schema.AgendamentoSchema()
        return make_response(jsonify(schema.dump(agendamento)), 200)

    @jwt_required()
    def delete(self, id_agendamento):
        """
        Deleta um agendamento
        ---
        tags:
          - Agendamento
        security:
          - Bearer: []
        parameters:
          - name: id_agendamento
            in: path
            type: integer
            required: true
        responses:
          200:
            description: Deletado com sucesso
          404:
            description: Não encontrado
        """
        if agendamento_service.deletar_agendamento(id_agendamento):
            return make_response(jsonify({'message': 'Deletado com sucesso'}), 200)
        return make_response(jsonify({'message': 'Não encontrado'}), 404)
# Registro das rotas
api.add_resource(AgendamentoList, '/agendamentos')
api.add_resource(AgendamentoResource, '/agendamentos/<int:id_agendamento>')