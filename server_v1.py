import os
import urllib.request
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
#import docker

app = Flask(__name__)

DIRPATH="/root/nopassDir/m1server"

ALLOWED_EXTENSIONS = set(['yml', 'yaml', 'cfg', 'ini', 'pem'])

def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Status Check

@app.route('/statuscheck/', methods=['GET'] )
def status_check():
        val=os.system('curl $DOCKER_HOST:2375')
        if (val==0):
                resp = jsonify({'docker_status': 'Running'})
                return(resp)
        else:
                resp = jsonify({'docker_status': 'Inactive'})
                return(resp)


# Create a Directory

@app.route('/folderCreate/', methods=['POST'] )
def folderCreate():
  
   os.system(f"mkdir -p {DIRPATH}/")
   resp = jsonify({'directory_status': 'Created'})
   return resp

#ssh-key generation

@app.route('/key-generate/<KEY>/<USER>', methods=['POST'])
def key_generate(KEY,USER):
        os.system(f"/root/serverData/key_generator {KEY} {USER}")
        resp = jsonify({'ssh_status': 'Done'})
        return resp

# Main Scripts file uploader

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

# Run Docker

@app.route('/pem_key/', methods=['POST'])
def upload_pemkey():
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
            if 'pem' in file.filename.rsplit('.', 1)[1].lower():
                filename = secure_filename(file.filename)
                file.save(os.path.join(f"{DIRPATH}/server.pem"))
                resp = jsonify({'file' : f'{file.filename}','Status' : 'Successfully uploaded'})
                resp.status_code = 201
                return resp

@app.route('/run_playbook/', methods=['POST'])
def run_playbook():
        command = f"cd /root/nopassDir/m1server && ansible-playbook -i Inventory.ini theplaybook.yaml > /root/report.txt"
        os.system(command)
        resp = jsonify({'message' : 'changes done'})
        resp.status_code = 201
        return resp
@app.route('/request-report')
def get_report():
        print("File dowloaded")
        return send_from_directory("/root/", "report.txt", as_attachment=True)

if __name__ == '__main__':
   app.run(debug=True, host="0.0.0.0")
