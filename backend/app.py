from flask import Flask, request, send_file, render_template
from transformers import MarianMTModel, MarianTokenizer
from pdfminer.high_level import extract_text
import os
import io
from fpdf import FPDF
import logging

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))

# Set up logging configuration
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get the uploaded file and target language
        file = request.files['file']
        target_lang = request.form['target_lang']

        # Save the uploaded file
        file_path = os.path.join(UPLOAD_FOLDER, 'uploaded_file.pdf')
        file.save(file_path)

        logger.debug("Uploaded file saved at: %s", file_path)

        # Translate the PDF
        translated_text = pdf_translator(file_path, target_lang)
        logger.debug("Translated Text Length: %d", len(translated_text))
        logger.debug("Translated Text: %s", translated_text)
        
        # Delete the uploaded file
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.debug("Uploaded file deleted")

        # Create PDF from translated text
        pdf_stream = create_pdf_from_text(translated_text)
        logger.debug("PDF Stream Length: %d", pdf_stream.getbuffer().nbytes)

        # Return the translated PDF as a downloadable file
        return send_file(pdf_stream, as_attachment=True, attachment_filename='translated_pdf.pdf')

    return render_template('index.html')

def pdf_translator(file_path, target_lang):
    # Load the translation model and tokenizer
    model_name = f"Helsinki-NLP/opus-mt-en-{target_lang}"
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)

    # Extract text from the PDF
    file_text = extract_text(file_path)

    # Log extracted text for debugging
    logger.debug("Extracted Text: %s", file_text)

    # Translate the text
    translated_text = translate_text(model, tokenizer, file_text)

    return translated_text

def translate_text(model, tokenizer, text):
    # Split text into paragraphs
    paragraphs = text.split('\n\n')

    # Translate each paragraph
    translated_paragraphs = []
    for paragraph in paragraphs:
        if paragraph.strip():  # Avoid translating empty paragraphs
            # Tokenize the paragraph for the model
            inputs = tokenizer(paragraph, return_tensors="pt", padding=True, truncation=True)
            
            # Translate the paragraph
            translated = model.generate(**inputs)
            translated_text = tokenizer.batch_decode(translated, skip_special_tokens=True)[0]
            translated_paragraphs.append(translated_text)

    # Concatenate translated paragraphs
    translated_text = '\n\n'.join(translated_paragraphs)

    return translated_text

def create_pdf_from_text(text):
    logging.basicConfig(level=logging.DEBUG)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Add DejaVuSans font
    font_path = '/Users/sravanthi/Desktop/Nvidia Contest/PDF/backend/dejavu-fonts-ttf-2.37/ttf/DejaVuSans.ttf' 
    pdf.add_font('DejaVu', '', font_path, uni=True)
    pdf.set_font('DejaVu', size=10)  # Set the initial font size to 10

    # Logging for debugging
    logging.debug("Text length: %d", len(text))

    # Split the text into paragraphs
    paragraphs = text.split('\n\n')

    # Process each paragraph
    for paragraph in paragraphs:
        # Split the paragraph into lines
        lines = paragraph.split('\n')
        
        # Process each line
        for line in lines:
            logging.debug("Processing line: %s", line)
            try:
                # Adjust the font size based on the line length
                if len(line) > 100:
                    pdf.set_font_size(8)
                else:
                    pdf.set_font_size(10)
                
                pdf.multi_cell(0, 5, line)  # Reduce the cell height to 5
            except Exception as e:
                logging.error("Error processing line: %s", e)
        
        # Add an extra line break between paragraphs
        pdf.ln()

    pdf_output = io.BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)

    return pdf_output



if __name__ == '__main__':
    app.run(debug=True)
