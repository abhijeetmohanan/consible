import os
import urllib.request
from flask import Flask, request, redirect, jsonify, render_template 
from werkzeug.utils import secure_filename

app = Flask(__name__)

DIRPATH="/root/nopassDir/m1server"

ALLOWED_EXTENSIONS = set(['yml', 'yaml', 'cfg', 'ini'])

def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/folderCreate/', methods=['POST'] )
def folderCreate():
  
   os.system(f"mkdir -p {DIRPATH}/")
   resp = jsonify({'directory_status': 'Created'})
   return resp

# API Curl command: curl -XPOST 192.168.10.128:5000/folderCreate/

# API cURL command Push File: curl --location --request POST 'http://192.168.10.128:5000/file-upload/' --form 'file=@/root/data/inv.ini'

#ssh-key generation

@app.route('/key-generate/<KEY>/<USER>', methods=['POST'])
def key_generate(KEY,USER):
        os.system(f"/root/serverData/key_generator {KEY} {USER}")
        resp = jsonify({'ssh_status': 'Done'})
        return resp

@app.route('/file-upload/', methods=['POST'])
def upload_file():
        # check if the post request has the file part
        if 'file' not in request.files:
                resp = jsonify({'message' : 'No file part in the request'})
                resp.status_code = 400
                return resp
        file = request.files['file']
        if file.filename == '':
                resp = jsonify({'message' : 'No file selected for uploading'})
                resp.status_code = 400
                return resp
        if file and allowed_file(file.filename):
            if 'yaml' in file.filename.rsplit('.', 1)[1].lower() or 'yml' in file.filename.rsplit('.', 1)[1].lower():
                filename = secure_filename(file.filename)
                file.save(os.path.join(f"{DIRPATH}/theplaybook.yaml"))
                resp = jsonify({'file' : f'{file.filename}','Status' : 'Successfully uploaded'})
                resp.status_code = 201
                return resp
            elif 'cfg' in file.filename.rsplit('.', 1)[1].lower():
                filename = secure_filename(file.filename)
                file.save(os.path.join(f"{DIRPATH}/ansible.cfg"))
                resp = jsonify({'file' : f'{file.filename}','Status' : 'Successfully uploaded'})
                resp.status_code = 201
                return resp
            elif 'ini' in file.filename.rsplit('.', 1)[1].lower():
                filename = secure_filename(file.filename)
                file.save(os.path.join(f"{DIRPATH}/Inventory.ini"))
                resp = jsonify({'file' : f'{file.filename}','Status' : 'Successfully uploaded'})
                resp.status_code = 201
                return resp
            else:
                resp = jsonify({'Status': 'Unknown Error !!!!'})
                return resp

        else:
                resp = jsonify({'message' : 'Ansible Files only allowed'})
                resp.status_code = 400
                return resp

if __name__ == '__main__':
   app.run(debug=True, host="0.0.0.0")
