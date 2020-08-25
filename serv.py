# Default Flask app :)

import os
import random
import urllib.request

import quickdraw
import json
from flask import Flask, render_template, request, send_file
import pred340
import time
import numpy as np

app = Flask(__name__)

archs = {"Baseline": "baseline", "From github": "from_github", "VGG Net": "vggnet"}


def gen_random_name_png(ln):
    return ''.join([str(random.randint(0, 9)) for x in range(ln)]) + ".png"


@app.route("/struct", methods=["GET"])
def get_model_struct():
    name = archs[request.args.get("arch", "Baseline")]
    return send_file("models_info/" + name + "_struct.png", mimetype="image/png")

@app.route("/stat", methods=["GET"])
def get_model_stat():
    name = archs[request.args.get("arch", "Baseline")]
    return send_file("models_info/" + name + "_stat.json", mimetype="text/json")

@app.route("/nn_stuff.js", methods=["GET"])
def nn_stuff():
    return send_file("tensorflowjs/nn_stuff.js")

@app.route("/340", methods=["GET"])
def p340():
    return render_template("index2.html");

@app.route("/pred340", methods=["POST"])
def predict_340():
    img = json.loads(request.data.decode())
    arr = img['res']
    qq = pred340.QuickDraw()
    t = time.time()
    pred = qq.keras_predict(np.array(arr))
    print("Time:", time.time() - t)
    pred_s = [qq.classes[x] for x in pred]
    return ', '.join(pred_s)

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/class", methods=["POST"])
def classif():
    arch = request.args.get("arch", "Baseline")
    print(arch)
    data = request.data.decode()
    resp = urllib.request.urlopen(data)
    fname = gen_random_name_png(15)
    with open(fname, "wb") as f:
        f.write(resp.file.read())
        f.close()
    qd = quickdraw.QuickDraw(archs[arch] + ".h5")
    res = qd.classif(fname)
    qd.clear()
    os.remove(fname)
    return res

app.run(debug=True)
