# import keras
import numpy as np
from PIL import Image

# import matplotlib.pyplot as plt
# import matplotlib.patches as mpatches

# import os
# import skimage.io
from PIL import Image
import pickle
# import cv2
import keras
from keras.models import load_model, model_from_json
import selectivesearch


def load_k_model(model_dir):
    return load_model(model_dir)

def load_labelenc(pickle_dir):
    labenc = open(pickle_dir,'rb')
    labenc = pickle.load(labenc)
    return labenc

label_encode = load_labelenc("./models/logonet01.pickle")
model = load_k_model("./models/logonet01.h5")

# label_encoder = load_labelenc("./labels/logonet02.pickle")
# model = load_k_model("./models/logonet02.h5")

def detect_logo(img):
  resize_dim = [75,75]
  ss_arr = []
  img = np.array(img)
#   label_encode = load_labelenc("./models/logonet01.pickle")
#   model = load_k_model("./models/logonet01.h5")

#   json_file = open('./new_model/architecture.json', 'r')
#   loaded_model_json = json_file.read()
#   loaded_model = model_from_json(loaded_model_json)
#   # load weights into new model
#   loaded_model.load_weights("./new_model/weights.h5")

#   loaded_model.compile(loss='sparse_categorical_crossentropy',
#               optimizer='adam',
#               metrics=['acc'])

  img_lbl, regions = selectivesearch.selective_search(img, scale=500, sigma=0, min_size=500)

  #fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(10, 10))

  candidates = []

  for r in regions:
      # excluding same rectangle (with different segments)
      if r['rect'] in candidates:
          continue
      # excluding regions smaller than 2000 pixels
      if r['size'] < 2000:
          continue
      # distorted rects
      x, y, w, h = r['rect']
      if h is 0 or w is 0:
          continue
      if w / h > 2 or h / w > 2:
          continue
      candidates.append(r['rect'])
          
      #rect = mpatches.Rectangle((x,y), w, h, fill=False, edgecolor='red', linewidth=1)
      #ax.add_patch(rect)
      image = Image.fromarray(img).crop((x,y,x+w,h+y)).resize(resize_dim)
      ss_arr.append(np.array(image))

  #ax.imshow(img)
  ss_arr = np.array(ss_arr) / 255
  

  preds = []
  probs = []


  #fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(10, 10))
  pred = model.predict(ss_arr)


  for j,i in zip(pred,range(len(pred))):
      preds.append(label_encode.inverse_transform([np.argmax(j,axis=0)])[0])
      probs.append(j.max())



  # x,y,w,h = candidates[probs.index(max(probs))]
  # rect = mpatches.Rectangle((x,y), w, h, fill=False, edgecolor='red', linewidth=1)  
  # ax.add_patch(rect)
  # ax.text(x,y,"{} - {}".format(preds[probs.index(max(probs))], max(probs)),fontsize=13,bbox=dict(facecolor='red', alpha=0.7))

  #ax.imshow(img)
  #print(preds[probs.index(max(probs))],'===>',max(probs))
  print(preds[probs.index(max(probs))])
  value = preds[probs.index(max(probs))]
  return value