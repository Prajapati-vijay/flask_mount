from flask import Flask, render_template, request, send_from_directory
import os

app = Flask(__name__)

# Base directories
DIRECTORIES = ['test', 'test1', 'test2']

# Helper function to get all files in a directory, including subdirectories
def get_all_files(directory):
    files = []
    try:
        # Traverse the directory and its subdirectories
        for root, dirs, filenames in os.walk(directory):
            for filename in filenames:
                # Add the full path to the file in the directory structure
                files.append(os.path.relpath(os.path.join(root, filename), start=directory))
    except FileNotFoundError:
        print(f"Directory '{directory}' not found.")
    except Exception as e:
        print(f"Error in directory '{directory}': {e}")
    return files

@app.route('/')
def index():
    files_in_dirs = {}
    for directory in DIRECTORIES:
        files_in_dirs[directory] = get_all_files(directory)
    
    return render_template('index.html', files_in_dirs=files_in_dirs)

@app.route('/view/<directory>/<filename>')
def view_file(directory, filename):
    # Ensure directory exists
    if directory not in DIRECTORIES:
        return f"Directory '{directory}' not found."

    file_path = os.path.join(directory, filename)
    
    # Check if file exists
    if not os.path.isfile(file_path):
        return f"File '{filename}' not found in '{directory}'."
    
    # Read the content of the file
    try:
        with open(file_path, 'r') as file:
            content = file.read()
    except Exception as e:
        return f"Error reading file '{filename}': {e}"
    
    return f"<h1>Content of {filename} in {directory}</h1><pre>{content}</pre><br><a href='/'>Back to Files</a>"

@app.route('/download/<directory>/<filename>')
def download_file(directory, filename):
    # Ensure directory exists
    if directory not in DIRECTORIES:
        return f"Directory '{directory}' not found."
    
    try:
        return send_from_directory(directory, filename, as_attachment=True)
    except Exception as e:
        return f"Error downloading file '{filename}': {e}"

if __name__ == '__main__':
    # Ensure the directories exist
    for directory in DIRECTORIES:
        os.makedirs(directory, exist_ok=True)
    
    app.run(debug=True)
