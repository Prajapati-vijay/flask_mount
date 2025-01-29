from flask import Flask, render_template, request, send_from_directory, abort
import os
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_port=1, x_for=1, x_host=1, x_prefix=1)

# Directory to monitor
DIRECTORY_PATH = "test"

def get_all_files(directory):
    """ Recursively get all files with relative paths """
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            rel_path = os.path.relpath(os.path.join(root, filename), directory)
            files.append(rel_path.replace("\\", "/"))  # Normalize for web URLs
    return files

@app.route('/')
def index():
    """ List all files including subdirectories """
    try:
        files = get_all_files(DIRECTORY_PATH)
    except FileNotFoundError:
        return f"Directory '{DIRECTORY_PATH}' not found."
    except Exception as e:
        return str(e)
    
    return render_template('index.html', files=files)

@app.route('/view/<path:filename>')
def view_file(filename):
    """ View file content, handling subdirectories """
    try:
        file_path = os.path.join(DIRECTORY_PATH, filename)
        if not os.path.isfile(file_path):
            abort(404, f"File '{filename}' not found.")
        
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except Exception as e:
        return str(e)
    
    return f"<h1>Content of {filename}</h1><pre>{content}</pre><br><a href='/'>Back to Files</a>"

@app.route('/download/<path:filename>')
def download_file(filename):
    """ Download a file, handling subdirectories """
    try:
        directory = os.path.join(DIRECTORY_PATH, os.path.dirname(filename))
        filename = os.path.basename(filename)
        return send_from_directory(directory, filename, as_attachment=True)
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    os.makedirs(DIRECTORY_PATH, exist_ok=True)
    app.run(debug=True)
