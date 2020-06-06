from tests.base import BaseTestCase

class TestGeonamesApi(BaseTestCase):

    def test_reverse_geocode(self):
        """ Test Reverse Geocode """
        with self.app.test_client() as client:
            result = client.get(
                'reverse-geocode',
                query_string={'lon': 69.17, 'lat': 34.52}
            )
            response = result.get_json()
            self.assertTrue(response['success'])
            self.assertTrue(len(response['data']) >= 1)
            self.assertEqual(
                response['data'][0]['properties']['name'],
                'Kabul'
            )
            self.assertEqual(
                response['data'][0]['properties']['admin1'],
                'Kabul'
            )
            self.assertEqual(
                response['data'][0]['properties']['admin2'],
                'Kabul'
            )
            self.assertEqual(
                response['data'][0]['properties']['iso2'],
                'AF'
            )
            self.assertDictEqual(
                response['data'][0]['geometry'],
                {'coordinates': [69.17233, 34.52813], 'type': 'Point'}
            )

    def test_geocode(self):
        """ Test Geocode """
        with self.app.test_client() as client:
            result = client.get(
                'geocode',
                query_string={'iso2': 'us', 'name': 'Saratoga'}
            )
            response = result.get_json()
            self.assertTrue(response['success'])
            self.assertEqual(len(response['data']), 2)
            self.assertEqual(response['data'][0]['properties']['iso2'], 'US')
            self.assertEqual(response['data'][0]['properties']['name'], 'Saratoga Springs')
            self.assertEqual(response['data'][0]['properties']['admin1'], 'New York')
            self.assertEqual(response['data'][1]['properties']['iso2'], 'US')
            self.assertEqual(response['data'][1]['properties']['name'], 'Saratoga Springs')
            self.assertEqual(response['data'][1]['properties']['admin1'], 'Utah')
            self.assertEqual(response['data'][1]['properties']['timezone'], 'America/Denver')

    def test_geocode_multiple_results(self):
        """ Test Geocode with more than one result"""
        with self.app.test_client() as client:
            result = client.get(
                'geocode',
                query_string={'iso2': 'us', 'name': 'Saratoga'}
            )
            response = result.get_json()
            self.assertTrue(response['success'])
            self.assertEqual(len(response['data']), 2)
            self.assertEqual(response['data'][0]['properties']['iso2'], 'US')
            self.assertEqual(response['data'][0]['properties']['name'], 'Saratoga Springs')
            self.assertEqual(response['data'][0]['properties']['admin1'], 'New York')
            self.assertEqual(response['data'][0]['properties']['admin2'], 'Saratoga County')
            self.assertEqual(response['data'][1]['properties']['iso2'], 'US')
            self.assertEqual(response['data'][1]['properties']['name'], 'Saratoga Springs')
            self.assertEqual(response['data'][1]['properties']['admin1'], 'Utah')
            self.assertEqual(response['data'][1]['properties']['admin2'], 'Utah County')
