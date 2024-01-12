from flask import Flask, jsonify

app_seller = Flask(__name__)

@app_seller.route('/ask', methods=['GET'])
def ask():
    return jsonify({"quote": 21}), 200

#def rejected():
    #return jsonify({"The deal is off"}), 200

if __name__ == '__main__':
    app_seller.run(port=8000)
