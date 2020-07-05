from flask import Flask, render_template, request, redirect, url_for
from get_images import get_images, get_path, get_directory
from get_prediction import get_prediction
from generate_html import generate_html
from torchvision import models
import json

app = Flask(__name__)

# mapping
imagenet_class_mapping = json.load(open('imagenet_class_index.json'))

# Make sure to pass `pretrained` as `True` to use the pretrained weights:
model = models.densenet121(pretrained=True)
# Since we are using our model only for inference, switch to `eval` mode:
model.eval()


def get_image_class(path):
    get_images(path)
    path = get_path(path)
    images_with_tags = get_prediction(model, imagenet_class_mapping, path)
    print(images_with_tags)
    generate_html(images_with_tags)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/', methods=['POST', 'GET'])
def get_data():
    if request.method == 'POST':
        user = request.form['search']
        get_image_class(user)
        return redirect(url_for('success', name=get_directory(user)))


@app.route('/success/<name>')
def success(name):
    return render_template('image_class.html')


if __name__ == '__main__' :
    app.run(debug=True)
