from cloudant.client import Cloudant
from cloudant.error import CloudantException
import requests
from cloudant.query import Query
from flask import Flask, jsonify, request
import atexit

#Add your Cloudant service credentials here
from cloudant.client import Cloudant
from cloudant.error import CloudantException
import requests

from cloudant.client import Cloudant
from cloudant.error import CloudantException
import requests

cloudant_username = 'apikey-v2-36pj3euq0qduq8gcwvks1xc9dxzshm5bt56i2xxthqur'
cloudant_api_key = 'RG6IhfR257M0jRcGNtlz4cMnXd1kBMvKBAREYqY-w8rW'
cloudant_url = 'https://apikey-v2-36pj3euq0qduq8gcwvks1xc9dxzshm5bt56i2xxthqur:6c52400f2cd796ef03388ce9500e64b5@9e8e1f68-b574-42c0-8bf7-a4dd91788e09-bluemix.cloudantnosqldb.appdomain.cloud'

# Initialize Cloudant client outside the try block
client = None

try:
    # Initialize Cloudant client
    client = Cloudant.iam(cloudant_username, cloudant_api_key, connect=True, url=cloudant_url)

    # Check if the client is connected
    if client.connect():
        print("Connected to Cloudant")

        # Access other Cloudant operations here using 'client'

        # Get the session information
        session = client.session()
        print("Session information:", session)

        # List all databases
        databases = client.all_dbs()
        print('Databases:', databases)

    else:
        print("Failed to connect to Cloudant")

except CloudantException as cloudant_exception:
    print("Cloudant exception:", cloudant_exception)

except requests.exceptions.RequestException as request_exception:
    print("Request exception:", request_exception)

except Exception as e:
    print("An unexpected error occurred:", e)

finally:
    # Disconnect the client in the finally block to ensure it's done whether there's an exception or not
    if client:
        client.disconnect()



print('Databases:', client.all_dbs())

db = client['reviews']

app = Flask(__name__)

@app.route('/api/get_reviews', methods=['GET'])
def get_reviews():
    dealership_id = request.args.get('id')

    # Check if "id" parameter is missing
    if dealership_id is None:
        return jsonify({"error": "Missing 'id' parameter in the URL"}), 400

    # Convert the "id" parameter to an integer (assuming "id" should be an integer)
    try:
        dealership_id = int(dealership_id)
    except ValueError:
        return jsonify({"error": "'id' parameter must be an integer"}), 400

    # Define the query based on the 'dealership' ID
    selector = {
        'dealership': dealership_id
    }

    # Execute the query using the query method
    result = db.get_query_result(selector)

    # Create a list to store the documents
    data_list = []

    # Iterate through the results and add documents to the list
    for doc in result:
        data_list.append(doc)

    # Return the data as JSON
    return jsonify(data_list)


@app.route('/api/post_review', methods=['POST'])
def post_review():
    if not request.json:
        abort(400, description='Invalid JSON data')
    
    # Extract review data from the request JSON
    review_data = request.json

    # Validate that the required fields are present in the review data
    required_fields = ['id', 'name', 'dealership', 'review', 'purchase', 'purchase_date', 'car_make', 'car_model', 'car_year']
    for field in required_fields:
        if field not in review_data:
            abort(400, description=f'Missing required field: {field}')

    # Save the review data as a new document in the Cloudant database
    db.create_document(review_data)

    return jsonify({"message": "Review posted successfully"}), 201

if __name__ == '__main__':
    app.run(debug=True)