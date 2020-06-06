import os
from tests.base import BaseTestCase
from api.models import Geoname


class TestGeonamesModel(BaseTestCase):

    def test_geonames_query(self):
        """Test query for Geonames"""
        result = Geoname.query.filter_by(geonameid=292223).all()
        self.assertEqual(len(result), 1)
        self.assertTrue(type(result[0].name), str)
        self.assertTrue(type(result[0].latitude), float)
        self.assertTrue(type(result[0].longitude), float)
        self.assertTrue(type(result[0].geonameid), int)

    def test_geocode_join_with_admin1_admin2(self):
        """ Test Geocoding join to admin2 table that has a value"""
        result = Geoname.geocode(iso2='us', name='saratoga')
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['properties']['id'], 5136334)
        self.assertEqual(result[0]['properties']['name'], 'Saratoga Springs')
        self.assertEqual(result[0]['properties']['admin1'], 'New York')
        self.assertEqual(result[0]['properties']['admin2'], 'Saratoga County')
        self.assertEqual(result[0]['properties']['iso2'], 'US')
        self.assertDictEqual(result[0]['geometry'], {'coordinates': [-73.78457, 43.08313], 'type': 'Point'})

        self.assertEqual(result[1]['properties']['id'], 5781087)
        self.assertEqual(result[1]['properties']['name'], 'Saratoga Springs')
        self.assertEqual(result[1]['properties']['admin1'], 'Utah')
        self.assertEqual(result[1]['properties']['admin2'], 'Utah County')
        self.assertEqual(result[1]['properties']['iso2'], 'US')
        self.assertDictEqual(result[1]['geometry'], {'coordinates': [-111.90466, 40.34912], 'type': 'Point'})

    def test_geocode_no_country_code(self):
        """ Geocodes from iso2 country code and city name"""
        result = Geoname.geocode(name='Sarajevo')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['properties']['id'], 3191281)
        self.assertEqual(result[0]['properties']['name'], 'Sarajevo')
        self.assertEqual(result[0]['properties']['population'], 696731)
        self.assertEqual(result[0]['properties']['featureCode'], 'PPLC')
        self.assertDictEqual(result[0]['geometry'], {'type': 'Point', 'coordinates': [18.35644, 43.84864]})

    def test_reverse_geocode(self):
        """ Test reverse geocode with closest feature first"""
        result = Geoname.reverse_geocode(lat=43.61062, lon=-72.97261)
        self.assertTrue(len(result) >= 1)
        self.assertEqual(result[0]['properties']['id'], 5240509)
        self.assertEqual(result[0]['properties']['name'], 'Rutland')
        self.assertEqual(result[0]['properties']['admin1'], 'Vermont')
        self.assertEqual(result[0]['properties']['admin2'], 'Rutland County')
        self.assertEqual(result[0]['properties']['iso2'], 'US')
        self.assertDictEqual(result[0]['geometry'], {'type': 'Point', 'coordinates': [-72.97261, 43.61062]})

    def test_reverse_geocode_fail_with_none(self):
        """ test reverse geocode fail with None lat/lon arguments"""
        result = Geoname.reverse_geocode(lat=None, lon=None)
        self.assertEqual(result, {})
