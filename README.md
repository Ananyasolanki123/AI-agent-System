AI Data & Research Intelligence Agent
This repository contains a multi-agent AI system designed to analyze and answer questions from both structured data (CSV/XLSX) and unstructured research documents (PDF/DOCX). It features a Streamlit frontend for user interaction and a FastAPI backend that orchestrates three different AI agents.

Key Features
Multi-Agent Architecture: The system uses a dedicated Orchestration Agent to intelligently route user queries to the correct specialized agent.

Data Intelligence Agent: Ingests and analyzes structured data from CSV or XLSX files. It can perform calculations, answer natural language questions, and generate interactive plots.

Research Agent: Processes unstructured documents like PDFs and DOCX files. It can provide concise summaries, extract keywords, and answer specific questions based on the document content.

Dockerized Deployment: The entire application is containerized using Docker and Docker Compose, ensuring a consistent and reproducible development and deployment environment.

Secure API Key Management: The GROQ API key is handled securely at runtime using Docker secrets and a .env file, preventing it from being hardcoded.

Getting Started
Prerequisites
Docker is required to run the application.

An API key from Groq is needed for the AI models.

Once you have your key, create a file named .env in the root of your project directory with the following content:

GROQ_API_KEY="YOUR_API_KEY_HERE"

Quick Start
Clone this repository to your local machine.

Open a terminal and navigate to the root directory of the project.

Run the following command to build the Docker images and start the services:

docker compose up --build

Once the build is complete, open your web browser and go to http://localhost:8501.

Project Structure
backend/: Contains the FastAPI application and the core AI agent logic.

frontend/: Contains the Streamlit application for the user interface.

docker-compose.yml: Defines the services and configurations for Docker.

.env: The file used to securely store your API key.

How to Use
Upload a File: Use the file uploader on the Streamlit page to select a .csv, .xlsx, .pdf, or .docx file.

Submit Query: Enter a natural language query related to the uploaded file.

For Data Files: Ask questions like "What is the total sales?" or "Plot revenue trends."

For Research Documents: Ask questions like "Summarize the paper" or "What are the key findings?"

The system will automatically route your query to the correct AI agent and display the response.
