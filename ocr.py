import os
import time
import threading
import asyncio
from flask import Flask, render_template, request, jsonify, session
from werkzeug.utils import secure_filename
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# from  llm_utils import create_cvs,retrieve
from cv_ocr import process_cv
import ollama
import chromadb
import uuid
from ollama import chat
from ollama import ChatResponse

app = Flask(__name__)
app.secret_key = "your-secret-key"
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# Global dictionary to hold processing status for each file.
# Key: filepath; Value: dict with progress, done flag, and result text.
progress_status = {}
client = chromadb.Client()
collection = client.get_or_create_collection(name="cvs")
def create_cv_record(candidate,filename):
    
    # t = ""
    # for k,val in candidate.items():
    #     t += f"{k}: "+val
    # t = (
    #        f"Name: {candidate['Name']}\n"
    #        f"Education: {candidate['Education']}\n"
    #        f"Work Experience: {candidate['Work_Experience']}\n"
    #        f"Skills: {candidate['Skills']}\n"
    #        f"Certifications: {candidate['Certifications']}\n"
    #        f"Additional Info: {candidate['Additional_Info']}\n"
    #    )
    response = ollama.embed(model="mxbai-embed-large", input=candidate)
    embeddings1 = response["embeddings"]
    # print(embeddings)
    collection.add(
        ids=[str(uuid.uuid4())],
        embeddings=embeddings1,
        documents=[candidate],
        metadatas={"filename": filename},
    )
def llm_format_cv(cv_text_dic):
    # Aggregate the CV text from the dictionary
    text = ""
    for k, val in cv_text_dic.items():
        text += " " + val

    # Refined prompt that integrates the CV text
    prompt = f"""
    You are an expert HR analyst. Below is a CV text extracted from a candidate’s resume.

    Extract and structure the information in JSON format using the following keys:
    - "Personal Information"
    - "Education"
    - "Work_Experience"
    - "Projects"
    - "Skills"
    - "Certifications"

    For any key that is not present in the CV, please return an empty string as its value. 
    If there are additional relevant sections not covered by the above keys, add them with an appropriate title.

    CV Text:
    {text}

    Return only the JSON output.
    """

    response: ChatResponse = chat(
        model='llama3.1',
        messages=[{'role': 'user', 'content': prompt}],
    )
    print(response.message.content)
    # print(response['message']['content'])
    # or access fields directly from the response object
    return response.message.content
def llm_sumarize_cv(query,documents):
    retrieved_documents_and_metadata =  documents
    user_query = query
    prompt = f"""
    You are an expert HR analyst with access to a collection of candidate profiles and their metadata. Each candidate profile includes information such as skills, education, work experience, certifications, and the name of the file (which corresponds to the candidate’s CV). The file name should be mentioned in your answer to help easily locate the candidate CV.

    The retrieved candidate information is as follows:
    {retrieved_documents_and_metadata}

    User Query: "{user_query}"

    Based on the candidate profiles and metadata provided, please answer the query in a clear and structured JSON format. Consider the following:
    - If the query is about finding candidates with specific skills, list the candidates who possess those skills along with details (e.g., years of experience, proficiency) and include the file name.
    - If the query is about comparing education levels, provide a side-by-side comparison of the candidates’ education credentials, including the file names.
    - If the query is about searching for experience in specific industries, identify and list the candidates with relevant industry experience along with key details and their file names.
    - If the query is about identifying matching candidates for job requirements, summarize which candidates best match the provided job requirements, explain why, and include the associated file names.

    Return only the final answer in string response format not json.
    """

    from ollama import chat
    from ollama import ChatResponse

    response: ChatResponse = chat(model='llama3.1', messages=[
    {
        'role': 'user',
        'content': prompt,
    },
    ])
    # print(response['message']['content'])
    # or access fields directly from the response object
    return response.message.content

def retrieve(prompt):
    # prompt = "who know how to program in c++?"
    #collection = client.get_collection('cvs')
    # generate an embedding for the input and retrieve the most relevant doc
    response = ollama.embed(
    model="mxbai-embed-large",
    input=prompt
    )
    results = collection.query(
    query_embeddings=response["embeddings"],
    n_results=3
    )
    # data = data['metadatas']+ results['documents'] 
    return results
def process_file(filepath):
    """Simulated processing function for a single file."""
    global progress_status
    progress_status[filepath] = {"progress": 0, "done": False, "result": ""}
    print("cccccccccccccccccccc",filepath)

    import os
    cv_text_dic  = process_cv(filepath)
    candidate = llm_format_cv(cv_text_dic)
    create_cv_record(candidate,os.path.basename(filepath))

    total_steps = 10  # Simulate processing in 10 steps
    for i in range(total_steps):
        time.sleep(1)  # Simulate work (replace with real processing)
        progress_status[filepath]["progress"] = int((i + 1) / total_steps * 100)
    # After processing, set a dummy result; you might extract text or summaries here.
    progress_status[filepath]["result"] = f"Processed content from {os.path.basename(filepath)}"
    progress_status[filepath]["done"] = True

def process_ask(query, aggregated_results):
    """Simulated processing function for handling an 'ask' query.
       You can enhance this to use an LLM or other processing logic."""
    docs = retrieve(query)
    res = llm_sumarize_cv(query,docs)
    # For example, simply return a response combining the query and aggregated results.
    return f"answer: {res}"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    if "files" not in request.files:
        return jsonify({"error": "No file part"}), 400

    files = request.files.getlist("files")
    if not files or len(files) == 0:
        return jsonify({"error": "No selected files"}), 400

    uploaded_files = []
    for file in files:
        if file.filename == "":
            continue
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)
        uploaded_files.append(filepath)

    # Store list of filepaths in session
    session["uploaded_files"] = uploaded_files
    return jsonify({"message": "Files uploaded successfully", "filepaths": uploaded_files})

@app.route("/process", methods=["POST"])
def process():
    uploaded_files = session.get("uploaded_files")
    # create_cvs()
    if not uploaded_files:
        return jsonify({"error": "No files uploaded"}), 400
    # Start processing each file in its own thread.
    for filepath in uploaded_files:
        thread = threading.Thread(target=process_file, args=(filepath,))
        thread.start()
    return jsonify({"message": "Processing started for all files"})

@app.route("/progress", methods=["GET"])
def progress():
    uploaded_files = session.get("uploaded_files")
    if not uploaded_files:
        return jsonify([])
    # Return a list of progress dictionaries for each file.
    progress_list = []
    for filepath in uploaded_files:
        status = progress_status.get(filepath, {"progress": 0, "done": False, "result": ""})
        progress_list.append({
            "filepath": filepath,
            "filename": os.path.basename(filepath),
            "progress": status["progress"],
            "done": status["done"]
        })
    return jsonify(progress_list)

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    query = data.get("query", "")
    uploaded_files = session.get("uploaded_files")
    if not uploaded_files:
        return jsonify({"error": "No files uploaded"}), 400

    # Aggregate results from all processed files.
    aggregated_results = ""
    for filepath in uploaded_files:
        status = progress_status.get(filepath, {})
        aggregated_results += status.get("result", "") + "\n"
    
    response_text = process_ask(query, aggregated_results)
    return jsonify({"response": response_text})

if __name__ == "__main__":
    app.run(debug=True)
