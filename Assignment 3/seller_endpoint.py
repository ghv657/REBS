from flask import Flask, jsonify

app_seller = Flask(__name__)

@app_seller.route('/ask', methods=['GET'])
def ask():
    return jsonify({"quote": 15}), 200  

@app_seller.route('/ask_high_price', methods=['GET'])
def ask_high_price():
    return jsonify({"quote": 19}), 200  

if __name__ == '__main__':
    app_seller.run(port=8000)
