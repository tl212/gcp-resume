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
        # get client IP address for unique visitor tracking
        # Check multiple headers for the real client IP
        forwarded_for = request.headers.get('X-Forwarded-For')
        real_ip = request.headers.get('X-Real-IP')
        
        if forwarded_for:
            # X-Forwarded-For can contain multiple IPs, take the first (original client)
            client_ip = forwarded_for.split(',')[0].strip()
        elif real_ip:
            client_ip = real_ip.strip()
        else:
            client_ip = request.remote_addr or 'unknown'
        
        # reference to collections
        counter_ref = db.collection('site-stats').document('visitor-counter')
        visitors_ref = db.collection('site-stats').document('unique-visitors')
        
        # get current counter and visitor data
        counter_doc = counter_ref.get()
        visitors_doc = visitors_ref.get()
        
        # Initialize counter if it doesn't exist
        if counter_doc.exists:
            current_count = counter_doc.to_dict().get('count', 0)
        else:
            current_count = 0
        
        # initialize visitor tracking if it doesn't exist
        if visitors_doc.exists:
            visitor_data = visitors_doc.to_dict()
            unique_ips = visitor_data.get('ips', [])
        else:
            unique_ips = []
        
        # check if this IP has visited before
        is_new_visitor = client_ip not in unique_ips
        
        if is_new_visitor:
            # add new visitor IP and increment counter
            unique_ips.append(client_ip)
            new_count = current_count + 1
            
            # update both documents
            counter_ref.set({
                'count': new_count,
                'last_updated': firestore.SERVER_TIMESTAMP
            })
            
            visitors_ref.set({
                'ips': unique_ips,
                'last_updated': firestore.SERVER_TIMESTAMP
            })
            
            return jsonify({'count': new_count, 'new_visitor': True}), 200, headers
        else:
            # return current count without incrementing
            return jsonify({'count': current_count, 'new_visitor': False}), 200, headers
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': 'Failed to update counter'}), 500, headers
