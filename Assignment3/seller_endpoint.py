from flask import Flask, jsonify, request

app_seller = Flask(__name__)

@app_seller.route('/quote', methods=['POST'])
def quote():
    try:
        data = request.json
        product = data.get("product")
        price = data.get("price")

        if price < 20:
            return jsonify({"quote": 17}), 200
        else:
            return jsonify({"quote": 25}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app_seller.run(port=8000)
