from flask import Blueprint, jsonify, request, make_response
from flask.views import MethodView
from api.models import Geoname

geonames_blueprint = Blueprint('geonames', __name__)


class ReverseGeocodeAPI(MethodView):
    """
    Get Nearest Geoname based on input lat/lon
    """

    def get(self):
        get_data = request.args
        try:
            lat = get_data.get('lat')
            lon = get_data.get('lon')
            feature_code = get_data.get('featureCode')
            feature_class = get_data.get('featureClass')
            if lat and lon:
                result = Geoname.reverse_geocode(lat=lat,
                                                 lon=lon,
                                                 feature_code=feature_code,
                                                 feature_class=feature_class)
                return make_response(
                    jsonify({'success': True,
                             "data": result
                             })), 200
            else:
                return make_response(
                    jsonify({'success': False,
                             'message': 'Must supply both `lat` and `lon` parameters.'
                             })), 400
        except Exception as e:
            response_object = {
                'success': False,
                'message': str(e)
            }
            return make_response(jsonify(response_object)), 500


class GeocodeAPI(MethodView):
    """
    Get Geoname based on Name & Country Code
    """

    def get(self):
        get_data = request.args
        try:
            iso2 = get_data.get('iso2')
            name = get_data.get('name')
            admin1 = get_data.get('admin1')
            admin2 = get_data.get('admin2')
            feature_code = get_data.get('featureCode')
            feature_class = get_data.get('featureClass')
            result = Geoname.geocode(iso2=iso2,
                                     name=name,
                                     admin1=admin1,
                                     admin2=admin2,
                                     feature_code=feature_code,
                                     feature_class=feature_class
                                     )
            return make_response(
                jsonify({'success': True,
                         'data': result
                         })), 200
        except Exception as e:
            response_object = {
                'success': False,
                'message': str(e)
            }
            return make_response(jsonify(response_object)), 500


reverse_geocode_view = ReverseGeocodeAPI.as_view('reverse_geocode_api')
geocode_view = GeocodeAPI.as_view('geocode_api')

# add Rules for API Endpoints
geonames_blueprint.add_url_rule(
    '/reverse-geocode',
    view_func=reverse_geocode_view,
    methods=['GET']
)
geonames_blueprint.add_url_rule(
    '/geocode',
    view_func=geocode_view,
    methods=['GET']
)
