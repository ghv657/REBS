from flask import Flask, jsonify, request

app_shipper = Flask(__name__)

@app_shipper.route('/order', methods=['POST'])
def order():
    try:
        data = request.json
        if "rejected" in data:
            return jsonify({"details": "Order has been rejected."}), 200
        else:
            product = data.get("product")
            return jsonify({"details": f"Order for {product} has been shipped."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app_shipper.run(port=8001)
