from flask import Flask, request, jsonify
import random

app = Flask(__name__)


@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    modelname = data.get('modelname')
    viewerid = data.get('viewerid')

    random_number = random.randint(1, 100)
    result = {
        "reason": modelname,
        "result": random_number
    }

    return jsonify(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

