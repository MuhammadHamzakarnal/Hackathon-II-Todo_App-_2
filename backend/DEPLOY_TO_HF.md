# Deploying Your Backend to Hugging Face Spaces

Follow these steps to deploy your FastAPI backend to Hugging Face Spaces:

## Prerequisites

1. A Hugging Face account (sign up at [huggingface.co](https://huggingface.co))
2. Your GitHub repository with the backend code (already done!)

## Steps to Deploy

### 1. Create a New Space

1. Go to [huggingface.co/spaces](https://huggingface.co/spaces)
2. Click "Create new Space"
3. Fill in the details:
   - Name: Choose a unique name for your space
   - License: MIT (or your preference)
   - SDK: Docker
   - Hardware: Choose based on your needs (CPU is fine for a backend API)
   - Visibility: Public or Private

### 2. Configure the Space

#### Option A: Using Git Clone
1. Clone your space repository:
   ```bash
   git clone https://huggingface.co/spaces/[your-username]/[your-space-name]
   ```

2. Copy all files from your backend repository to the space directory:
   ```bash
   cp -r /path/to/your/backend/* /path/to/hf/space/
   ```

3. Use the Dockerfile_hf as your Dockerfile:
   ```bash
   cp Dockerfile_hf Dockerfile
   ```

4. Commit and push:
   ```bash
   git add .
   git commit -m "Add backend application"
   git push
   ```

#### Option B: Direct Import from GitHub
1. In your Space settings, you can link directly to your GitHub repository
2. This will automatically sync your GitHub code to the Hugging Face Space

### 3. Set Up Secrets

In your Hugging Face Space settings, navigate to the "Secrets" tab and add:

- `DATABASE_URL`: Your PostgreSQL database connection string
- `BETTER_AUTH_SECRET`: Secret key for JWT token signing
- `JWT_ALGORITHM`: Algorithm for JWT encoding (optional, defaults to HS256)
- `JWT_EXPIRY_DAYS`: Number of days for JWT expiry (optional, defaults to 7)
- `DEBUG`: Debug mode (optional, defaults to false)
- `CORS_ORIGINS`: Comma-separated list of allowed origins (optional)

### 4. Wait for Deployment

After pushing your code, Hugging Face will automatically build and deploy your application. This may take a few minutes.

## Important Notes

1. The application will be available at: `https://[your-username]-[your-space-name].hf.space`

2. Your API endpoints will be accessible at:
   - `https://[your-username]-[your-space-name].hf.space/api/auth/register`
   - `https://[your-username]-[your-space-name].hf.space/api/auth/login`
   - `https://[your-username]-[your-space-name].hf.space/api/tasks/`
   - etc.

3. The Dockerfile_hf is optimized for Hugging Face Spaces and handles port configuration automatically.

4. Make sure your database connection string in secrets is accessible from the Hugging Face infrastructure.

## Troubleshooting

- If the build fails, check the build logs in the Space settings
- Ensure all required environment variables are set as secrets
- Verify that your database is accessible from external sources
- Check that your CORS settings allow requests from your frontend domain

## Updating Your Space

To update your deployed space:
1. Make changes to your GitHub repository
2. Push the changes
3. The Space will automatically rebuild with the new code