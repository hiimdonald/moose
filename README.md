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

## Requirements

[python3.11](https://www.python.org/downloads/)


### Installation

1. **Clone the repository**

   ```
   git clone https://github.com/hiimdonald/moose.git
   cd moose
   ```

2. **Create and Activate Virtual Environment** *(Optional, but recommended)*
    [flask installation guide](https://flask.palletsprojects.com/en/3.0.x/installation/)

    ```
    For macOS/Linux:
        1. python3 -m venv .venv
        2. . .venv/bin/activate
    ```

3. **Install required packages**

    ```
    pip install -r requirements.txt
    ```

4. **Create .env file in main directory**

    ```
    # Replace SECRET_KEY, MAIL_USERNAME, MAIL_PASSWORD, and ADMINS

    SECRET_KEY="YOURSECRETKEY"

    MAIL_SERVER="smtp.gmail.com"
    MAIL_PORT=465
    MAIL_USE_TLS="False"
    MAIL_USE_SSL="True"
    MAIL_USERNAME="<your-gmail-email>"
    MAIL_PASSWORD="<your-google-app-password>"

    ADMINS="<your-gmail-email>"
    ```


5. **Create config.py file in main directory**

    ```
    # Example config.py

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
        MAIL_PORT = os.environ.get("MAIL_PORT")
        MAIL_USE_SSL = os.environ.get("MAIL_USE_SSL")
        MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
        MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
        ADMINS = os.environ.get("ADMINS")
    ```

6. **Create and Migrate Database**
In the command terminal
    ```
    1. (venv) $ flask db init
    2. (venv) $ flask db migrate -m "users and gameplay tables"
    3. (venv) $ flask db upgrade
    ```

7. **Create .flaskenv file in mail directory** (optional)

    ```
    FLASK_APP=mathy.py
    FLASK_DEBUG=0
    FLASK_RUN_PORT=8000
    ```

8. **Run the app to start playing**
    ```
    (venv) $ flask run
    ```