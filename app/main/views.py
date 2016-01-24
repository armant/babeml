from . import main
from flask import render_template, request
from googleapiclient.discovery import build
from werkzeug import secure_filename
import OCR
import os


def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@main.route('/', methods=['GET', 'POST'])
def index():
  if request.method == 'POST':
    image_file = request.files['file']
    if image_file:
      filepath = os.path.join('uploads', image_file.filename)
      image_file.save(filepath)
      language = detect_language(filepath)
      result_file_path = 'recognized/' + image_file.filename + '.txt'
      OCR.recognizeFile(filepath=filepath, resultFilePath=result_file_path,
                        language=language, outputFormat='txt')
      return translate(filepath=result_file_path), 500

  return render_template('main/index.html')

def detect_language(filepath):
  # ML algorithm goes here
  return 'ChinesePRC'

def translate(filepath):
  service = build('translate', 'v2',
    developerKey='ENTER_YOUR_DEV_KEY')
  f = open( filepath )
  contents = f.read().decode('utf-8')
  translated_text = service.translations().list(
      target='en',q=[contents]).execute()
  return translated_text['translations'][0]['translatedText']