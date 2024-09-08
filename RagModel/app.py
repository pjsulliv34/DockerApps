import os
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from langchain_openai.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnablePassthrough, RunnableParallel

app = Flask(__name__) 

# Load environment variables from a .env file

load_dotenv()
# Retrieve the OpenAI API key from environment variables
api_key = os.getenv('api_key')

# Initialize the OpenAI client with the provided API key and model
model = ChatOpenAI(api_key=api_key, model='gpt-3.5-turbo')

# Define the prompt template for generating responses
question_template = """
You are a smart bot that answers questions based on the context given to you only.
You don't make things up.
context:{context}
question:{question}
"""
# Create a PromptTemplate instance with the defined template
prompt = PromptTemplate.from_template(template=question_template)

# Initialize components for the document processing pipeline
# Output parser to format the response from the model
parser = StrOutputParser()
# Splitter to divide text into chunks for processing
spliter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=50)
# Loader to read and split the PDF document into chunks
file_loader = PyPDFLoader('communications_with_extraterrestrial.pdf')
# Load and split the document text
document_text = file_loader.load_and_split()
# Further split the loaded document text into smaller chunks
document_text = spliter.split_documents(document_text)
# Create a FAISS vector store from the document chunks
vector_storage = FAISS.from_documents(document_text, OpenAIEmbeddings(api_key= api_key))
# Create a retriever to fetch relevant document chunks based on the query
retriever = vector_storage.as_retriever()
# Combine context retrieval and question processing in parallel
result = RunnableParallel(context=retriever, question=RunnablePassthrough())
# Create a processing chain from context retrieval to prompt formatting to model response
chain = result | prompt | model | parser

@app.route('/')
def home():
    # Render the home page with the form
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    # Retrieve the question from the form data
    question = request.form.get('question')

    if not question:
        # Return an error response if no question is provided
        return jsonify({"error": "No question provided"}), 400

    try:
        # Process the question using the chain and retrieve context used
        response = chain.invoke(question)
        context_used = retriever.invoke(question)
        
        # Format the retrieved context documents for display
        formatted_documents = [
            f"page: {doc.metadata['page']} content: {' '.join(doc.page_content.split()[:10])}..."
            for doc in context_used
        ]
        
        # Return the answer and the formatted context as a JSON response
        return jsonify({
            'answer': response,
            'context': formatted_documents  # Include the formatted context
        })
    except Exception as e:
        # Return an error response if an exception occurs
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Run the Flask application
    app.run()
