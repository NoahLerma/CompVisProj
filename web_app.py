"""
Web-based Ollama Vision Tester
A Streamlit application for testing Ollama vision capabilities
"""

import streamlit as st
import requests
import base64
import json
from PIL import Image
import io
import time

class OllamaVisionWebTester:
    def __init__(self):
        self.setup_page()
        
    def setup_page(self):
        st.set_page_config(
            page_title="Ollama Vision Capabilities Tester",
            page_icon="👁️",
            layout="wide",
            initial_sidebar_state="collapsed"  # Start collapsed
        )
        
    def encode_image_to_base64(self, image):
        """Convert PIL Image to base64 string"""
        buffered = io.BytesIO()
        
        # Convert RGBA to RGB for JPEG compatibility
        if image.mode == 'RGBA':
            # Create a white background
            background = Image.new('RGB', image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[-1])  # Use alpha channel as mask
            image = background
        elif image.mode not in ['RGB', 'L']:
            image = image.convert('RGB')
            
        image.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')
        
    def send_vision_request(self, prompt, base64_image, model):
        """Send vision request to Ollama"""
        try:
            url = f"{st.session_state.get('ollama_url', 'http://localhost:11434')}/api/generate"
            
            payload = {
                "model": model,
                "prompt": prompt,
                "stream": False,
                "images": [base64_image]
            }
            
            response = requests.post(url, json=payload, timeout=120)  # Increased timeout to 120 seconds
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', 'No response received')
            else:
                return f"Error: HTTP {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Error: {str(e)}"
            
    def test_connection(self):
        """Test connection to Ollama server"""
        try:
            url = f"{st.session_state.get('ollama_url', 'http://localhost:11434')}/api/tags"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                models = response.json().get('models', [])
                all_models = []
                vision_models = []
                
                for model in models:
                    # Use full model name (including version)
                    full_name = model['name']
                    all_models.append(full_name)
                    
                    # Also identify likely vision models
                    if any(v in full_name.lower() for v in ['llava', 'bakllava', 'moondream', 'vision', 'clip', 'multimodal']):
                        vision_models.append(full_name)
                
                # Store both all models and vision models
                st.session_state['all_models'] = all_models
                st.session_state['vision_models'] = vision_models
                
                return True, all_models
            else:
                return False, str(e)
                
        except Exception as e:
            return False, str(e)
            
    def run_color_test(self, base64_image, model):
        """Run color recognition test"""
        prompt = "What are the main colors in this image? List them in a single sentence."
        return self.send_vision_request(prompt, base64_image, model)
        
    def run_shape_test(self, base64_image, model):
        """Run shape recognition test"""
        prompt = "What geometric shapes do you see in this image? Describe them in one sentence."
        return self.send_vision_request(prompt, base64_image, model)
        
    def run_general_test(self, base64_image, model):
        """Run general vision analysis"""
        prompt = "Briefly describe what you see in this image in one or two sentences."
        return self.send_vision_request(prompt, base64_image, model)
        
    def run(self):
        st.title("👁️ Ollama Vision Capabilities Tester")
        st.markdown("Test and showcase the computer vision capabilities of Ollama AI models")
        
        # Sidebar for configuration
        with st.sidebar:
            st.header("⚙️ Configuration")
            
            # Server URL
            ollama_url = st.text_input(
                "Ollama Server URL",
                value="http://localhost:11434",
                help="URL of your Ollama server"
            )
            st.session_state['ollama_url'] = ollama_url
            
            # Model selection
            st.subheader("Model Selection")
            
            # Test connection button
            if st.button("🔗 Test Connection", type="primary"):
                with st.spinner("Testing connection..."):
                    success, result = self.test_connection()
                    
                if success:
                    st.success("✅ Connection successful!")
                    if result:
                        st.info(f"Found {len(result)} total models")
                        vision_models = st.session_state.get('vision_models', [])
                        if vision_models:
                            st.info(f"Likely vision models: {', '.join(vision_models)}")
                        else:
                            st.warning("No obvious vision models detected, but you can try any model")
                    else:
                        st.warning("No models found. Make sure to pull a model first")
                else:
                    st.error(f"❌ Connection failed: {result}")
            
            # Model dropdown - show all models
            available_models = st.session_state.get('all_models', ['llava:13b', 'llava', 'llava-13b', 'bakllava', 'moondream'])
            selected_model = st.selectbox(
                "Select Model (All Available Models)",
                available_models,
                help="Choose any model. Vision models are recommended for image analysis"
            )
            
            # Show vision model indicator
            vision_models = st.session_state.get('vision_models', [])
            if selected_model in vision_models:
                st.success("👁️ This is likely a vision model")
            else:
                st.info("ℹ️ This may not be a vision model, but you can try it")
        
        # Main content area
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.header("📸 Image Upload")
            
            # Image upload
            uploaded_file = st.file_uploader(
                "Choose an image",
                type=['jpg', 'jpeg', 'png', 'bmp', 'gif', 'tiff'],
                help="Upload an image to test vision capabilities"
            )
            
            if uploaded_file is not None:
                # Display image
                image = Image.open(uploaded_file)
                st.image(image, caption="Uploaded Image", use_container_width=True)
                
                # Convert to base64
                base64_image = self.encode_image_to_base64(image)
                st.session_state['base64_image'] = base64_image
                st.session_state['image_uploaded'] = True
                
                # Image info
                st.subheader("📊 Image Information")
                st.write(f"**Format:** {image.format}")
                st.write(f"**Size:** {image.size}")
                st.write(f"**Mode:** {image.mode}")
                
            else:
                st.session_state['image_uploaded'] = False
                st.info("Please upload an image to begin testing")
        
        with col2:
            st.header("🧪 Vision Tests")
            
            # Test buttons
            if st.session_state.get('image_uploaded', False):
                test_col1, test_col2, test_col3 = st.columns(3)
                
                with test_col1:
                    if st.button("🎨 Color Test", type="primary", use_container_width=True):
                        self.run_test_with_progress("Color Recognition", self.run_color_test, 
                                                   st.session_state['base64_image'], selected_model)
                
                with test_col2:
                    if st.button("📐 Shape Test", type="primary", use_container_width=True):
                        self.run_test_with_progress("Shape Recognition", self.run_shape_test,
                                                   st.session_state['base64_image'], selected_model)
                
                with test_col3:
                    if st.button("🔍 General Test", type="primary", use_container_width=True):
                        self.run_test_with_progress("General Vision", self.run_general_test,
                                                   st.session_state['base64_image'], selected_model)
            else:
                st.warning("Please upload an image first")
            
            # Results section
            st.header("📋 Results")
            
            if 'test_results' in st.session_state:
                st.markdown(f"### {st.session_state.get('test_name', 'Test Results')}")
                st.text_area(
                    "Model Response:",
                    value=st.session_state['test_results'],
                    height=300,
                    disabled=True,
                    help="The model's analysis of your image"
                )
                
                # Download results
                results_text = f"=== {st.session_state.get('test_name', 'Test Results')} ===\n"
                results_text += f"Model: {selected_model}\n"
                results_text += f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                results_text += st.session_state['test_results']
                
                st.download_button(
                    label="📥 Download Results",
                    data=results_text,
                    file_name=f"vision_test_{int(time.time())}.txt",
                    mime="text/plain"
                )
            else:
                st.info("Run a test to see results here")
        
        # Footer
        st.markdown("---")
        st.markdown(
            "<div style='text-align: center; color: gray;'>"
            "Computer Vision Final Project"
            "</div>",
            unsafe_allow_html=True
        )
    
    def run_test_with_progress(self, test_name, test_function, base64_image, model):
        """Run test with progress indicator"""
        with st.spinner(f"Running {test_name}..."):
            result = test_function(base64_image, model)
            st.session_state['test_results'] = result
            st.session_state['test_name'] = test_name
            st.rerun()

def main():
    app = OllamaVisionWebTester()
    app.run()

if __name__ == "__main__":
    main()
