from flask import Flask, jsonify
import requests  # Ensure this line is added to import the requests module

app_buyer = Flask(__name__)

@app_buyer.route('/buy', methods=['GET'])
def buy():
    try:
        # Assuming buyer is asking for chips
        response = jsonify({"product": "chips"})
        
        # Asking seller for a quote
        seller_response = requests.get('http://localhost:8000/ask').json()
        price = seller_response.get('quote', 0)  # Default value of 0 if 'quote' key is not present
        
        if price < 20:
            print("Price is lower than 20.")
            
            # Accept the quote and send an order to shipper
            shipper_response = requests.post('http://localhost:8001/order', json={"order": "chips"}).json()
            invoice = shipper_response.get('details', 'N/A')  # Default value 'N/A' if 'details' key is not present
            
            print(f"Received {invoice} from Shipper!")
        else:
            print("Price is not lower than 20.")
            # Handle rejection if the price is not acceptable
        
        return response, 200
    except requests.RequestException as e:
        print(f"Request error occurred: {e}")
        return jsonify({"error": "Request Error"}), 500
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == '__main__':
    app_buyer.run(port=8002, debug=True)
