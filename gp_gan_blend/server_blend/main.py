from perform_blend import Merger
from flask import Flask, jsonify, request
import flask
import json
from flask_cors import CORS
from flask_healthz import healthz
import logging
from flask_healthz import HealthError
import google.cloud.logging
client = google.cloud.logging.Client()
client.setup_logging()
app = Flask(__name__)
app.register_blueprint(healthz, url_prefix="/")

cors = CORS(
    app,
    resources={
        r"/blend/*": {"origin": "*"},
        r"/test_blend/*": {"origin": "*"},
    },
)

def printok():
    print("Everything is fine")

def liveness():
    try:
        printok()
    except Exception:
        raise HealthError("Can't connect to the file")

def readiness():
    try:
        printok()
    except Exception:
        raise HealthError("Can't connect to the file")

app.config.update(
    HEALTHZ = {
        "alive": "main.liveness",
        "ready": "main.readiness",
    }
)

blender = Merger()

@app.route("/blend", methods=["GET","POST"])
def get_result_url():
    # source = request.args.to_dict()['image_src']
    # destin = request.args.to_dict()["image_dst"]
    # blended = request.args.to_dict()["blend_id"]
    
    # result_BLOB = blender.get_res_blob(
    #     source, destin, blended
    # )

    # return jsonify({"result_BLOB": result_BLOB})
    logging.info(request.get_json())
    # json_dict=request.args.to_dict()
  
    json_dict=request.get_json()['instances']
    print(json_dict)
    source=json_dict[0].get('image_src')
    destin=json_dict[0].get('image_dst')
    blended=json_dict[0].get('blend_id')
    # for k,v in json_dict.items():
    #     data_dict=json.loads(k)
    # source = data_dict.get('instances')[0]["image_src"]
    # destin = data_dict.get('instances')[0]["image_dst"]
    # blended = data_dict.get('instances')[0]["blend_id"]

    result_BLOB = blender.get_res_blob(source, destin, blended)

    return jsonify({"result_BLOB": result_BLOB})


@app.route("/test_blend", methods=["GET"])
def test():
    return jsonify({"result": "blend good to go"})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
