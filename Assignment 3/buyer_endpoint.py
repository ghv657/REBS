from flask import Flask, jsonify, request
import requests

app_buyer = Flask(__name__)

@app_buyer.route('/buy', methods=['GET'])
def buy():
    try:
        # Assuming buyer is asking for chips
        response = jsonify({"product": "chips"})
        
        # Asking sellers for quotes
        seller_response = requests.get('http://localhost:8000/ask')
        seller_response_high_price = requests.get('http://localhost:8000/ask_high_price')

        # Check if the requests were successful
        if seller_response.status_code != 200 or seller_response_high_price.status_code != 200:
            print(f"Failed to get valid responses from the sellers.")
            return jsonify({"error": "Failed to get valid responses from Sellers"}), 500

        # Check if the responses are valid JSON
        try:
            price = seller_response.json().get('quote', 0)
            price_high_price = seller_response_high_price.json().get('quote', 0)
        except ValueError:
            print("Received invalid responses from the sellers.")
            return jsonify({"error": "Invalid Responses from Sellers"}), 500

        if price < 20 or price_high_price < 20:
            if price < price_high_price:
                print("Price is acceptable, I choose seller1 because", price, "<", price_high_price)

                # Accept the quote and send an order to the shipper
                shipper_response = requests.post('http://localhost:8001/order', json={"order": "chips"}).json()
                invoice = shipper_response.get('details', 'N/A')

                print(f"Received {invoice} from Shipper!")
            else:
                print("Price is acceptable, I choose seller1 because", price_high_price, "<", price)

                # Accept the quote and send an order to the shipper
                shipper_response = requests.post('http://localhost:8001/order', json={"order": "chips"}).json()
                invoice = shipper_response.get('details', 'N/A')

                print(f"Received {invoice} from Shipper!")
        else:
            print("Both prices are too high (", price, price_high_price, ")")

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
