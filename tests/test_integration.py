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

    # test that count behavior is consistent for same IP
    def test_cloud_function_increments_count(self):

        # first call 
        response_one = requests.get(self.function_url)
        data_one = response_one.json()
        count_one = data_one['count']

        # small delay
        time.sleep(1)

        # second call from same IP should return same count (not increment)
        response_two = requests.get(self.function_url)
        data_two = response_two.json()
        count_two = data_two['count']

        # since both requests come from the same IP, count should not increment
        self.assertEqual(count_two, count_one)
        # second request should indicate it's not a new visitor
        self.assertEqual(data_two['new_visitor'], False)

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
        

