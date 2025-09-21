import unittest
import json
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# add backend to path BEFORE importing from it << Fix 
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

# Mock the Firestore client before importing main to avoid credential issues in CI/CD
with patch('google.cloud.firestore.Client') as mock_firestore:
    mock_firestore.return_value = MagicMock()
    from main import app, visitor_counter

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
        self.mock_request.remote_addr = '192.168.1.1'

        # mock firestore responses for counter document
        mock_counter_doc = Mock()
        mock_counter_doc.exists.return_value = True
        mock_counter_doc.to_dict.return_value = {'count': 5}

        # mock firestore responses for visitors document 
        mock_visitors_doc = Mock()
        mock_visitors_doc.exists.return_value = True
        mock_visitors_doc.to_dict.return_value = {'ips': ['192.168.1.2']}

        mock_counter_ref = Mock()
        mock_counter_ref.get.return_value = mock_counter_doc
        mock_counter_ref.set = Mock()
        
        mock_visitors_ref = Mock()
        mock_visitors_ref.get.return_value = mock_visitors_doc
        mock_visitors_ref.set = Mock()

        mock_collection = Mock()
        # return different refs based on document name
        def mock_document(doc_name):
            if doc_name == 'visitor-counter':
                return mock_counter_ref
            elif doc_name == 'unique-visitors':
                return mock_visitors_ref
        mock_collection.document.side_effect = mock_document
        
        mock_db.collection.return_value = mock_collection

        #call visitor_counter
        with app.app_context():
            response = visitor_counter(self.mock_request)
        body = json.loads(response[0].get_data(as_text=True))

        #assert response
        self.assertEqual(response[1], 200)
        self.assertEqual(body['count'], 6)
        self.assertEqual(body['new_visitor'], True)
        mock_counter_ref.set.assert_called_once()
        mock_visitors_ref.set.assert_called_once()
    
    @patch('main.db')
    # test visitor counter when no previous count exists
    def test_visitor_counter_new_visitor(self, mock_db):
        self.mock_request.method = 'GET'
        self.mock_request.remote_addr = '192.168.1.3'
        
        # mock Firestore for new visitor - both documents don't exist debug 5.2
        mock_counter_doc = Mock()
        mock_counter_doc.exists = False
        
        mock_visitors_doc = Mock()
        mock_visitors_doc.exists = False
        
        mock_counter_ref = Mock()
        mock_counter_ref.get.return_value = mock_counter_doc
        mock_counter_ref.set = Mock()
        
        mock_visitors_ref = Mock()
        mock_visitors_ref.get.return_value = mock_visitors_doc
        mock_visitors_ref.set = Mock()
        
        mock_collection = Mock()
        
        # return different refs based on document name
        def mock_document(doc_name):
            if doc_name == 'visitor-counter':
                return mock_counter_ref
            elif doc_name == 'unique-visitors':
                return mock_visitors_ref
        mock_collection.document.side_effect = mock_document
        
        mock_db.collection.return_value = mock_collection
        
        # call visitor_counter
        with app.app_context():
            response = visitor_counter(self.mock_request)
        body = json.loads(response[0].get_data(as_text=True))
        
        # assert response
        self.assertEqual(response[1], 200)
        self.assertEqual(body['count'], 1)
        self.assertEqual(body['new_visitor'], True)
        mock_counter_ref.set.assert_called_once()
        mock_visitors_ref.set.assert_called_once()
    
    @patch('main.db')
    # test error handling in visitor counter
    def test_visitor_counter_error_handling(self, mock_db):
        self.mock_request.method = 'GET'
        
        #mock Firestore to raise an exception
        mock_db.collection.side_effect = Exception("Database error")
        
        # call visitor_counter
        with app.app_context():
            response = visitor_counter(self.mock_request)
        body = json.loads(response[0].get_data(as_text=True))

        # assert response
        self.assertEqual(response[1], 500)
        self.assertIn('error', body)

if __name__ == '__main__':
    unittest.main()