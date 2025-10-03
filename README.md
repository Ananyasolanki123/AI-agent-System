# 🚀 Insight Agent: AI Data & Research Assistant

**Insight Agent** is a sophisticated **multi-agent AI system** that helps you analyze both **structured datasets** (CSVs, Excel) and **unstructured documents** (PDFs, DOCX). Simply upload a file and interact with it using **natural language** to get insights, generate charts, summarize content, or ask specific questions.

---

## ✨ Key Features

* **🧮 Dual-Capability Analysis**
  Seamlessly works with **tabular data** and **text-based documents** in one interface.

* **💬 Natural Language Q&A**
  Ask complex questions in plain English and get precise answers.

* **📊 Automated Chart Generation**
  Creates **interactive Plotly charts** from data (e.g., “Plot sales trends over time”).

* **📖 Intelligent Document Analysis**
  Summarizes research papers, extracts keywords, and answers content-based questions via a **RAG pipeline**.

* **🤖 Smart Agent Routing**
  A central orchestrator routes your request to the correct specialist agent (**Data** or **Research**).

---

## 🏗️ System Architecture

Insight Agent is powered by a **multi-agent architecture**:

* **Central Orchestrator Agent** – interprets your query and delegates to…

  * **Data Agent** – handles CSV/Excel analysis
  * **Research Agent** – handles PDF/DOCX analysis

**Frontend:** Streamlit
**Backend:** FastAPI (with Uvicorn)
**AI/ML:** LangChain, Groq (Llama 3.1), RAG, Pandas, Plotly
**Databases:** ChromaDB (vector storage), SQLite (structured storage)
**Deployment:** Docker + Docker Compose

---

## 🛠️ Tech Stack

| Category       | Technologies                                     |
| -------------- | ------------------------------------------------ |
| **Backend**    | FastAPI, Uvicorn                                 |
| **Frontend**   | Streamlit                                        |
| **AI/ML**      | LangChain, Groq (Llama 3.1), RAG, Pandas, Plotly |
| **Database**   | ChromaDB, SQLite                                 |
| **Deployment** | Docker, Docker Compose                           |

---

## 🚀 Getting Started

### ✅ Prerequisites

* [Docker](https://www.docker.com/) & Docker Compose installed
* A **Groq API key**

### 🔧 Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-username/insight-agent.git
   cd insight-agent
   ```

2. **Create an Environment File**
   In the project root, create a `.env` file and add:

   ```bash
   GROQ_API_KEY="your_groq_api_key_here"
   ```

3. **Build and Run with Docker Compose**

   ```bash
   docker compose up --build
   ```

4. **Access the App**
   Open your browser: [http://localhost:8501](http://localhost:8501)

---

## 📖 How to Use

1. **Upload a File** – Choose a dataset (`.csv`, `.xlsx`) or a document (`.pdf`, `.docx`).
2. **Process the File** – Click **Upload** to send it to the backend.
3. **Ask a Question** – Enter your query in natural language and click **Analyze**.

---

## 💡 Example Queries

### 📊 For a Sales CSV

* *"What were the total sales?"*
* *"What is the average price of a product?"*
* *"Plot the revenue trends by month."*

### 📖 For a Research PDF

* *"Summarize this paper."*
* *"What are the main keywords?"*
* *"What methods were used in this study?"*

---

## 🌟 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to change.

---
