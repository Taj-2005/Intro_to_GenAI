# Chrome Extension Icons

The extension requires three icon files:
- `icon16.png` (16x16 pixels)
- `icon48.png` (48x48 pixels)
- `icon128.png` (128x128 pixels)

## Creating Icons

You can create icons using:
1. **Online Tools:**
   - https://www.favicon-generator.org/
   - https://realfavicongenerator.net/
   - https://www.canva.com/

2. **Image Editors:**
   - GIMP (free)
   - Photoshop
   - Figma

3. **Simple Placeholder:**
   - Create a simple colored square with text "FJD" (Fake Job Detector)
   - Use a magnifying glass or shield icon to represent detection/security

## Icon Design Suggestions

- **Color Scheme:** Purple/indigo gradient (matching the UI theme)
- **Symbol:** Magnifying glass, shield, or checkmark
- **Style:** Modern, clean, professional

## Temporary Solution

For development, you can:
1. Create simple colored squares as placeholders
2. The extension will work without icons (Chrome will show a default icon)
3. Add proper icons before distribution

## Example Icon Creation (Python)

```python
from PIL import Image, ImageDraw, ImageFont

def create_icon(size, filename):
    img = Image.new('RGB', (size, size), color='#667eea')
    draw = ImageDraw.Draw(img)
    
    # Draw a simple magnifying glass
    center = size // 2
    radius = size // 3
    draw.ellipse([center-radius, center-radius, center+radius, center+radius], 
                 outline='white', width=2)
    draw.line([center+radius, center+radius, center+radius*1.5, center+radius*1.5], 
              fill='white', width=2)
    
    img.save(filename)

create_icon(16, 'icon16.png')
create_icon(48, 'icon48.png')
create_icon(128, 'icon128.png')
```
