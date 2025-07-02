# 🎬 Videoflix Backend

Welcome to the **Videoflix Backend** — a modern video platform powered by Django. This setup includes a full Docker configuration, environment variable management, and is ready for local development or production scaling.

---

## 🚀 Quick Start (with Docker)

1. **Clone the repository**

   ```bash
   git clone https://github.com/MarcelZalec/Videoflix_Backend_Docker.git
   cd Videoflix_Backend_Docker


2. **Create .env file from .env_template**
    ```bash
    cp .env_template .env
    ```

    Before proceeding, make sure to [set up your `.env` file](#setup) by following the instructions below.


3. **Start the Docker Container**<br>
    ```bash
    docker-compose up --build
    ```
    This setup:<br><br>
    Automatically creates a .env file from .env_template (if not already present)<br>
    Runs migrations<br>
    Launches the server at http://localhost:8000/<br>

<a name="setup"></a>
## **Set up `.env` file**
   Define the required environment variables in your `.env` file to enable registration and password reset email functionality:

   ```env
   # URL where users are redirected after registration or password reset
   REDIRECT_LANDING='http://deine.FrontendURL.com/'

   # Backend base URL used in email links
   BACKEND_URL='http://deine.BackenURL.com/'