from flask import Flask, Response
from flask_cors import CORS
from flask_restful import Api, Resource

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from flask_basicauth import BasicAuth
from werkzeug.exceptions import HTTPException
from werkzeug.utils import redirect

from bot.enums import StateUser
from database.database import session
from database.models import User, Cartridge
from config import DB_USER, DB_PASSWORD

app = Flask(__name__, static_url_path='')
api = Api(app)
cors = CORS(app)

app.config['CORS_HEADERS'] = 'Access-Control-Allow-Origin'
app.config['BASIC_AUTH_USERNAME'] = DB_USER
app.config['BASIC_AUTH_PASSWORD'] = DB_PASSWORD

basic_auth = BasicAuth(app)

admin = Admin(app)


class AuthException(HTTPException):
    def __init__(self, message):
        super().__init__(message, Response(
            "You could not be authenticated. Please refresh the page.", 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'}
        ))


class MyModelView(ModelView):
    def is_accessible(self):
        if not basic_auth.authenticate():
            raise AuthException('Not authenticated.')
        else:
            return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(basic_auth.challenge())


admin.add_view(MyModelView(Cartridge, session))
admin.add_view(MyModelView(User, session))


class CartridgeView(Resource):

    def get(self, id=0):
        if id != 0:
            cartridges = session.query(Cartridge).filter(Cartridge.id_cartridge == str(id)).all()
        else:
            cartridges = session.query(Cartridge).all()

        if len(cartridges) == 0:
            return 'Not found', 404
        else:
            cartridges = serializer_cartridges(cartridges)
        return cartridges, 200


api.add_resource(CartridgeView, '/cartridges', '/cartridges/<int:id>')


def serializer_cartridges(cartridges):
    list_cartridges = []
    for cartridge in cartridges:
        list_cartridges.append({'id': cartridge.id,
                                'id_cartridge': cartridge.id_cartridge,
                                'types': cartridge.types,
                                'corps': cartridge.corps,
                                'audience': cartridge.audience,
                                'note': cartridge.note,
                                'state': StateUser[cartridge.state],
                                'last_update': str(cartridge.last_update)})
    return list_cartridges


if __name__ == '__main__':
    app.run(debug=True)
