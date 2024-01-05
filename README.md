# My Stripe Shop Django Project

## How to run with Docker

1. Install Docker: [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)

2. Open a terminal in the project directory.

3. Build the Docker image:
   ```bash
   docker build -t stripe_shop_django .

4. Start project:
    ```bash
    docker run -p 8000:8000 stripe_shop_django

5. Open your browser and visit http://localhost:8000 to see the application.