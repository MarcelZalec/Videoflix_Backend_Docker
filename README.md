# 🎬 Videoflix Backend

Welcome to the **Videoflix Backend** — a modern video platform powered by Django. This setup includes a full Docker configuration, environment variable management, and is ready for local development or production scaling.

---

## 🚀 Quick Start (with Docker)

1. **Clone the repository**

   ```bash
   git clone https://github.com/MarcelZalec/Videoflix_Backend.git
   cd Videoflix_Backend


2. **Start the Docker Container**
    <code>docker-compose up --build</code>
    This setup:

    Automatically creates a .env file from .env_template (if not already present)
    Runs migrations
    Launches the server at http://localhost:8000/

## **Set up `.env` file**
   Define the required environment variables in your `.env` file to enable registration and password reset email functionality:

   ```env
   # URL where users are redirected after registration or password reset
   REDIRECT_LANDING='http://deine.FrontendURL.com/'

   # Backend base URL used in email links
   BACKEND_URL='http://deine.BackenURL.com/'