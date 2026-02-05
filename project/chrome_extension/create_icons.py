"""
Simple script to create placeholder icons for Chrome extension.
Requires Pillow: pip install Pillow
"""
try:
    from PIL import Image, ImageDraw
    
    def create_icon(size, filename):
        """Create a simple icon with gradient background."""
        img = Image.new('RGB', (size, size), color='#667eea')
        draw = ImageDraw.Draw(img)
        
        # Draw a simple magnifying glass icon
        center = size // 2
        radius = int(size * 0.3)
        
        # Circle (magnifying glass)
        draw.ellipse(
            [center - radius, center - radius, center + radius, center + radius],
            outline='white',
            width=max(2, size // 16)
        )
        
        # Handle (magnifying glass handle)
        handle_length = int(radius * 0.8)
        handle_start = center + int(radius * 0.7)
        draw.line(
            [handle_start, handle_start, handle_start + handle_length, handle_start + handle_length],
            fill='white',
            width=max(2, size // 16)
        )
        
        img.save(filename)
        print(f"Created {filename} ({size}x{size})")
    
    # Create all three icon sizes
    create_icon(16, 'icon16.png')
    create_icon(48, 'icon48.png')
    create_icon(128, 'icon128.png')
    
    print("\nIcons created successfully!")
    print("You can now load the extension in Chrome.")
    
except ImportError:
    print("Pillow is required. Install it with: pip install Pillow")
    print("\nAlternatively, create icons manually:")
    print("- icon16.png (16x16 pixels)")
    print("- icon48.png (48x48 pixels)")
    print("- icon128.png (128x128 pixels)")
    print("\nSee ICONS.md for more information.")
