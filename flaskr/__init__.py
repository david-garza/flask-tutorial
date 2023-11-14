import os

from flask import Flask

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flasker.sqlite'),
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the instance config if pased in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that say hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    # Registers the init-db for command line use
    from . import db
    db.init_app(app)

    # Registers the auth blueprint
    from . import auth
    app.register_blueprint(auth.bp)
    
    return app