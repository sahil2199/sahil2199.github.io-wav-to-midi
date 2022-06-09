from flask import Flask, render_template, request, send_file
import requests
from handlers.handlers import ConvertHandler

# initialize flask app
app = Flask(__name__)

# This prevents caching in local systems
@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


# render FrontEnd
@app.route('/')
def upload_file_page():
    return render_template('./upload.html')


# upload method for file
@app.route('/file_upload', methods=['GET', 'POST'])
def file_upload():
    # get the wav file
    file = request.files['file']
    if file.filename != '':
        # confirm that file is in WAV format
        split = file.filename.split('.')
        if split.__len__() == 2 and split[1] == 'wav':
            # fetch filename
            fname = file.filename.split('.')[0]
            file.save(fname + ".wav")
            # convert file to midi format and download to front-end
            ConvertHandler.convert_file(fname + ".wav", fname + ".mid")
            return send_file(path_or_file=fname + ".mid", mimetype="audio/midi", as_attachment=True)
    return "Error in the uploaded file", 400


# upload method for web links
@app.route('/upload_link', methods=['GET', 'POST'])
def upload_link():
    # download file from link and convert
    url = request.form['uploadLink']
    r = requests.get(url, allow_redirects=True)
    open('upload_file.wav', 'wb').write(r.content)
    ConvertHandler.convert_file("upload_file.wav", "upload_file.mid")
    # send the converted file to FrontEnd
    return send_file(path_or_file="upload_file.mid", mimetype="audio/midi", as_attachment=True)


# run the application server
if __name__ == "__main__":
    app.run()