from model.translator import get_translation_from_list, get_translation_from_text
from iso639 import Lang
import json
from flask import Flask, request, Response
# from flask_cors import CORS
import os
app = Flask(__name__)


# def save_to_json(data, name):
#     jsonString = json.dumps(data, ensure_ascii=False)
#     with open(name, "w", encoding="utf-8") as jsonFile:
#         jsonFile.write(jsonString)

@app.route("/translate", methods=["GET", "POST"])
def translate(json_data=None):
    result = {}
    try:
        if json_data is None:
            json_data = request.get_json()

        text = json_data.get('text', '')
        dest_code = json_data.get('dest_language')

        dest_language = Lang(dest_code).name
        if type(text) == list:
            answers, cost = get_translation_from_list(dest_language, text)
        else:
            answers, cost = get_translation_from_text(dest_language, text)

        result['success']=True
        result['answers'] = answers
        result['cost'] = cost
        
    except Exception as e:
        result["success"]=False
        result["message"]=str(e)
    finally: 
        return Response(json.dumps(result), mimetype=u'application/json')


@app.route("/", methods=["GET"])
def login():
    return "Hello, world!"
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.getenv('PORT', "5001"))



