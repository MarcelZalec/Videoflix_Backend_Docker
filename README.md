# Videoflix
![Logo](Logo.svg)

## Overview  
**Videoflix** is a feature-rich Netflix clone designed with a modern web stack.

- **Frontend:** Built using [Angular 19](https://github.com/MarcelZalec/videoflix_frontend)  
- **Backend:** Developed with [Django REST Framework](https://github.com/MarcelZalec/Videoflix_Backend)

---

## Backend Setup

1. **Clone the repository**  
   ```bash
   git clone https://github.com/MarcelZalec/Videoflix_Backend.git
   cd Videoflix-Backend

2. **Create a virtual environment:**  
   ```bash
   python -m venv env
   source env/bin/activate       # Linux / macOS
   env\Scripts\activate          # Windows

3. **Install dependencies:**  
   ```bash
   pip install -r requirements.txt

4. **Make migrations**  
   ```bash
   python manage.py makemigrations
   python manage.py migrate

5. **Create a env file from .env_template**  
   ```bash
   cp .env_template .env

6. **Start Backend with**  
   ```bash
   python3 manage.py runserver

## **Set up `.env` file**
   Define the required environment variables in your `.env` file to enable registration and password reset email functionality:

   ```env
   # URL where users are redirected after registration or password reset
   REDIRECT_LANDING='http://deine.FrontendURL.com/'

   # Backend base URL used in email links
   BACKEND_URL='http://deine.BackenURL.com/'
