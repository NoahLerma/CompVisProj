"""
Utility script to generate test images for vision testing
Creates simple geometric shapes with different colors for testing purposes
"""

from PIL import Image, ImageDraw
import os

def create_color_test_image():
    """Create an image with various color blocks for color recognition testing"""
    img = Image.new('RGB', (600, 400), 'white')
    draw = ImageDraw.Draw(img)
    
    # Create color blocks
    colors = [
        ('red', (255, 0, 0)),
        ('green', (0, 255, 0)),
        ('blue', (0, 0, 255)),
        ('yellow', (255, 255, 0)),
        ('purple', (128, 0, 128)),
        ('orange', (255, 165, 0)),
        ('cyan', (0, 255, 255)),
        ('pink', (255, 192, 203))
    ]
    
    block_size = 150
    for i, (name, color) in enumerate(colors):
        x = (i % 4) * block_size
        y = (i // 4) * block_size
        draw.rectangle([x, y, x + block_size - 10, y + block_size - 10], fill=color)
    
    return img

def create_shape_test_image():
    """Create an image with various geometric shapes for shape recognition testing"""
    img = Image.new('RGB', (600, 400), 'white')
    draw = ImageDraw.Draw(img)
    
    # Circle
    draw.ellipse([50, 50, 150, 150], fill='red', outline='darkred', width=2)
    
    # Square
    draw.rectangle([200, 50, 300, 150], fill='blue', outline='darkblue', width=2)
    
    # Triangle
    draw.polygon([350, 150, 400, 50, 450, 150], fill='green', outline='darkgreen', width=2)
    
    # Rectangle
    draw.rectangle([50, 200, 200, 280], fill='yellow', outline='orange', width=2)
    
    # Pentagon (approximated)
    draw.polygon([300, 200, 350, 220, 370, 270, 330, 300, 270, 270], fill='purple', outline='darkviolet', width=2)
    
    # Star (simplified)
    draw.polygon([450, 200, 460, 230, 490, 240, 470, 260, 480, 290, 450, 270, 420, 290, 430, 260, 410, 240, 440, 230], fill='orange', outline='darkorange', width=2)
    
    # Hexagon
    draw.polygon([100, 320, 150, 320, 175, 350, 150, 380, 100, 380, 75, 350], fill='cyan', outline='darkcyan', width=2)
    
    # Diamond
    draw.polygon([300, 320, 350, 370, 300, 420, 250, 370], fill='pink', outline='deeppink', width=2)
    
    return img

def create_complex_test_image():
    """Create a more complex image with overlapping shapes and patterns"""
    img = Image.new('RGB', (600, 400), 'lightgray')
    draw = ImageDraw.Draw(img)
    
    # Background gradient effect with rectangles
    for i in range(10):
        color_val = 255 - i * 20
        draw.rectangle([i * 60, 0, (i + 1) * 60, 400], fill=(color_val, color_val, 255))
    
    # Overlapping circles pattern
    for i in range(3):
        for j in range(2):
            x = 100 + i * 150
            y = 100 + j * 150
            draw.ellipse([x, y, x + 80, y + 80], fill='red', outline='darkred', width=2)
    
    # Grid pattern
    for i in range(0, 600, 50):
        draw.line([i, 0, i, 400], fill='white', width=1)
    for i in range(0, 400, 50):
        draw.line([0, i, 600, i], fill='white', width=1)
    
    # Text-like shapes (rectangles of varying sizes)
    text_shapes = [(50, 50, 80, 20), (150, 80, 60, 15), (250, 60, 90, 18), (380, 90, 70, 22)]
    for x, y, w, h in text_shapes:
        draw.rectangle([x, y, x + w, y + h], fill='black')
    
    return img

def main():
    """Generate test images"""
    os.makedirs('test_images', exist_ok=True)
    
    # Generate test images
    color_img = create_color_test_image()
    color_img.save('test_images/color_test.png')
    print("Created color test image: test_images/color_test.png")
    
    shape_img = create_shape_test_image()
    shape_img.save('test_images/shape_test.png')
    print("Created shape test image: test_images/shape_test.png")
    
    complex_img = create_complex_test_image()
    complex_img.save('test_images/complex_test.png')
    print("Created complex test image: test_images/complex_test.png")
    
    print("\nTest images generated successfully!")
    print("You can use these images to test the vision capabilities of your Ollama models.")

if __name__ == "__main__":
    main()
