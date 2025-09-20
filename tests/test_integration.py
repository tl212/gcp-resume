import requests
import unittest
import time

class TestIntegration(unittest.TestCase):

    # set up test urls
    def setUp(self):
        self.function_url = "https://visitor-counter-uasgf6ueta-uc.a.run.app"
        self.website_url = "https://storage.googleapis.com/resume-sevenl33-v2-25/index.html"
    
    # test that cloud function returns a count greater than 0
    def test_cloud_function_returns_count(self):
        response = requests.get(self.function_url)
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn('count', data)
        self.assertIsInstance(data['count'], int)
        self.assertGreater(data['count'], 0)

    # test that count increments on subsequent requests
    def test_cloud_function_increments_count(self):

        # first call 
        response_one = requests.get(self.function_url)
        count_one = response_one.json()['count']

        # small delay
        time.sleep(1)

        # second call
        response_two = requests.get(self.function_url)
        count_two = response_two.json()['count']

        self.assertEqual(count_two, count_one + 1)

    # test that website loads and increments count
    def test_website_loads_and_increments_count(self):
        response = requests.get(self.website_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/html', response.headers.get('Content-Type', ''))

    # test CORS preflight request
    def test_cors_preflight_request(self):
        response = requests.options(self.function_url)
        self.assertEqual(response.status_code, 204)
        self.assertIn('Access-Control-Allow-Origin', response.headers)
    
if __name__ == '__main__':
    unittest.main()
        

