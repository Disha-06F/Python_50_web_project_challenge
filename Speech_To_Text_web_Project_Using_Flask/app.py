from flask import Flask,render_template,request
import speech_recognition as sr
from pydub import AudioSegment
import os

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',text=None)

@app.route('/upload',methods=['POST'])
def upload():
    if 'audio_file' not in request.files:
        return render_template('index.html',text="No file uploaded")
    
    file=request.files['audio_file']
    if file.filename=='':
        return render_template('index.html',text="No selected file")
    
    filename=file.filename
    file.save(filename)

    if filename.endswith(".mp3"):
        sound=AudioSegment.from_mp3(filename)
        filename='converted.wav'
        sound.export(filename,format="wav")


    recognizer=sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio_data=recognizer.record(source)


    try:
        text=recognizer.recognize_google(audio_data)
    except sr.UnknownValueError:
        text="Could not understand the audio"

    except sr.RequestError as e:
        text=f"API Error:{e}"  


    if os.path.exists(filename):
        os.remove(filename)

    return render_template('index.html',text=text) 
if __name__ =='__main__':
    app.run(debug=True)             
