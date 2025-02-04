from flask import Flask, send_from_directory

# Create the Flask app, pointing to the 'frontend' directory for static files
app = Flask(__name__, static_folder='frontend')

@app.route('/')
def index():
    # Serve the index.html from the frontend folder
    return send_from_directory(app.static_folder, 'index.html')

# If you have additional endpoints (e.g., to proxy requests to Rasa),
# you can define them here

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

