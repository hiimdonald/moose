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
    - Initialize and migrate the database with the following commands:
        ```bash
        flask db init
        flask db migrate -m "users and gameplay tables"
        flask db upgrade
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


### Running the Application

- Start the application with:
    ```bash
    flask run
    ```
- Access the game at `http://127.0.0.1:8000/` in your web browser.


## Security

Ensure your `.env` file containing sensitive information like email credentials and secret keys is secure and never commit it to a public repository.

## Support

For support, please open an issue in the [GitHub issues page](https://github.com/hiimdonald/moose/issues).
