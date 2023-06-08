import mysql.connector

#click es una herramienta para poder ejecutar comandos en la terminal, eso lo vamos  a necesitar para poder crear tablas, y tambien crear la relacion entre ellos, sin tener que ir a workbench y hacer las conexiones
import click

#g es una variable que siempre se encuentra en la aplicacion completa y podemos ir llamandola cuando la necesitemos
#current_app mantiene la app corriendo.
from flask import current_app, g

from flask.cli import with_appcontext

from .schema import instructions

#los corchetes [] se usan para acceder a una propiedad de la configuracion que ya habiamos hecho.
def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(
            host=current_app.config['DATABASE_HOST'],
            user=current_app.config['DATABASE_USER'],
            password=current_app.config['DATABASE_PASSWORD'],
            database=current_app.config['DATABASE'],
        )
        g.c = g.db.cursor(dictionary=True)
    
    return g.db, g.c

def close_db(e=None):
    db= g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db, c = get_db()

    for i in instructions:
        c.execute(i)
    db.commit()

@click.command('init-db')
@with_appcontext


def init_db_command():
    init_db()
    click.echo('Base de datos inicializada.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
