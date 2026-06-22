from flask_restful import Resource
from marshmallow import ValidationError
from flask import request, jsonify, make_response
from flask_jwt_extended import jwt_required
from src.schemas import servico_schema
from src.services import servico_service
from src import api


class ServicoList(Resource):

    @jwt_required()
    def get(self):
        """
        Lista todos os serviços
        ---
        tags:
          - Serviço
        security:
          - Bearer: []
        responses:
          200:
            description: Lista de serviços retornada com sucesso
        """
        servicos = servico_service.listar_servico()
        schema = servico_schema.ServicoSchema(many=True)
        return make_response(jsonify(schema.dump(servicos)), 200)

    @jwt_required()
    def post(self):
        """
        Cria um novo serviço
        ---
        tags:
          - Serviço
        security:
          - Bearer: []
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              properties:
                nome:
                  type: string
                  example: "Corte de cabelo"
                preco:
                  type: number
                  example: 50.0
                duracao_minutos:
                  type: integer
                  example: 30 
        responses:
          201:
            description: Serviço criado com sucesso
          400:
            description: Erro de validação
        """
        schema = servico_schema.ServicoSchema()

        try:
            dados = schema.load(request.json)
            resultado = servico_service.cadastrar_servico(dados)

            return make_response(jsonify(schema.dump(resultado)), 201)

        except ValidationError as err:
            return make_response(jsonify(err.messages), 400)


class ServicoResource(Resource):

    @jwt_required()
    def get(self, id_servico):
        """
        Busca um serviço por ID
        ---
        tags:
          - Serviço
        security:
          - Bearer: []
        parameters:
          - name: id_servico
            in: path
            type: integer
            required: true
        responses:
          200:
            description: Serviço encontrado com sucesso
          404:
            description: Serviço não encontrado
        """
        servico = servico_service.listar_servico_id(id_servico)

        if not servico:
            return make_response(jsonify({'message': 'Não encontrado'}), 404)

        schema = servico_schema.ServicoSchema()

        return make_response(jsonify(schema.dump(servico)), 200)

    @jwt_required()
    def put(self, id_servico):
        """
        Atualiza um serviço
        ---
        tags:
          - Serviço
        security:
          - Bearer: []
        parameters:
          - name: id_servico
            in: path
            type: integer
            required: true
          - in: body
            name: body
            required: true
            schema:
              type: object
              properties:
                nome:
                  type: string
                  example: "Corte de cabelo"
                preco:
                  type: number
                  example: 50.0
                duracao_minutos:
                  type: integer
                  example: 30
        responses:
          200:
            description: Serviço atualizado com sucesso
          400:
            description: Erro de validação
          404:
            description: Serviço não encontrado
        """
        schema = servico_schema.ServicoSchema()

        try:
            dados = schema.load(request.json)

            servico = servico_service.editar_servico(id_servico, dados)

            if not servico:
                return make_response(
                    jsonify({'message': 'Serviço não encontrado'}),
                    404
                )

            return make_response(jsonify(schema.dump(servico)), 200)

        except ValidationError as err:
            return make_response(jsonify(err.messages), 400)

    @jwt_required()
    def delete(self, id_servico):
        """
        Deleta um serviço
        ---
        tags:
          - Serviço
        security:
          - Bearer: []
        parameters:
          - name: id_servico
            in: path
            type: integer
            required: true
        responses:
          200:
            description: Serviço deletado com sucesso
          404:
            description: Serviço não encontrado
        """
        if servico_service.deletar_servico(id_servico):

            return make_response(
                jsonify({'message': 'Serviço deletado com sucesso'}),
                200
            )

        return make_response(
            jsonify({'message': 'Serviço não encontrado'}),
            404
        )


api.add_resource(ServicoList, '/servicos')
api.add_resource(ServicoResource, '/servicos/<int:id_servico>')