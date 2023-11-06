# Document chatbot

This repository contains the source code for a website with chatbot functionality. The chatbot provides 
Retrieval-augmented generation (RAG) functionality, meaning it's designed to answer questions about topics for which 
there is information in the database. The database can be updated at any time to extend the scope of topics that the 
chatbot can provide answers for.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)


## Introduction

This project is designed to create a website with chatbot functionality where the users can ask questions related to a 
corpus of documents which are pre-processed and kept in the database. The pre-processing of the documents consists of 
splitting them in relatively small chunks that usually contain a couple of pieces of important information, then 
generating a vector embedding for each chunk. Afterward, these embeddings are used to retrieve the most important parts 
of the documents for each user question. Apart from posing the questions, the user will be able to select which LLM to 
use for generating an answer. Some of the options will be LLM accessible via API (E.g. ChatGPT), while others will be 
open-source LLMs used locally on our server.

The backend, developed using FastAPI, provides a robust API to serve the frontend, built with Angular. The chatbot is 
powered by LangChain, a framework for building LLM applications, and Chroma DB, a vector database.

## Features

- Interactive chatbot powered by Langchain.
- User-friendly Angular frontend.
- Efficient and scalable FastAPI backend.
- Integration with Chroma DB for chatbot interactions.
- Easily extensible and customizable.

## Prerequisites

Before getting started with this project, make sure you have the following prerequisites installed:

- Python 3.10+
- Node.js and npm
- Angular CLI
- Chroma DB
- LangChain
- Git (optional)

## Getting Started

Follow the steps below to set up and run the project locally.

Clone this repository (or download the source code):

   ```bash
   git clone https://github.com/yourusername/your-repo.git
   ```

### Backend Setup
   
1. Navigate to the backend directory:
    ```bash
    cd backend
2. Install Poetry (if not already installed) and follow the prompts to set up your project's information.
    ```bash
   poetry init
   ```
3. Initialize the Poetry project:
    ```bash
   poetry install
   ```
4. Start the FastAPI backend:
    ```bash
   poetry run uvicorn backend.api.api:app
   ```
The FastAPI backend should now be running on http://localhost:8000.

### Frontend Setup
1. Navigate to the frontend directory:
    ```bash
    cd frontend
    ```
2. Install Angular CLI (if not already installed):
    ```bash
    npm install -g @angular/cli
    ```

3. Install the frontend dependencies:
    ```bash
    npm install
    ```

4. Start the Angular development server:
    ```bash
    ng serve --port 4200 --proxy-config proxy.conf.json
    ```

The Angular development server should now be running on http://localhost:4200.