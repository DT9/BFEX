import os
from flask import Flask
from bfex.blueprints.faculty_api import faculty_bp
from bfex.blueprints.search_api import search_bp
from bfex.models import initialize_models


def create_app():
    """Instantiates and configures the BFEX application.

    First, any environment variables needed are retrieved using sensible defaults for a development environment.
    Next, any initializations that need to be performed are done. Currently, we instantiate a connection to elastic
    and initialize the model definitions in the database.
    Finally, API blueprints are registered to the application so they can be accessed.

    Environment Variables:
    ELASTIC_HOST: URL of the elasticsearch instance to be used. If undefined, localhost is used.

    :return An initialized and configured instance of a Flask application.
    """
    from elasticsearch_dsl.connections import connections
    
    app = Flask("bfex")
    
    elastic_host = os.getenv("ELASTIC_HOST", "localhost")
    connections.create_connection(hosts=[elastic_host])

    initialize_models()

    app.register_blueprint(faculty_bp)
    app.register_blueprint(search_bp)

    return app

app = create_app()
