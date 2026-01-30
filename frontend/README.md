# Todoo - Frontend

A modern todo application built with Next.js.

## Deployment to Hugging Face Spaces

This frontend is configured to be deployed on Hugging Face Spaces using Docker.

### Setup

1. Create a new Space on Hugging Face: https://huggingface.co/spaces/new
2. Choose "Docker" as the SDK
3. Name your space (e.g., `hamza1222-todoo-frontend`)
4. Select "Advanced" and set the port to `3000`

### Environment Variables

Add the following environment variable in your Hugging Face Space settings:

- `NEXT_PUBLIC_API_URL`: URL of your backend API (e.g., `https://hamza1222-todo.hf.space`)

### Deploy

1. Push this code to a GitHub repository
2. In your Hugging Face Space settings, connect to your GitHub repository
3. The Docker build will automatically start

### Development

```bash
npm install
npm run dev
```

### Build

```bash
npm run build
```

## Features

- Modern, responsive UI
- JWT authentication
- Task CRUD operations
- Real-time updates
