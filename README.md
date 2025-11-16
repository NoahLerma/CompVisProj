# Ollama Vision Capabilities Tester

A Python application for testing and showcasing the computer vision capabilities of Ollama AI models, specifically focusing on color and shape recognition.

## Features

- **Color Recognition**: Tests the model's ability to identify and describe colors, shades, and color patterns in images
- **Shape Recognition**: Evaluates geometric shape identification, positioning, and spatial relationships
- **General Vision Analysis**: Comprehensive image analysis including objects, colors, shapes, and composition
- **Web-based Interface**: Modern Streamlit interface (recommended) or desktop GUI option
- **Multiple Model Support**: Works with various Ollama vision models (llava, llava-13b, bakllava, moondream)

## Requirements

- Python 3.7 or higher
- Ollama server running locally or accessible via network
- Vision-capable Ollama model installed (e.g., llava)

## Installation

1. Clone or download this repository
2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Setup Ollama

1. Install Ollama: https://ollama.ai
2. Pull a vision-capable model:
   ```bash
   ollama pull llava
   # or try other models:
   ollama pull llava-13b
   ollama pull bakllava
   ollama pull moondream
   ```
3. Start Ollama server:
   ```bash
   ollama serve
   ```

## Usage

### Option 1: Web Interface (Recommended)

1. Start the web app:
   ```bash
   python run_web.py
   ```
   or directly:
   ```bash
   streamlit run web_app.py
   ```

2. Open your browser to the provided URL (usually http://localhost:8501)

3. Configure the Ollama server URL and test connection

4. Upload an image using the file uploader

5. Choose a test type:
   - **Color Recognition**: Analyzes colors, shades, and color patterns
   - **Shape Recognition**: Identifies geometric shapes and their relationships
   - **General Vision**: Comprehensive image analysis

6. View the results and download them if needed

### Option 2: Desktop GUI (Alternative)

If tkinter is properly installed on your system:

```bash
python main.py
```

**Note**: The web interface is recommended as it doesn't depend on tkinter and provides a better user experience.

## Test Examples

### Color Recognition Test
The model will analyze:
- Dominant colors and their shades
- Color gradients and transitions
- Color patterns and schemes
- Approximate color distribution

### Shape Recognition Test
The model will identify:
- Basic geometric shapes (circles, squares, triangles, etc.)
- Shape positions and spatial relationships
- Size proportions and arrangements
- Complex shape combinations

### General Vision Test
The model provides:
- Complete object identification
- Color and shape analysis
- Text/symbol recognition
- Composition and style analysis
- Notable details and features

## Supported Image Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- GIF (.gif)
- TIFF (.tiff)

## Troubleshooting

- **Connection Failed**: Ensure Ollama server is running and accessible at the specified URL
- **Model Not Found**: Make sure you have pulled a vision-capable model using `ollama pull`
- **Tcl/Tk Error**: Use the web interface instead of the desktop GUI
- **Slow Response**: Larger images may take longer to process. Consider resizing images for faster testing
- **Poor Results**: Try different prompts or models. Some models perform better on specific tasks

## Future Enhancements

Planned additions for more comprehensive testing:
- Object detection and counting
- Text recognition (OCR capabilities)
- Scene understanding and context analysis
- Comparative analysis between multiple images
- Batch testing capabilities
- Performance metrics and scoring

## License

This project is open source and available under the MIT License.
