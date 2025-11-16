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

### ✔ Uses the public /messages API

Messages retrieved from:

https://november7-730026606190.europe-west1.run.app/messages
