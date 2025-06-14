import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img,img_to_array
from tensorflow.keras.applications.vgg16 import preprocess_input
import numpy as np
import gdown

app=Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'],exist_ok=True)

#Download the model fom the google drive link 

list_of_file=os.listdir('model')
if "model_vgg16.h5" in list_of_file:
    print("Model already exists")
else:
    file_id="1ZxzKZ9s2QMLXKAY8jOzxplSEfBG6CVf_"
    url=f"https://drive.google.com/uc?id={file_id}"
    output="model/model_vgg16.h5"
    gdown.download(url,output,quiet=False)

#https://drive.google.com/file/d/1ZxzKZ9s2QMLXKAY8jOzxplSEfBG6CVf_/view?usp=sharing


# Load the pre-trained model
model = load_model('model/model_vgg16.h5')

class_name=[
    'Oblique fracture',
    'Spiral fracture'
]

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1].lower() in {'png','jpg','jpeg','gif'}
        
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('file')
        if file and allowed_file(file.filename):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            # Preprocess the image    
            img = load_img(filepath, target_size=(224, 224))
            x = img_to_array(img)
            x = np.expand_dims(x, axis=0)
            x = preprocess_input(x)

            # Make prediction
            prediction = model.predict(x)
            idx = np.argmax(prediction[0])
            label = class_name[idx]
            confidence = prediction[0][idx]

            return render_template('index.html', label=label, confidence=confidence, filename=file.filename)
        
        return redirect(request.url)

    # ✅ For GET requests (initial page load)
    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return redirect(url_for('static', filename='uploads/' + filename))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
