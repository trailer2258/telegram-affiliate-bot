from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os

def add_watermark(image_bytes, watermark_text, font_size, color, position, margin):
    try:
        img = Image.open(BytesIO(image_bytes))
        
        # Convert to RGBA if needed
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Create watermark layer
        watermark = Image.new('RGBA', img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(watermark)
        
        # Try to load font
        font_path = os.path.join(os.path.dirname(__file__), '../../fonts/Arial.ttf')
        try:
            font = ImageFont.truetype(font_path, font_size)
        except IOError:
            # Fallback to default font
            font = ImageFont.load_default()
        
        # Calculate text position
        text_width, text_height = draw.textsize(watermark_text, font=font)
        positions = {
            'top-left': (margin, margin),
            'top-right': (img.width - text_width - margin, margin),
            'bottom-left': (margin, img.height - text_height - margin),
            'bottom-right': (img.width - text_width - margin, img.height - text_height - margin)
        }
        pos = positions.get(position, positions['bottom-right'])
        
        # Draw text with shadow
        shadow_pos = (pos[0] + 2, pos[1] + 2)
        draw.text(shadow_pos, watermark_text, (0, 0, 0, 128), font=font)
        draw.text(pos, watermark_text, (*color, 200), font=font)
        
        # Combine with original image
        watermarked = Image.alpha_composite(img, watermark)
        
        # Save to bytes
        img_byte_arr = BytesIO()
        watermarked.save(img_byte_arr, format='PNG')
        return img_byte_arr.getvalue()
        
    except Exception as e:
        print(f"Watermark failed: {str(e)}")
        return image_bytes