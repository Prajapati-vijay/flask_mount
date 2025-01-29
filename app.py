from flask import Flask, render_template, request
import os
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_port=1, x_for=1, x_host=1, x_prefix=1)

# Directory to monitor
DIRECTORY_PATH = "test"

def get_all_files(directory):
    # This function will return all files and directories recursively
    files = []
    
    try:
        # Traverse directories and subdirectories
        for entry in os.scandir(directory):
            # Just append the entry path, regardless of whether it's a file or directory
            files.append(os.path.relpath(entry.path, directory))
            if entry.is_dir():
                # Recurse into subdirectories
                files.extend(get_all_files(entry.path))
    except Exception as e:
        print(f"Error scanning directory {directory}: {str(e)}")
    
    return files

@app.route('/')
def index():
    # List all files and directories in the directory
    try:
        files = get_all_files(DIRECTORY_PATH)
    except FileNotFoundError:
        return f"Directory '{DIRECTORY_PATH}' not found."
    except Exception as e:
        return str(e)
    
    return render_template('index.html', files=files)

@app.route('/view/<path:filename>')
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

if __name__ == '__main__':
    # Ensure the directory exists
    os.makedirs(DIRECTORY_PATH, exist_ok=True)
    app.run(debug=True)
