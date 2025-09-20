import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from google.cloud import firestore

# Create Flask app instance (needed for testing)
app = Flask(__name__)
CORS(app)

# initialize firestore client (automatically uses current's project)
db = firestore.Client()

def visitor_counter(request):
    # handle CORS preflight request
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 204, headers)

    # set CORS headers for main request
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
    }

    try:
        #reference to the counter document
        counter_ref = db.collection('site-stats').document('visitor-counter')

        #get current count or initialize
        counter_doc = counter_ref.get()

        if counter_doc.exists:
            current_count = counter_doc.to_dict().get('count', 0)
        else:
            current_count = 0

        #increment the counter
        new_count = current_count + 1

        #update Firestore
        counter_ref.set({
            'count': new_count,
            'last_updated': firestore.SERVER_TIMESTAMP
        })

        #return the new count
        return jsonify({'count': new_count}), 200, headers
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': 'Failed to update counter'}), 500, headers
