import unittest
import json
from unittest.mock import Mock, patch
import sys
import os
from main import visitor_counter

#add backend to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

class TestVisitorCounter(unittest.TestCase):
    def setUp(self):
        self.mock_request = Mock()

    #test CORS preflight (options) request
    def test_options_request(self):
        self.mock_request.method = 'OPTIONS'
        response = visitor_counter(self.mock_request)
        self.assertEqual(response[1], 204)
        self.assertIn('Access-Control-Allow-Origin', response[2])
        self.assertEqual(response[2]['Access-Control-Allow-Origin'], '*')

    @patch('main.db')
    #test visitor counter increment 
    def test_visitor_counter_increment(self, mock_db):
        self.mock_request.method = 'GET'

        #mock firestore responses
        mock_doc = Mock()
        mock_doc.exists.return_value = True
        mock_doc.to_dict.return_value = {'count': 5}

        mock_ref = Mock()
        mock_ref.get.return_value = mock_doc
        mock_ref.set = Mock()

        mock_collection = Mock()
        mock_collection.document.return_value = mock_ref
        
        mock_db.collection.return_value = mock_collection

        #call visitor_counter
        response = visitor_counter(self.mock_request)
        body = json.loads(response[0].get_data(as_text=True))

        #assert response
        self.assertEqual(response[1], 200)
        self.assertEqual(body['count'], 6)
        mock_ref.set.assert_called_once()
    
    @patch('main.db')

    #test visitor counter when no previous count exists
    def test_visitor_counter_new_visitor(self, mock_db):
        self.mock_request.method = 'GET'
        
        #mock Firestore for new visitor
        mock_doc = Mock()
        mock_doc.exists = Mock(return_value=False)
        
        mock_ref = Mock()
        mock_ref.get.return_value = mock_doc
        mock_ref.set = Mock()
        
        mock_collection = Mock()
        mock_collection.document.return_value = mock_ref
        
        mock_db.collection.return_value = mock_collection
        
        # call visitor_counter
        response = visitor_counter(self.mock_request)
        body = json.loads(response[0].get_data(as_text=True))
        
        # assert response
        self.assertEqual(response[1], 200)
        self.assertEqual(body['count'], 1)
        mock_ref.set.assert_called_once()
    
    @patch('main.db')
    # test error handling in visitor counter
    def test_visitor_counter_error_handling(self, mock_db):
        self.mock_request.method = 'GET'
        
        #mock Firestore to raise an exception
        mock_db.collection.side_effect = Exception("Database error")
        
        # call visitor_counter
        response = visitor_counter(self.mock_request)
        body = json.loads(response[0].get_data(as_text=True))

        # assert response
        self.assertEqual(response[1], 500)
        self.assertIn('error', body)

if __name__ == '__main__':
    unittest.main()