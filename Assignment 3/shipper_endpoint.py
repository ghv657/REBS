from flask import Flask, jsonify

app_shipper = Flask(__name__)

@app_shipper.route('/order', methods=['POST'])
def order():
    data = "Some invoice details"  # This is a placeholder; you can modify as needed
    return jsonify({"details": data}), 200

if __name__ == '__main__':
    app_shipper.run(port=8001)
