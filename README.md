# Moose - The Math Game

Welcome to the Moose! This interactive game is designed to make learning math fun and engaging. Built with Flask, a lightweight WSGI web application framework, and JavaScript for dynamic content, it offers a seamless user experience for all ages.

## Description

Moose is an educational web application that challenges users with addition and subtractions problems with varying difficulties. The game is designed to improve problem-solving skills and speed in a fun, interactive way. Whether you're a student looking to sharpen your skills or an adult seeking a quick math refresher, this game is for you.

## Features

- **Interactive Math Problems**: Solve various math problems designed to test and improve your math skills.
- **Progress Tracking**: Keep track of your scores and progress over time.
- **Difficulty Levels**: Choose your difficulty level to match your math proficiency.
- **Instant Feedback**: Receive immediate feedback on your answers to understand your mistakes and learn from them.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

I followed the great Flask Mega-Tutorial for the database and user accounts. 

To enable password reset via email follow this [tutorial](https://blog.coffeeinc.in/how-to-send-a-mail-using-flask-mail-and-gmail-smtp-in-python-eb235e5b2048) and follow the comments for Installation steps 4 and 5.

### Prerequisites

Before you begin, ensure you have the following installed:
- Python (3.6 or later)
- pip (Python package installer)
- Git
- Running microservice.py in a separate terminal

## Requirements

[python3.11](https://www.python.org/downloads/)


### Installation

1. **Clone the Repository**
    ```bash
    git clone https://github.com/hiimdonald/moose.git
    cd moose
    ```

2. **Create and Activate a Virtual Environment** (Optional, but recommended)
    - For macOS/Linux:
        ```bash
        python3 -m venv .venv
        source .venv/bin/activate
        ```
    - For Windows:
        ```bash
        python -m venv .venv
        .venv\Scripts\activate
        ```

3. **Install Required Packages**
    ```bash
    pip install -r requirements.txt
    ```

### Configuration

4. **Environment Variables**
    - Create a `.env` file in the main directory and replace placeholders with your actual data.
        ```plaintext
        SECRET_KEY="YOUR_SECRET_KEY"
        MAIL_SERVER="smtp.gmail.com"
        MAIL_PORT=465
        MAIL_USE_TLS=False
        MAIL_USE_SSL=True
        MAIL_USERNAME="your-email@gmail.com"
        MAIL_PASSWORD="your-email-password"
        ADMINS="your-email@gmail.com"
        ```


5. **Application Configuration**
    - Create a `config.py` file in the main directory with the following content:
        ```python
        import os
        from dotenv import load_dotenv

        basedir = os.path.abspath(os.path.dirname(__file__))
        load_dotenv(os.path.join(basedir, ".env"))


        class Config:
            SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
            SQLALCHEMY_DATABASE_URI = os.environ.get(
                "DATABASE_URL"
            ) or "sqlite:///" + os.path.join(basedir, "app.db")

            SQLALCHEMY_TRACK_MODIFICATIONS = False
            MAIL_SERVER = os.environ.get("MAIL_SERVER")
            MAIL_PORT = os.environ.get(("MAIL_PORT") or 25)
            MAIL_USE_SSL = os.environ.get("MAIL_USE_SSL") == "True"
            MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
            MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
            ADMINS = os.environ.get("ADMINS")
        ```

6. **Database Initialization and Migration**
    - Initialize and migrate the database with the following command:
        ```bash
        flask setup-db
        ```
### Flask Environment Configuration (Optional)

7. **Set Flask Environment Variables**
   - Creating a `.flaskenv` file in the main project directory can simplify the process of setting environment variables for Flask. This step is optional but can make running the application easier. Add the following lines to your `.flaskenv` file:

    ```plaintext
    FLASK_APP=mathy.py
    FLASK_ENV=development  # Use 'development' for debug mode or 'production' for production mode
    FLASK_RUN_PORT=8000
    ```

   - This file sets the entry point for the Flask application (`mathy.py`), the environment (development or production), and the port Flask will serve the application on. Adjust `FLASK_APP` to match the name of your main Flask script if it's different from `mathy.py`.


### Running the Microservice.py Application

- In a separate terminal start the application with:
    ```bash
    python microservice.py
    ```

### Running the Flask Application

- Start the application with:
    ```bash
    flask run
    ```
- Access the game at `http://127.0.0.1:8000/` in your web browser.


## Security

Ensure your `.env` file containing sensitive information like email credentials and secret keys is secure and never commit it to a public repository.

# Microservice Communication Contract

This document outlines the communication contract for the microservice implemented to support random data generation for a Flask-based web application. My partner will import the ZMQ module to their app, and then setup a request socket as described below:

### A. How to Request Data

Establish a ZeroMQ REQ socket and connect to the microservice endpoint. Send a string message "generate_numbers" to request random number generation. Await a JSON response containing the generated numbers.

- Setup ZeroMQ context and REQ socket:
    ```bash
    import zmq

    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://127.0.0.1:5555")
    ```

- Request data:
    ```bash

    socket.send_string("generate_numbers")
    ```

### B. How to Receive Data

Upon sending a request, the microservice will respond with a JSON object containing three keys: num1, page_num, and num2, each associated with a randomly generated number. 

- Receive response:
    ```bash
    response = socket.recv_json()
    print(response)  # Output: {'num1': <number>, 'page_num': <number>, 'num2': <number>}
    ```


- How to interpret the response:
    - num1: A random number between 1 and 933, inclusive.
    - page_num: A random number between 1 and 3, inclusive.
    - num2: A random number between 1 and 1000, inclusive. 
        - If page_num is 3, num2 will be between 1 and 384, inclusive.[^1] 


[^1]: Per partners API docs.

![UML](https://github.com/hiimdonald/moose/assets/4016508/a9515286-48ca-401e-9695-c8c351919d82)
