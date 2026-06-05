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
        tags:
          - Agendamento
        security:
          - Bearer: []
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              properties:
                data_hora: {type: string, format: date-time, example: "2026-06-10T14:30:00"}
                servico_id: {type: integer, example: 1}
                usuario_id: {type: integer, example: 1}
                status: {type: string, example: "Agendado"}
        responses:
          201: {description: Agendamento criado com sucesso}
          400: {description: Erro de validação}
        """
        schema = agendamento_schema.AgendamentoSchema()
        try:
            dados = schema.load(request.json)
        
            dados['usuario_id'] = int(dados['usuario_id'])
            
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
    @jwt_required()
    def put(self, id_agendamento):
        """
        Atualiza um agendamento existente
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
          - in: body
            name: body
            required: true
            schema:
              type: object
              properties:
                data_hora: {type: string, format: date-time, example: "2026-06-10T14:30:00"}
                servico_id: {type: integer, example: 1}
                usuario_id: {type: integer, example: 1}
                status: {type: string, example: "Agendado"}
        responses:
          200:
            description: Agendamento atualizado com sucesso
          404:
            description: Agendamento não encontrado
          400:
            description: Erro de validação
        """
        schema = agendamento_schema.AgendamentoSchema()
        try:
            dados = schema.load(request.json)
            
            dados['usuario_id'] = int(dados['usuario_id'])
            
            agendamento_atualizado = agendamento_service.editar_agendamento(id_agendamento, dados)
            
            if not agendamento_atualizado:
                return make_response(jsonify({'message': 'Agendamento não encontrado'}), 404)
            
            return make_response(jsonify(schema.dump(agendamento_atualizado)), 200)
            
        except ValidationError as err:
            return make_response(jsonify(err.messages), 400)

api.add_resource(AgendamentoList, '/agendamentos')
api.add_resource(AgendamentoResource, '/agendamentos/<int:id_agendamento>')