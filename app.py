from flask import Flask, request, send_file
from rembg import remove
from PIL import Image
import io
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return {
        'status': 'ok',
        'service': 'Background Removal API',
        'powered_by': 'rembg',
        'cost': 'FREE'
    }

@app.route('/remove-background', methods=['POST'])
def remove_background():
    try:
        # Get image URL from request
        data = request.get_json()
        image_url = data.get('image_url')
        
        if not image_url:
            return {'error': 'No image_url provided'}, 400
        
        # Download image from URL
        print(f'Downloading image from: {image_url}')
        response = requests.get(image_url, timeout=30)
        response.raise_for_status()
        
        input_image = response.content
        
        # Remove background using rembg
        print('Removing background...')
        output_image = remove(input_image)
        
        # Return processed image
        return send_file(
            io.BytesIO(output_image),
            mimetype='image/png',
            as_attachment=False,
            download_name='output.png'
        )
    
    except Exception as e:
        print(f'Error: {str(e)}')
        return {'error': str(e)}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860)
