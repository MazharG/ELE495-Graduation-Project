import json
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/data', methods=['GET'])
def get_data():
    
    with open("datas.json", "r") as file:
        datas = json.load(file)
    return jsonify(datas)  
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
