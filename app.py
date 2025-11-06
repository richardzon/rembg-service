from flask import Flask, request, send_file
from flask_cors import CORS
from rembg import remove
from PIL import Image
import io
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

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
        
        # Remove background using rembg (returns PNG with fully transparent background)
        print('Removing background...')
        print(f'Input image size: {len(input_image)} bytes')
        
        # Use rembg with explicit parameters for best transparency
        output_image = remove(
            input_image,
            alpha_matting=True,
            alpha_matting_foreground_threshold=240,
            alpha_matting_background_threshold=10,
            alpha_matting_erode_size=10
        )
        
        print(f'Output image size after rembg: {len(output_image)} bytes')
        
        # Load image and ensure RGBA mode
        img = Image.open(io.BytesIO(output_image))
        print(f'Image mode: {img.mode}')
        
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
            print('Converted to RGBA')
        
        # Apply gradient fade to bottom 30% of ENTIRE IMAGE (including the gangster)
        # This makes the gangster fade out at the bottom for smooth card blending
        width, height = img.size
        fade_height = int(height * 0.3)  # Bottom 30% fades out
        fade_start = height - fade_height
        
        # Create new alpha channel with gradient applied to EVERYTHING
        new_alpha = Image.new('L', (width, height), 255)
        alpha_pixels = new_alpha.load()
        
        # Get original alpha from rembg (0 = background, 255 = foreground)
        original_alpha = img.split()[3]
        original_pixels = original_alpha.load()
        
        for y in range(height):
            for x in range(width):
                # Start with original alpha from rembg
                base_alpha = original_pixels[x, y]
                
                # Apply gradient fade to bottom portion
                if y >= fade_start:
                    # Calculate how far into the fade we are (0.0 to 1.0)
                    fade_progress = (y - fade_start) / fade_height
                    # Fade factor goes from 1.0 (fully visible) to 0.0 (fully transparent)
                    fade_factor = 1.0 - fade_progress
                    # Multiply base alpha by fade factor
                    base_alpha = int(base_alpha * fade_factor)
                
                alpha_pixels[x, y] = base_alpha
        
        # Apply the new alpha channel
        img.putalpha(new_alpha)
        
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
