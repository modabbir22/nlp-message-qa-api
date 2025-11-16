# 📘 Member Question-Answering Service

This project implements a simple **question-answering API** that answers natural-language questions about members using the message data from the public November7 API.

The service exposes a single endpoint:

GET /ask?question=...


It analyzes the question, retrieves messages from the upstream API (or local fallback), finds the most relevant message using keyword scoring, and returns the best possible answer.

---

## 🚀 Features

### ✔ Natural-language question → JSON answer

**Example query:**


GET /ask?question=When%20is%20Layla%20planning%20her%20trip%20to%20London%3F


**Example response:**

```json
{
  "answer": "Layla Kawaguchi: Please remember I prefer aisle seats during my flights."
}
✔ Uses the public /messages API

Messages retrieved from:

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
🏗 Project Structure
css
Copy code
.
├── main.py
├── requirements.txt
└── README.md
⚙️ Running Locally
Clone the repo

bash
Copy code
git clone <your-repo-url>
cd <your-repo>
Create a virtual environment

bash
Copy code
python -m venv venv
Activate it

Windows (CMD):

cmd
Copy code
venv\Scripts\activate
macOS/Linux:

bash
Copy code
source venv/bin/activate
Install dependencies

bash
Copy code
pip install -r requirements.txt
Run the server

bash
Copy code
uvicorn main:app --reload --host 0.0.0.0 --port 8000
Open Swagger documentation

bash
Copy code
http://localhost:8000/docs
🌐 Deployment
This service can be deployed to any Python-friendly hosting platform.

Recommended: Render, Railway, Fly.io

Start command:
bash
Copy code
uvicorn main:app --host 0.0.0.0 --port 8000
Ensure the deployed API exposes:

/ask

/docs

yaml
Copy code
