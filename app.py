
from flask import Flask, render_template, request, send_from_directory, jsonify
from flask_ngrok import run_with_ngrok
import os
from keras.preprocessing.image import load_img
from functions import detect_logo
# import json

# import base64
# import io
# from PIL import Image


APP_ROOT = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
run_with_ngrok(app)

# CONFIG = json.loads(open('config.json','rb').read())

UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 

# def load():
#     global model,label_encoder
#     model = load_k_model(CONFIG['Model_Path'])
#     label_encode = load_labelenc(CONFIG['Label_Encoder_Path'])
# load()
@app.route("/")
def home():
    return render_template('index.html')

@app.route("/upload", methods=['GET','POST'])
def upload():
    for img in request.files.getlist("file"):
	    img_name = img.filename
	    destination = "/".join([UPLOAD_FOLDER, img_name])
	    img.save(destination)
    if img_name == img.filename:
        #img = cv2.imread('/static/uploads/<image_name>',flags=3)
        img = load_img(('./static/uploads/'+img_name), target_size=(640, 480))
        #img = load_img(listdir(r'E:\projects\one\static\uploads', target_size=(224,224)))
        #img_name = img.filename
        result = []
        result = detect_logo(img)
        print("######################################",result)
        # im = Image.open(result)
        # data = io.BytesIO()
        # im.save(data,"JPEG")
        # encoded_img_data = base64.b64encode(data.getvalue())

    return render_template("result.html",image_name = img_name, logo = result)

@app.route("/static/uploads/<filename>")
def send_image(filename):
	return send_from_directory("./static/uploads/", filename)
    
app.run()