# 📘 Member Question-Answering Service

This project implements a simple **question-answering API** that answers natural-language questions about members using the message data from the public November7 API.

The service exposes a single endpoint:

GET /ask?question=...

yaml
Copy code

It analyzes the question, retrieves messages from the upstream API (or local fallback), finds the most relevant message using keyword scoring, and returns the best possible answer.

---

## 🚀 Features

### ✔ Natural-language question → JSON answer  
Example:

GET /ask?question=When%20is%20Layla%20planning%20her%20trip%20to%20London%3F

css
Copy code

Response:
```json
{
  "answer": "Layla Kawaguchi: Please remember I prefer aisle seats during my flights."
}
✔ Uses the public /messages API
Messages retrieved from:

bash
Copy code
https://november7-730026606190.europe-west1.run.app/messages
✔ Keyword-based retrieval
The system:

Tokenizes the question

Removes stopwords

Fetches messages

Computes keyword overlap

Returns the message with the highest score

✔ FastAPI with interactive docs
Accessible at:

bash
Copy code
/docs
📡 API Endpoint: /ask
GET /ask?question=Your+question+here
Query Param	Type	Description
question	string	Natural-language question

Example
perl
Copy code
GET /ask?question=What%20does%20Amira%20prefer%20for%20dinner%3F
Response
json
Copy code
{
  "answer": "Amira Jones: I’m craving sushi tonight!"
}
If no match is found:

json
Copy code
{
  "answer": "Sorry, I couldn't find an answer to that question in the member messages."
}
If the upstream API is unavailable:

json
Copy code
{
  "detail": "Upstream /messages API returned 402 Payment Required. Cannot fetch member messages at this time."
}
🏗️ Project Structure
css
Copy code
.
├── main.py
├── requirements.txt
└── README.md
⚙️ Running Locally
1. Clone the repo
bash
Copy code
git clone <your-repo-url>
cd <your-repo>
2. Create a virtual environment
bash
Copy code
python -m venv venv
3. Activate it
Windows (CMD):

cmd
Copy code
venv\Scripts\activate
macOS/Linux:

bash
Copy code
source venv/bin/activate
4. Install dependencies
bash
Copy code
pip install -r requirements.txt
5. Run the server
bash
Copy code
uvicorn main:app --reload --host 0.0.0.0 --port 8000
6. Open Swagger documentation
Visit:

bash
Copy code
http://localhost:8000/docs
🌐 Deployment
This service can be deployed to any platform supporting Python web apps.

Recommended: Render, Railway, Fly.io
Start command:

nginx
Copy code
uvicorn main:app --host 0.0.0.0 --port 8000
Ensure the deployed API exposes:

/ask

/docs