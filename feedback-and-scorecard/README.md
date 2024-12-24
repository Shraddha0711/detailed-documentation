# Feedback & Scorecard Generation API

This repository contains a **Feedback App** that generates customer service scorecards based on input transcripts. The app uses technologies like **FastAPI**, **LangGraph**, and **OpenAI's RAG (Retrieval-Augmented Generation)**. It is containerized using **Docker** and orchestrated using **Docker Compose**. The application also securely manages Firebase database credentials using **Docker Swarm secrets**.

## Table of Contents

- [Overview](#overview)
- [Technologies Used](#technologies-used)
- [How It Works](#how-it-works)
- [Firebase Database Connection and Credential Management](#firebase-database-connection-and-credential-management)
- [Setting Up Secrets](#setting-up-secrets)
- [Building the Docker Image](#building-the-docker-image)
- [Running the Application](#running-the-application)
- [Docker Compose Configuration](#docker-compose-configuration)
- [Docker Swarm Setup](#docker-swarm-setup)

---

## Overview

The **Feedback App** provides an automated way to evaluate customer service interactions. It generates various scores based on factors such as **empathy**, **clarity**, **problem resolution**, **engagement**, and more. These scores are used to create a comprehensive **scorecard** for each interaction.

The app is built using **FastAPI** for fast web service development, **LangGraph** for building state machines to handle multiple feedback metrics, and **OpenAI** for performing natural language processing tasks. The app integrates with **Firebase** for storing feedback-related data, and securely handles sensitive credentials using **Docker Swarm secrets**.

### Key Features:
- **Scorecard Generation**: Evaluates customer service transcripts and generates scores for various metrics like empathy, clarity, and engagement.
- **Retrieval-Augmented Generation (RAG)**: Uses OpenAI’s RAG technique to improve the feedback generation process by incorporating relevant external data (e.g., documents or knowledge bases).
- **Secure Secrets Management**: Handles sensitive data, such as Firebase credentials, securely using Docker Swarm secrets.
- **Containerized Application**: The app is fully containerized using Docker and managed with Docker Compose for easy deployment.

---

## Technologies Used

- **FastAPI**: A modern web framework for building APIs, known for its fast performance and easy integration with Python-based applications.
- **LangGraph**: A Python library for building state-based workflows. It is used to manage the feedback scoring process by executing various tasks in parallel.
- **OpenAI**: The app uses OpenAI's language models for NLP tasks such as generating scores for different customer service metrics.
- **Firebase**: A NoSQL cloud database used to store feedback and scorecard data.
- **Docker**: Used to containerize the application for easy deployment and scalability.
- **Docker Compose**: Helps to define and run multi-container applications (for example, the app and Firebase-related containers).
- **Docker Swarm**: Used for managing secrets securely in a Docker environment.

---

## How It Works

1. **Input Transcript**: The application accepts a transcript of a customer service interaction as input. This could be a conversation between a customer and a service agent, including the questions, responses, and tone.
   
2. **Text Splitting**: The transcript is split into smaller chunks for easier processing using the `CharacterTextSplitter` class from LangChain.

3. **Feedback Scoring**: Each chunk of the transcript is analyzed by a series of feedback evaluation functions. These functions assess different aspects of the interaction, such as:
   - **Empathy**
   - **Clarity and Conciseness**
   - **Grammar and Language**
   - **Listening Score**
   - **Problem Resolution Effectiveness**
   - **Personalization**
   - **Conflict Management**
   - **Response Time**
   - **Customer Satisfaction**
   - **Positive Sentiment Score**
   - **Structure and Flow**
   - **Stuttering Words**
   - **Active Listening Skills**
   - **Rapport Building**
   - **Engagement**

   These functions are executed in parallel using **LangGraph** to evaluate the feedback metrics.

4. **Score Aggregation**: The results of the feedback evaluation are aggregated into a single scorecard. This scorecard includes all the individual scores and an overall assessment of the interaction.

5. **External Data Integration**: The app integrates external documents or knowledge bases using the **Retrieval-Augmented Generation (RAG)** method, providing richer and more accurate feedback. Relevant documents are retrieved from the database or vector store.

6. **Secure Credential Management**: Firebase credentials are managed securely using **Docker Swarm secrets**. These credentials are not stored directly in the Dockerfile or environment variables, ensuring they are hidden during the container build process.

---

## Firebase Database Connection and Credential Management

The application connects to **Firebase** to store the generated feedback and scorecards. Firebase requires a service account key for authentication, which contains sensitive credentials. These credentials should be securely handled using **Docker Swarm secrets**.

### How to Handle Firebase Credentials Securely:

1. **Create Docker Secret**: Store the Firebase service account credentials in a JSON file (e.g., `firebase_credentials.json`).

2. **Initialize Docker Swarm**: Run `docker swarm init` to initialize Docker Swarm, which is required for managing secrets.

3. **Store Credentials as Secret**:
    - First, create a file containing your Firebase credentials (e.g., `firebase_credentials.json`).
    - Then, create a Docker secret using the following command:
   
    ```bash
    docker secret create db_credential ./firebase_credentials.json
    ```

4. **Access Secrets in Docker Compose**: In the `docker-compose.yml` file, specify that the application requires the `db_credential` secret to be mounted during runtime.

    ```yaml
    secrets:
      db_credential:
        external: true
    ```

This way, the Firebase credentials are securely handled by Docker Swarm and are not exposed in the application code or Docker environment.

---

## Setting Up Secrets

### Step 1: Initialize Docker Swarm

Docker Swarm mode is required to manage secrets. To initialize Swarm, run the following command:

```bash
docker swarm init
```

### Step 2: Create a Secret

Create a secret by specifying a file that contains sensitive information (e.g., Firebase credentials):

```bash
docker secret create db_credential ./firebase_credentials.json
```

### Step 3: Verify the Secret

You can list all available secrets with the following command:

```bash
docker secret ls
```

---

## Building the Docker Image

To build the Docker image for the Feedback App:

1. Navigate to the project directory where the `Dockerfile` is located.
2. Run the following command to build the image:

```bash
docker build -t feedback-app .
```

---

## Running the Application

To run the application with Docker Compose:

1. Ensure you have Docker Swarm initialized and the necessary secrets created (see above).
2. Run the following command to start the application:

```bash
docker compose up --build
```

This will start the app, which will connect to Firebase, process input transcripts, and generate feedback scorecards.

---

## Docker Compose Configuration

Here is an example of the `docker-compose.yml` file used to configure the app and manage Docker secrets:

```yaml
version: "3.8"

services:
  my-app:
    image: feedback-app
    build:
      context: .
    ports:
      - "8000:8000"
    secrets:
      - db_credential

secrets:
  firebase_credential:
    external: true
```

In this example, the `db_credential` secret is required for the app to connect to Firebase securely.

---

## Docker Swarm Setup

1. **Initialize Docker Swarm**:
   - Run `docker swarm init` to initialize Docker Swarm mode.
   
2. **Create Secrets**:
   - Use `docker secret create` to store Firebase credentials as secrets.
   
3. **Deploy with Docker Compose**:
   - Use `docker compose up --build` to deploy the app with Docker Compose.

---


### Key Points:
1. **Firebase Database**: The app uses Firebase to store feedback and scorecard data.
2. **Secure Firebase Credentials**: Firebase credentials (service account key) are managed using Docker Swarm secrets.
3. **Docker Setup**: The app is containerized with Docker, and Docker Compose is used to manage services. Secrets are securely handled during the container build and runtime.
4. **How it works**: The app evaluates customer service interactions using FastAPI, LangGraph, and OpenAI, generating detailed scorecards.
