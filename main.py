import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import requests
import base64
import json
from PIL import Image, ImageTk
import io
import threading
import os

class OllamaVisionTester:
    def __init__(self, root):
        self.root = root
        self.root.title("Ollama Vision Capabilities Tester")
        self.root.geometry("1200x800")
        
        # Ollama server configuration
        self.ollama_url = "http://localhost:11434"
        self.current_model = "llava"
        
        # Image storage
        self.current_image = None
        self.image_path = None
        
        # Setup UI
        self.setup_ui()
        
    def setup_ui(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Server Configuration Frame
        config_frame = ttk.LabelFrame(main_frame, text="Ollama Server Configuration", padding="10")
        config_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(config_frame, text="Server URL:").grid(row=0, column=0, sticky=tk.W)
        self.url_entry = ttk.Entry(config_frame, width=40)
        self.url_entry.insert(0, self.ollama_url)
        self.url_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        
        ttk.Label(config_frame, text="Model:").grid(row=0, column=2, sticky=tk.W, padx=(20, 0))
        self.model_var = tk.StringVar(value=self.current_model)
        self.model_combo = ttk.Combobox(config_frame, textvariable=self.model_var, width=15)
        self.model_combo['values'] = ('llava', 'llava-13b', 'bakllava', 'moondream')
        self.model_combo.grid(row=0, column=3, sticky=tk.W, padx=(5, 0))
        
        ttk.Button(config_frame, text="Test Connection", command=self.test_connection).grid(row=0, column=4, padx=(20, 0))
        
        # Left Panel - Image Selection
        left_frame = ttk.LabelFrame(main_frame, text="Image Selection", padding="10")
        left_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        ttk.Button(left_frame, text="Select Image", command=self.select_image).grid(row=0, column=0, pady=(0, 10))
        
        # Image display
        self.image_label = ttk.Label(left_frame, text="No image selected", relief=tk.SUNKEN, anchor=tk.CENTER)
        self.image_label.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.image_label.configure(width=40, height=20)
        
        left_frame.columnconfigure(0, weight=1)
        left_frame.rowconfigure(1, weight=1)
        
        # Right Panel - Test Controls and Results
        right_frame = ttk.Frame(main_frame)
        right_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Test buttons
        test_frame = ttk.LabelFrame(right_frame, text="Vision Tests", padding="10")
        test_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(test_frame, text="Test Color Recognition", command=self.test_color_recognition).grid(row=0, column=0, padx=(0, 5), pady=2)
        ttk.Button(test_frame, text="Test Shape Recognition", command=self.test_shape_recognition).grid(row=0, column=1, padx=(0, 5), pady=2)
        ttk.Button(test_frame, text="Test General Vision", command=self.test_general_vision).grid(row=0, column=2, pady=2)
        
        # Results area
        results_frame = ttk.LabelFrame(right_frame, text="Results", padding="10")
        results_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Results text with scrollbar
        self.results_text = tk.Text(results_frame, wrap=tk.WORD, width=60, height=20)
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=scrollbar.set)
        
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(1, weight=1)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
    def select_image(self):
        file_path = filedialog.askopenfilename(
            title="Select an image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff")]
        )
        
        if file_path:
            self.image_path = file_path
            self.display_image(file_path)
            self.status_var.set(f"Image selected: {os.path.basename(file_path)}")
            
    def display_image(self, file_path):
        try:
            # Load and resize image for display
            image = Image.open(file_path)
            
            # Calculate thumbnail size to fit in the label
            max_width, max_height = 400, 300
            image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage and display
            photo = ImageTk.PhotoImage(image)
            self.image_label.configure(image=photo, text="")
            self.image_label.image = photo  # Keep a reference
            
            # Store PIL image for processing
            self.current_image = Image.open(file_path)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {str(e)}")
            
    def test_connection(self):
        def test_thread():
            try:
                url = self.url_entry.get().rstrip('/')
                response = requests.get(f"{url}/api/tags", timeout=5)
                if response.status_code == 200:
                    models = response.json().get('models', [])
                    model_names = [model['name'].split(':')[0] for model in models]
                    
                    # Update model combo box
                    self.root.after(0, lambda: self.update_models(model_names))
                    self.root.after(0, lambda: self.status_var.set("Connection successful"))
                else:
                    self.root.after(0, lambda: self.status_var.set("Connection failed"))
                    
            except Exception as e:
                self.root.after(0, lambda: self.status_var.set(f"Connection error: {str(e)}"))
                
        threading.Thread(target=test_thread, daemon=True).start()
        
    def update_models(self, models):
        self.model_combo['values'] = tuple(models)
        if models and self.model_var.get() not in models:
            self.model_var.set(models[0])
            
    def encode_image_to_base64(self, image_path):
        """Encode image to base64 string"""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
            
    def send_vision_request(self, prompt, image_path):
        """Send vision request to Ollama"""
        try:
            url = f"{self.url_entry.get().rstrip('/')}/api/generate"
            
            # Encode image
            base64_image = self.encode_image_to_base64(image_path)
            
            # Prepare request payload
            payload = {
                "model": self.model_var.get(),
                "prompt": prompt,
                "stream": False,
                "images": [base64_image]
            }
            
            response = requests.post(url, json=payload, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', 'No response received')
            else:
                return f"Error: HTTP {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Error: {str(e)}"
            
    def test_color_recognition(self):
        if not self.image_path:
            messagebox.showwarning("Warning", "Please select an image first")
            return
            
        prompt = """Analyze the colors in this image in detail. Please:
1. List all the dominant colors you can identify
2. Be specific about color shades and tones (e.g., "navy blue" instead of just "blue")
3. Mention any color gradients or transitions
4. Identify any color patterns or color schemes
5. Estimate the percentage of each color in the image"""
        
        self.run_vision_test("Color Recognition", prompt)
        
    def test_shape_recognition(self):
        if not self.image_path:
            messagebox.showwarning("Warning", "Please select an image first")
            return
            
        prompt = """Identify and analyze all geometric shapes in this image. Please:
1. List all shapes you can identify (circles, squares, triangles, rectangles, etc.)
2. Describe their positions and locations relative to each other
3. Estimate their sizes and proportions
4. Identify any patterns or arrangements of shapes
5. Note any complex shapes or combinations of basic shapes"""
        
        self.run_vision_test("Shape Recognition", prompt)
        
    def test_general_vision(self):
        if not self.image_path:
            messagebox.showwarning("Warning", "Please select an image first")
            return
            
        prompt = """Provide a comprehensive analysis of this image. Please describe:
1. All objects and elements you can identify
2. Colors and their distribution
3. Shapes and geometric patterns
4. Spatial relationships between elements
5. Any text or symbols present
6. Overall composition and style
7. Notable details or interesting features"""
        
        self.run_vision_test("General Vision Analysis", prompt)
        
    def run_vision_test(self, test_name, prompt):
        def test_thread():
            # Update UI
            self.root.after(0, lambda: self.results_text.delete(1.0, tk.END))
            self.root.after(0, lambda: self.results_text.insert(tk.END, f"Running {test_name}...\n\n"))
            self.root.after(0, lambda: self.status_var.set(f"Running {test_name}..."))
            
            # Send request
            result = self.send_vision_request(prompt, self.image_path)
            
            # Display results
            self.root.after(0, lambda: self.display_results(test_name, result))
            
        threading.Thread(target=test_thread, daemon=True).start()
        
    def display_results(self, test_name, result):
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, f"=== {test_name} Results ===\n\n")
        self.results_text.insert(tk.END, result)
        self.results_text.insert(tk.END, f"\n\n{'='*50}")
        
        self.status_var.set(f"{test_name} completed")

def main():
    root = tk.Tk()
    app = OllamaVisionTester(root)
    root.mainloop()

if __name__ == "__main__":
    main()
