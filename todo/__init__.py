import os
#variables de entorno.

from flask import Flask


#create app para cuando queramos hacer testing  o hacer varias instacias de la aplicacion
def create_app():
    app = Flask(__name__)
    #from_mapping es ua variable de entorno que despues no va a permitir utilizar variables de configuracion que podremos usar en nuestra APP
    app.config.from_mapping(
        #SECRET_KEY es una cookie.
        SECRET_KEY='mikey',
        DATABASE_HOST=os.environ.get('FLASK_DATABASE_HOST'),
        DATABASE_USER=os.environ.get('FLASK_DATABASE_USER'),
        DATABASE_PASSWORD=os.environ.get('FLASK_DATABASE_PASSWORD'),
        DATABASE=os.environ.get('FLASK_DATABASE'),
    )#AQUI DEFINIMOS LA BASE DE DATOS, Y LA VAMOS ESTABLESER EN VARIABLES DE ENTORNO.

    from . import db
    
    db.init_app(app)

    from . import auth
    from . import todo

    app.register_blueprint(auth.bp)
    app.register_blueprint(todo.bp)

    @app.route('/hola')
    def hola():
        return 'chanchito feliz'
    
    return app


