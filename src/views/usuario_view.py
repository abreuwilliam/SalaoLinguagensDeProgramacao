from flask_restful import Resource
from marshmallow import ValidationError
from flask import request, jsonify, make_response

from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    get_jwt_identity
)

from src.schemas import usuario_schema
from src.models.usuario_model import UsuarioModel
from src.services import usuario_service
from src import api


class UsuarioList(Resource):

    @jwt_required()
    def get(self):
        """
        Lista todos os usuários
        ---
        tags:
          - Usuários

        security:
          - Bearer: []

        responses:
          200:
            description: Lista de usuários retornada com sucesso

          401:
            description: Token não enviado ou inválido

          404:
            description: Não existe usuários cadastrados
        """

        usuarios = usuario_service.listar_usuario()

        if not usuarios:
            return make_response(
                jsonify({
                    "message": "Não existe usuarios!"
                }),
                404
            )

        schema = usuario_schema.UsuarioSchema(many=True)

        return make_response(
            jsonify(schema.dump(usuarios)),
            200
        )



    def post(self):
        """
        Cadastra um novo usuário
        ---
        tags:
          - Usuários

        parameters:
          - in: body
            name: body
            required: true

            schema:
              type: object

              properties:
                nome:
                  type: string
                  example: William

                email:
                  type: string
                  example: william@gmail.com

                senha:
                  type: string
                  example: "123456"

        responses:
          201:
            description: Usuário criado com sucesso

          400:
            description: Erro de validação ou e-mail já cadastrado
        """

        schema = usuario_schema.UsuarioSchema()

        try:
            dados = schema.load(request.json)

        except ValidationError as err:
            return make_response(
                jsonify(err.messages),
                400
            )

        if usuario_service.listar_usuario_email(dados['email']):

            return make_response(
                jsonify({
                    'message': 'E-mail já cadastrado.'
                }),
                400
            )

        try:

            novo_usuario = UsuarioModel(
                nome=dados['nome'],
                email=dados['email']
            )

            # GERA HASH DA SENHA
            novo_usuario.gen_senha(
                dados['senha']
            )

            resultado = usuario_service.cadastrar_usuario(
                novo_usuario
            )

            return make_response(
                jsonify(schema.dump(resultado)),
                201
            )

        except Exception as e:

            return make_response(
                jsonify({
                    'message': str(e)
                }),
                400
            )


class UsuarioResource(Resource):

    @jwt_required()
    def get(self, id_usuario):
        """
        Busca usuário por ID
        ---
        tags:
          - Usuários

        security:
          - Bearer: []

        parameters:
          - name: id_usuario
            in: path
            type: integer
            required: true
            example: 1

        responses:
          200:
            description: Usuário encontrado

          401:
            description: Token inválido

          404:
            description: Usuário não encontrado
        """

        usuario = usuario_service.listar_usuario_id(
            id_usuario
        )

        if usuario:

            schema = usuario_schema.UsuarioSchema()

            return make_response(
                jsonify(schema.dump(usuario)),
                200
            )

        return make_response(
            jsonify({
                'message': "Usuario não encontrado."
            }),
            404
        )



    @jwt_required()
    def put(self, id_usuario):
        """
        Atualiza um usuário
        ---
        tags:
          - Usuários

        security:
          - Bearer: []

        parameters:
          - name: id_usuario
            in: path
            type: integer
            required: true
            example: 1

          - in: body
            name: body
            required: true

            schema:
              type: object

              properties:
                nome:
                  type: string
                  example: William

                email:
                  type: string
                  example: william@gmail.com

                senha:
                  type: string
                  example: "123456"

        responses:
          200:
            description: Usuário atualizado com sucesso

          401:
            description: Token inválido

          404:
            description: Usuário não encontrado
        """

        schema = usuario_schema.UsuarioSchema()

        try:
            dados = schema.load(request.json)

        except ValidationError as err:

            return make_response(
                jsonify(err.messages),
                400
            )

        usuario = usuario_service.editar_usuario(
            id_usuario,
            dados
        )

        if usuario:

            return make_response(
                jsonify(schema.dump(usuario)),
                200
            )

        return make_response(
            jsonify({
                'message': 'Usuario não encontrado.'
            }),
            404
        )



    @jwt_required()
    def delete(self, id_usuario):
        """
        Remove um usuário
        ---
        tags:
          - Usuários

        security:
          - Bearer: []

        parameters:
          - name: id_usuario
            in: path
            type: integer
            required: true
            example: 1

        responses:
          200:
            description: Usuário deletado com sucesso

          401:
            description: Token inválido

          404:
            description: Usuário não encontrado
        """

        if usuario_service.deletar_usuario(
            id_usuario
        ):

            return make_response(
                jsonify({
                    'message': 'Usuário deletado com sucesso!'
                }),
                200
            )

        return make_response(
            jsonify({
                'message': 'Usuário não encontrado!'
            }),
            404
        )


class LoginResource(Resource):

    def post(self):
        """
        Login do usuário
        ---
        tags:
          - Login

        parameters:
          - in: body
            name: body
            required: true

            schema:
              type: object

              properties:
                email:
                  type: string
                  example: william@gmail.com

                senha:
                  type: string
                  example: "123456"

        responses:
          200:
            description: Login realizado com sucesso

          401:
            description: Credenciais inválidas
        """

        dados = request.json or {}

        if not dados.get('email') or not dados.get('senha'):

            return make_response(
                jsonify({
                    'message': 'Email e senha são obrigatórios.'
                }),
                400
            )

        usuario = usuario_service.listar_usuario_email(
            dados['email']
        )

        if not usuario:

            return make_response(
                jsonify({
                    'message': 'Usuário não encontrado'
                }),
                404
            )

        if not usuario.verifica_senha(
            dados['senha']
        ):

            return make_response(
                jsonify({
                    'message': 'Senha inválida'
                }),
                401
            )

        token = create_access_token(
            identity=str(usuario.id)
        )

        return make_response(
            jsonify({
                'access_token': token,
                'usuario': {
                    'id': usuario.id,
                    'nome': usuario.nome,
                    'email': usuario.email
                }
            }),
            200
        )


api.add_resource(UsuarioList, '/usuarios')
api.add_resource(UsuarioResource, '/usuarios/<int:id_usuario>')
api.add_resource(LoginResource, '/login')