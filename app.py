from flask import Flask, render_template, request, send_from_directory
import os
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_port=1, x_for=1, x_host=1, x_prefix=1)

# Directory to monitor
DIRECTORY_PATH = "test"

@app.route('/')
def index():
    # List all files in the directory
    try:
        files = os.listdir(DIRECTORY_PATH)
    except FileNotFoundError:
        return f"Directory '{DIRECTORY_PATH}' not found."
    except Exception as e:
        return str(e)
    
    return render_template('index.html', files=files)

@app.route('/view/<filename>')
def view_file(filename):
    try:
        file_path = os.path.join(DIRECTORY_PATH, filename)
        with open(file_path, 'r') as file:
            content = file.read()
    except FileNotFoundError:
        return f"File '{filename}' not found."
    except Exception as e:
        return str(e)
    
    return f"<h1>Content of {filename}</h1><pre>{content}</pre><br><a href='/'>Back to Files</a>"

@app.route('/download/<filename>')
def download_file(filename):
    try:
        return send_from_directory(DIRECTORY_PATH, filename, as_attachment=True)
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    # Ensure the directory exists
    os.makedirs(DIRECTORY_PATH, exist_ok=True)
    app.run(debug=True)
