# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
from keras.models import load_model
from PIL import Image
import keras
import tensorflow as tf
import matplotlib.pyplot as plt
import cv2
import os
import numpy as np
import model

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():

        return render_template('index.html', price=price)

if __name__ == '__main__':
   app.run(debug = True)