from importlib import util as importing

from flask import Flask, redirect
from flask_restx import Api
from werkzeug.middleware.proxy_fix import ProxyFix

from backend.api.v1 import API_VERSION as V1
from backend.api.v1.service_api import namespace as service_namespace
from backend.api.v1.shared_models import namespace as shared_models_namespace
from backend.api.v1.user_api import namespace as user_namespace
from backend.configuration.application_configuration import ApplicationConfiguration, get_application_configuration
from backend.common.db.database import get_db_session, init_db, migrate_db, build_db_connection_string
from backend.common.dto.database_configuration import DatabaseConfiguration

_SWAGGER_URL = '/doc/'


def create_app() -> Flask:
    app = Flask(__name__)
    # fix for https swagger - see https://github.com/python-restx/flask-restx/issues/58
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_port=1, x_for=1, x_host=1, x_prefix=1)

    def load_local_development_config():
        config_file = 'backend.local_config'
        if importing.find_spec(config_file):
            app.config.from_object(config_file)
            app.config['IS_LOCAL_DEV'] = True

    def connect_to_database(conf: ApplicationConfiguration):
        # connect to the database
        # docs https://flask.palletsprojects.com/en/1.1.x/patterns/sqlalchemy/
        init_db(DatabaseConfiguration(
            postgres_user=conf.postgres_user,
            postgres_password=conf.postgres_password,
            postgres_url=conf.postgres_url,
            postgres_db=conf.postgres_db
        ))
        # process the migrations
        migrate_db(build_db_connection_string(
            postgres_user=conf.postgres_user,
            postgres_password=conf.postgres_password,
            postgres_url=conf.postgres_url,
            postgres_db=conf.postgres_db
        ))

    def configure_apis():
        authorizations = {
            'bearer': {
                'type': 'apiKey',
                'in': 'header',
                'name': 'Authorization'
            }
        }

        api = Api(
            doc=_SWAGGER_URL,
            version='1.0',
            title='Breviary API',
            authorizations=authorizations,
        )
        api.init_app(app)
        api.add_namespace(shared_models_namespace)
        api.add_namespace(service_namespace, path=f'{V1}/service')
        api.add_namespace(user_namespace, path=f'{V1}/user')

    def init_default_routes():
        # pylint: disable=unused-variable
        @app.route('/')
        def redirect_to_swagger():
            return redirect(_SWAGGER_URL, code=302)

    def configure_context_hooks():
        # close session when the request is processed
        # https://flask.palletsprojects.com/en/1.1.x/patterns/sqlalchemy/
        @app.teardown_appcontext
        def shutdown_session(exception=None):
            session = get_db_session()
            if session:
                session.remove()

    with app.app_context():
        # load configuration
        load_local_development_config()
        conf = get_application_configuration()
        # initialize database engine
        connect_to_database(conf)
        # configure context lifetime
        configure_context_hooks()
        # register basic routes
        init_default_routes()
        # finish configuration
        configure_apis()
        return app
