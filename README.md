# iBet API Documentation

Welcome to the iBet API documentation! iBet is a betting platform built using Django Rest Framework (DRF) that allows users to compete against each other in iMessage games. Users can sign up, log in, stake bets on preferred games, and engage in competitive matches. This README will guide you through setting up and running the iBet API on your local server, and also show you how to access the API documentation using Swagger and ReDoc.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the API](#running-the-api)
- [API Documentation](#api-documentation)

## Prerequisites

Before you proceed, make sure you have the following installed on your system:

- Python (version 3.6 or higher)
- Pip (Python package manager)

## Installation

1. Clone the iBet repository from GitHub:

   ```bash
   git clone https://github.com/Opeoluwa-Fatunmbi/iBet
   cd iBet
   ```

2. Create and activate a virtual environment (recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the project dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Running the API

1. Apply database migrations:

   ```bash
   python manage.py migrate
   ```

2. Create a superuser for the Django admin panel:

   ```bash
   python manage.py createsuperuser
   ```

3. Start the development server:

   ```bash
   python manage.py runserver
   ```

4. Open your web browser and navigate to `http://127.0.0.1:8000/admin/` to access the Django admin panel. Log in using the superuser credentials you created earlier.

## API Documentation

iBet API comes with built-in documentation powered by DRF-YASG. You can explore and test the API using Swagger and ReDoc.

- Swagger UI: To view and interact with the API using Swagger UI, go to `http://127.0.0.1:8000/api/swagger/` in your web browser.

- ReDoc: For a more user-friendly API documentation interface, navigate to `http://127.0.0.1:8000/api/redoc/` in your web browser.

Feel free to explore the available endpoints, request formats, and responses to understand how to use the iBet API effectively.
