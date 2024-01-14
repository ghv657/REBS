from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/greet', methods=['POST'])
def greet():
    data = request.json
    name = data.get('name')

    if not name:
        return jsonify({"error": "Name is required"}), 400

    greeting = f"Hello, {name}"
    return jsonify({"greeting": greeting})

if __name__ == '__main__':
    app.run(host='localhost', port=8080)
