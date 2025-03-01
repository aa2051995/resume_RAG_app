# resume_RAG_app

A resume parsing and retrieval application that uses OCR to extract information from resumes, stores the results in a Chroma vector store, and enables querying on resumes to match candidates to job descriptions.

## Overview

This application parses resumes (PDF files) using OCR, stores the extracted data in a vector store, and allows HR professionals to query and compare candidate profiles. The system leverages a locally hosted Llama 3.1 model for indexing and retrieval via LlamaIndex and Ollama Embedding, while Chroma DB stores the documents and their embeddings. A Flask-based web interface allows users to upload files, trigger processing, and interact with the system through a chatbot-like interface.

## Dependencies

- **PaddleOCR**: Extracts information from PDF files using OCR.
- **Ollama**: Hosts the Llama 3.1 model on a local environment.
- **LlamaIndex & Ollama Embedding**: Used for indexing and retrieval.
- **Chroma DB**: Stores and retrieves documents along with their embeddings.
- **Flask**: Provides a web interface for file uploads and a chat interface for queries.

## User Interface

- **File Upload**: A simple interface to upload resume files (PDF/Word).
- **Processing**: Click the "Process" button to extract information from resumes via OCR. The data is then stored in the vector store.
- **Querying**: After processing, users can enter queries about the resumes. The LLM will summarize answers, helping identify candidates matching specific job requirements.

## Installation

1. **Install Ollama:**
   - Download and install [Ollama](https://github.com/ollama/ollama).
   - Pull the Llama 3.1 model:
     ```bash
     ollama pull llama3.1
     ```

2. **Set Up Python Environment:**
   - Create and activate a conda environment:
     ```bash
     conda create -n resume_app python=3.10
     conda activate resume_app
     ```

3. **Install Dependencies:**
   - Install Flask:
     ```bash
     pip install flask
     ```
   - Install Chroma DB (refer to [Chroma DB installation guide](https://docs.trychroma.com/)).
   - Install LlamaIndex:
     ```bash
     pip install llama-index
     ```
   - Install Ollama integration for LlamaIndex:
     ```bash
     pip install llama-index-llms-ollama
     ```
   - Ensure that the requirements file (e.g., `requirements.txt` or `environment.yml`) includes all the packages needed for this project.

## Usage

1. Start the Flask application:
   ```bash
   flask run
