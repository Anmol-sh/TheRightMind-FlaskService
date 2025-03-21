from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import base64
import os
from google import genai
from google.genai import types
from env_var import gemini_api_key
from gemini_flash_2 import generate

app = Flask(__name__)

# Enable CORS for all routes
CORS(
    app,
    resources={r"/*": {"origins": ["http://127.0.0.1:3000", "http://localhost:3000"]}},
    supports_credentials=True
)

# genai.configure(api_key=gemini_api_key)
output_img = "/Users/anmol/Code/TheRightMind/output_img.jpeg"
output_text = "/Users/anmol/Code/TheRightMind/output_text.txt"
IMAGES_FOLDER = "/Users/anmol/Code/TheRightMind/TheRightMind-Service"

# Existing route
@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/image/<filename>', methods=['GET'])
def get_image(filename):
    """
    Serve an image file by filename from the IMAGES_FOLDER.
    """
    try:
        # send_from_directory automatically checks that filename doesn't escape 
        # the directory boundaries (preventing directory traversal attacks)
        return send_from_directory(IMAGES_FOLDER, filename)
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    
@app.route('/chat', methods=['POST'])
async def process_chat():
    data = request.get_json()

    # Validate the data (length and width must exist and be numeric)
    if 'message' not in data:
        return jsonify({'error': 'Message missing in input object'}), 400

    try:
        # Return the result as JSON
        message = data["message"]
        print(f"Received message: {message}")

        response = await generate(message=message)

        return jsonify({'message': response}), 200
    except Exception as error:
        return jsonify({'error': str(error)}), 500


if __name__ == '__main__':
    app.run(debug=True)