from flask import Flask, jsonify

app_shipper = Flask(__name__)

@app_shipper.route('/order', methods=['POST'])
def order():
    data = "(Your order has been shipped)"  
    return jsonify({"details": data}), 200

if __name__ == '__main__':
    app_shipper.run(port=8001)
