import os
from flask import Flask, request, jsonify, render_template
import openai
import PyPDF2
from dotenv import load_dotenv

app = Flask(__name__)

# Access the API key from environment variables
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
# Initialize the OpenAI client
openai.api_key = api_key

# Define the prompt template for the alien researcher
def generate_response(context, question):
    messages = [
        {"role": "system", "content": "You are an alien researcher specializing in extraterrestrial topics."},
        {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}"}
    ]
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Or the appropriate model
        messages=messages
    )
    
    # Get the response content
    content = response.choices[0].message['content'].strip()
    
    # Limit the response to 2 paragraphs
    paragraphs = content.split('\n\n')
    limited_response = '\n\n'.join(paragraphs[:2])
    
    return limited_response

# Function to read the content of a PDF
def read_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    return text

# Load the PDF text
document_text = read_pdf('communications_with_extraterrestrial.pdf')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    question = request.form.get('question')

    if not question:
        return jsonify({"error": "No question provided"}), 400

    # Generate the answer using OpenAI's ChatCompletion
    try:
        answer = generate_response(document_text, question)
        return jsonify({'answer': answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()
