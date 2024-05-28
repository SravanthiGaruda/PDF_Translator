# PDF Translator
This project allows users to upload a PDF file and translate its content to a target language of their choice. The translated PDF is then made available for download. The translation is performed using the MarianMTModel from the Hugging Face Transformers library.

## Models Used
- **MarianMTModel**: A sequence-to-sequence model for machine translation, used to translate text from one language to another.
- **MarianTokenizer**: Tokenizer for the MarianMTModel, used to preprocess input text before translation.
- **PDFMiner**: A tool for extracting text from PDF files.
- **FPDF**: A library for creating PDF files in Python.

## Technologies Used
- **Python**: Programming language used for backend development.
- **HTML**: Markup language used for creating the web interface.
- **CSS**: Styling language used for styling the web interface.
- **Flask**: Web framework used for building the web application.
- **Hugging Face Transformers**: Library used for natural language processing tasks, including machine translation.

## Installation
1. **Clone the repository:**
    ```bash
    git clone https://github.com/your_username/pdf-translator.git
    cd pdf-translator
    ```

2. **Install the required Python packages:**
    ```bash
    pip install flask transformers pdfminer.six fpdf
    ```

3. **Optionally, install other dependencies:**
    - `langid`: Used for language detection.
    - `nltk`: Used for tokenization (optional, depending on your requirements).
    ```bash
    pip install langid nltk
    ```

## Usage
1. **Run the Flask application:**
    ```bash
    python app.py
    ```

2. **Open your web browser and navigate to `http://localhost:5000`.**

3. **Upload a PDF file and select the target language for translation.**

4. **Click the "Translate" button.**

5. **Once the translation is complete, the translated PDF will be downloaded automatically.**

## File Structure
- **app.py**: Flask application file containing the main logic for file upload, translation, and PDF creation.
- **templates/index.html**: HTML template for the web interface.
- **uploads**: Directory to store uploaded PDF files.
- **backend**: Directory containing backend files such as fonts.

---

Feel free to copy and paste this content directly into your GitHub README file. Let me know if you need any further assistance!
