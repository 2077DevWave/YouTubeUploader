from flask import Flask, request, jsonify
import requests
import os
from Upload import upload_video

app = Flask(__name__)

@app.route('/upload_video', methods=['GET'])
def upload_video_api():
    try:
        # Define the required GET parameters
        required_params = ['video_title', 'video_description', 'video_file_url']

        # Check if all required parameters are present
        for param in required_params:
            if request.args.get(param) is None:
                return jsonify({'error': f'Missing required parameter: {param}'}), 400

        # Get parameters from the GET request
        video_title = request.args.get('video_title')
        video_description = request.args.get('video_description')
        video_file_url = request.args.get('video_file_url')

        # Download the video file from the provided URL
        video_file_path = download_file(video_file_url)

        # Call the upload_video function from Upload.py
        result = upload_video(video_title, video_description, video_file_path)

        # Return the result as JSON
        return jsonify({'result': result})

    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Error downloading file: {str(e)}'}), 500

    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

def download_file(url):
    try:
        # Send a GET request to the URL to download the file
        response = requests.get(url, stream=True)

        # Get the filename from the URL
        filename = url.split("/")[-1]

        # Save the file to a local directory
        with open(os.path.join('downloads', filename), 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)

        # Return the path to the saved file
        return os.path.join('downloads', filename)

    except Exception as e:
        raise Exception(f'Error downloading file: {str(e)}')

if __name__ == '__main__':
    app.run(debug=True)