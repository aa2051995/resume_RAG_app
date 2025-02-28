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
def create_cv_record(candidate):
    
    t = ""
    for k,val in candidate.items():
        t += " "+val
    # t = (
    #        f"Name: {candidate['Name']}\n"
    #        f"Education: {candidate['Education']}\n"
    #        f"Work Experience: {candidate['Work_Experience']}\n"
    #        f"Skills: {candidate['Skills']}\n"
    #        f"Certifications: {candidate['Certifications']}\n"
    #        f"Additional Info: {candidate['Additional_Info']}\n"
    #    )
    response = ollama.embed(model="mxbai-embed-large", input=t)
    embeddings1 = response["embeddings"]
    # print(embeddings)
    collection.add(
        ids=[str(uuid.uuid4())],
        embeddings=embeddings1,
        documents=[t]
    )
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
    data = results['documents']
    return data
def process_file(filepath):
    """Simulated processing function for a single file."""
    global progress_status
    progress_status[filepath] = {"progress": 0, "done": False, "result": ""}
    print("cccccccccccccccccccc",filepath)
    cv_text_dic  = process_cv(filepath)
    create_cv_record(cv_text_dic)
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
    res = retrieve(query)
    # For example, simply return a response combining the query and aggregated results.
    return f"Query: {res}"

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
