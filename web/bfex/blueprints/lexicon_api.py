from flask import Blueprint, abort, render_template, make_response, request
from flask_restful import Resource, Api

from bfex.models import Lexicon
from bfex.components.data_ingestor import DataIngester
from bfex.common.exceptions import DataIngestionException
from bfex.common.schema import LexiconSchema
from bfex.blueprints.api_utils import paginate_query

MB = 1024 * 1024

# Setup the blueprint and add to the api.
lexicon_bp = Blueprint("lexicon_api", __name__)
api = Api(lexicon_bp)

class LexiconListAPI(Resource):
    """Methods for performing some operations on lists of Lexicon members."""

    def get(self):
        """HTTP Get for the lexicon list resource.

        Returns a list of lexicon members from elasticsearch.
        :param page: URL Parameter for the page to fetch. Default - 0.
        :param results: URL Parameter for the number of results to return per page. Default - 20.
        :return:
        """
        search = Lexicon.search()
        query, pagination_info = paginate_query(request, search)
        response = query.execute()

        schema = LexiconSchema()
        results = [schema.dump(lexicon) for lexicon in response]

        return {
            "pagination": pagination_info,
            "data": results
        }

    def post(self):
        """HTTP Post for the lexicon list resource.

        Ingests a lists of lexicon members, and saves the information into elasticsearch. Currently does not do any
        checks if there already exists a lexicon member with the same id that will be overridden.
        TODO: Decide if this should check for existing lexicon and return which lexicon were not inserted, and add PUT.

        :return:HTTP 400 if the request is not JSON.
                HTTP 413 if the given JSON is more than 16MB in size or there was an error ingesting the given data.
                HTTP 200 if the ingestion succeeded.
        """
        if not request.is_json:
            abort(400)

        json_data = request.get_json()

        try:
            DataIngester.bulk_create_lexicon(json_data["data"])
        except DataIngestionException as e:
            print(e)
            abort(500)

        return 200


api.add_resource(LexiconListAPI, '/lexicon')

