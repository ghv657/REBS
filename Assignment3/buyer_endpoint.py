from flask import Flask, jsonify, request
import threading
import time

app_buyer = Flask(__name__)

buyer_state = {
    "product": None,
    "price": None,
    "order_accepted": False,
    "order_rejected": False,
}

@app_buyer.route('/quote', methods=['POST'])
def quote():
    try:
        data = request.json
        product = data.get("product")
        price = data.get("price")
        buyer_state["product"] = product
        buyer_state["price"] = price

        if price < 20:
            buyer_state["order_accepted"] = True
            buyer_state["order_rejected"] = False
        else:
            buyer_state["order_accepted"] = False
            buyer_state["order_rejected"] = True
        
        return jsonify({"status": "processed"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def send_order_to_shipper():
    product = buyer_state["product"]
    if buyer_state["order_accepted"]:
        # Simulate order placement
        time.sleep(2)
        return jsonify({"details": f"Order for {product} has been shipped."})
    elif buyer_state["order_rejected"]:
        return jsonify({"details": f"Order for {product} has been rejected."})
    else:
        return jsonify({"error": "Order not processed."})

@app_buyer.route('/buy', methods=['GET'])
def buy():
    try:
        product = "chips"  # Assuming buyer is asking for chips
        response = jsonify({"product": product})
        
        # Asking sellers for quotes asynchronously
        seller_response_thread = threading.Thread(target=ask_seller, args=(product,))
        seller_response_high_price_thread = threading.Thread(target=ask_high_price_seller, args=(product,))
        
        seller_response_thread.start()
        seller_response_high_price_thread.start()
        
        seller_response_thread.join()
        seller_response_high_price_thread.join()

        return send_order_to_shipper()

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def ask_seller(product):
    try:
        # Simulate seller response
        time.sleep(1)
        response = request.post('http://localhost:8000/quote', json={"product": product, "price": 17})
        if response.status_code == 200:
            print("Received quote from Seller: $17")

    except request.RequestException as e:
        print(f"Request error occurred: {e}")

def ask_high_price_seller(product):
    try:
        # Simulate seller response
        time.sleep(1)
        response = request.post('http://localhost:8000/quote', json={"product": product, "price": 25})
        if response.status_code == 200:
            print("Received quote from High Price Seller: $25")

    except request.RequestException as e:
        print(f"Request error occurred: {e}")

if __name__ == '__main__':
    app_buyer.run(port=8002)
