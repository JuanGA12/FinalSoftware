from flask import Flask
from flask import request, jsonify
from flask_mongoengine import MongoEngine
import time
app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'PBIdb',
    'host': '127.0.0.1',
    'port': 27017
}
db = MongoEngine()
db.init_app(app)

@app.route('/')
def get_pbi():
    country_arg = request.args.get('country')
    db_pbi = Pbi.objects(country=country_arg).first()
    time.sleep(1.5)
    if not db_pbi:
        return jsonify({'error': 'data not found'})
    else:
        return jsonify({'pbi' : db_pbi.valor})
    
class Pbi(db.Document):
    country = db.StringField()
    valor = db.StringField()
    def to_json(self):
        return {"Country": self.country,
                "Valor": self.valor}
    
if __name__ == "__main__":
    app.run(debug=True, port=6102)