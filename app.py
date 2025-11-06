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
        
        # Remove background using rembg (returns PNG with alpha channel)
        print('Removing background...')
        output_image = remove(input_image, alpha_matting=True, alpha_matting_foreground_threshold=240, alpha_matting_background_threshold=10)
        
        # Ensure transparency is preserved
        img = Image.open(io.BytesIO(output_image))
        
        # Convert to RGBA if not already (ensures alpha channel)
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Apply gradient fade to bottom 30% of image for smooth blending
        width, height = img.size
        fade_height = int(height * 0.3)  # Bottom 30% of image
        
        # Create gradient mask (fully opaque at top, transparent at bottom)
        gradient = Image.new('L', (width, height), 255)  # Start with fully opaque
        for y in range(height - fade_height, height):
            # Calculate alpha (255 = opaque, 0 = transparent)
            alpha = int(255 * (1 - (y - (height - fade_height)) / fade_height))
            for x in range(width):
                gradient.putpixel((x, y), alpha)
        
        # Apply gradient mask to alpha channel
        alpha_channel = img.split()[3]  # Get existing alpha
        alpha_channel = Image.composite(gradient, alpha_channel, gradient.point(lambda x: 255))
        img.putalpha(alpha_channel)
        
        # Save with transparency
        output_buffer = io.BytesIO()
        img.save(output_buffer, format='PNG', optimize=True)
        output_buffer.seek(0)
        
        print(f'Background removed! Image size: {len(output_buffer.getvalue())} bytes')
        
        # Return processed image with transparency
        return send_file(
            output_buffer,
            mimetype='image/png',
            as_attachment=False,
            download_name='output.png'
        )
    
    except Exception as e:
        print(f'Error: {str(e)}')
        return {'error': str(e)}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860)
