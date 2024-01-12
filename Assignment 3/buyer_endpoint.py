from flask import Flask, jsonify
import requests

app_buyer = Flask(__name__)
@app_buyer.route('/buy', methods=['GET'])

def buy():
    try:
        # Assuming buyer is asking for chips
        response = jsonify({"product": "chips"})
        
        # Asking seller for a quote
        seller_response = requests.get('http://localhost:8000/ask')
        
        # Check if the request was successful
        if seller_response.status_code != 200:
            print(f"Failed to get a valid response from the seller. Status Code: {seller_response.status_code}")
            return jsonify({"error": "Failed to get valid response from Seller"}), 500
        
        # Check if the response is valid JSON
        try:
            price = seller_response.json().get('quote', 0)
        except ValueError:
            print("Received an invalid response from the seller.")
            return jsonify({"error": "Invalid Response from Seller"}), 500
        
        if price < 20:
            print("Price is lower than 20.")
            
            # Accept the quote and send an order to shipper
            shipper_response = requests.post('http://localhost:8001/order', json={"order": "chips"}).json()
            invoice = shipper_response.get('details', 'N/A')
            
            print(f"Received {invoice} from Shipper!")
        else:
            print("Price is not lower than 20.")
            
            # Handle rejection by sending a rejection message to shipper
            rejection_response = requests.post('http://localhost:8001/order', json={"rejected": True})
            if rejection_response.status_code == 200:
                print("Successfully sent rejection to Shipper.")
            else:
                print(f"Failed to send rejection to Shipper. Status Code: {rejection_response.status_code}")
        
        return response
    except requests.RequestException as e:
        print(f"Request error occurred: {e}")
        return jsonify({"error": "Request Error"}), 500
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == '__main__':
    app_buyer.run(port=8002)
