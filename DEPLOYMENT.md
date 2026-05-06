# Deployment Guide

This guide explains how to deploy the Crop Management System easily using Docker or cloud platforms.

## Option 1: Deployment via Docker Compose (Recommended)

This is the easiest way to run the entire project locally or on a VPS (like AWS EC2, DigitalOcean, etc.).

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) installed.
- [Docker Compose](https://docs.docker.com/compose/install/) installed.

### Steps
1.  **Clone the repository** (if you haven't already).
2.  **Open a terminal** in the root directory.
3.  **Build and run the project**:
    ```bash
    docker-compose up --build -d
    ```
4.  **Access the application**:
    - Frontend: [http://localhost:3000](http://localhost:3000)
    - Backend API: [http://localhost:8001](http://localhost:8001)

### Customizing the API URL
If you are deploying to a server with a domain name, update the `VITE_API_URL` in `docker-compose.yml`:
```yaml
frontend:
  build:
    context: ./frontend
    args:
      - VITE_API_URL=https://api.yourdomain.com
```

---

## Option 2: Cloud Deployment (Render / Vercel)

If you want to host the project online for free or at low cost, follow these steps:

### Backend (on [Render.com](https://render.com))
1.  Connect your GitHub repository.
2.  Create a new **Web Service**.
3.  Set the Root Directory to `backend`.
4.  Runtime: `Docker`.
5.  Render will automatically use the `backend/Dockerfile`.

### Frontend (on [Vercel](https://vercel.com) or [Netlify](https://netlify.com))
1.  Connect your GitHub repository.
2.  Set the Root Directory to `frontend`.
3.  Framework Preset: `Vite`.
4.  **Important**: Add an Environment Variable:
    - Name: `VITE_API_URL`
    - Value: `https://your-backend-url.onrender.com` (Your Render service URL).
5.  Deploy.

---

## Database Persistence
The Docker setup uses a volume to map `backend/crop.db` to the container. This ensures that your data is saved even if the container is deleted or updated.

If you are using Render, make sure to add a **Disk** to your service and mount it at `/app/crop.db` to keep your data.
