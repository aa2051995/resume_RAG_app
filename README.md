# resume_RAG_app
parse resumes using ocr and store the results in chroma vector store, enable querying on resumes  and matching candidates to job description
dependencies: 
-  Paddleocr will extract info from pdf files.
- ollama to host lama 3.1 on local enviroment
- lamaindex and olama embedding for indexing and retrieval
- chroma db to store and retrieve documents and their embeddings
- flask for creating the chat interface and file upload
User interface:
 - simple user interface where you upload files click upload
 - Click process so it extracts info using OCR and stores files data and info
 - Then you can write queries about the CV, and llm will summarize the answer
installation:
- Download and install ollama https://github.com/ollama/ollama
- ollama pull llama3.1
- create and activate enviroment using conda
- install flask using pip install flask
- install chroma db
- install lamaindex using pip install llama-index
- install olam for lamaindex pip install llama-index-llms-ollama
  requirement file contains all possible packages 


