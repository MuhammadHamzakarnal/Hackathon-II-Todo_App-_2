# Fix Connection Issue Between Frontend and Backend

## Problem
The frontend deployed at `https://hackathon-ii-todo-app-2-18am-k9i3mqetb.vercel.app/` is showing "Failed to load resource: net::ERR_CONNECTION_REFUSED" when trying to connect to the backend at `https://hamza1222-todo.hf.space`.

## Root Causes
1. The frontend is configured to connect to `http://localhost:8000/api` by default instead of your deployed backend
2. CORS configuration needs to properly allow requests from your frontend domain

## Solution Steps

### Step 1: Update Frontend Environment Variables (Required)
Go to your Vercel dashboard and set the environment variable:
- Key: `NEXT_PUBLIC_API_URL`
- Value: `https://hamza1222-todo.hf.space/api`

### Step 2: Redeploy Backend (Recommended)
After making the code changes below, redeploy your backend to Hugging Face Spaces to ensure CORS settings are applied correctly.

### Step 3: Updated Backend CORS Configuration
The backend CORS configuration has been updated in `src/main.py` to include your frontend URL without the trailing slash:

```python
# CORS Middleware
origins = [
    "https://hackathon-ii-todo-app-2-18am-k9i3mqetb.vercel.app",  # Vercel frontend URL
    "http://localhost:3000",                                       # For local development
    "http://localhost:8000",                                       # For local backend testing
]
```

### Step 4: Update Backend Config File
The CORS_ORIGINS setting in `src/config.py` has been updated to include your frontend URL:

```python
CORS_ORIGINS: str = "http://localhost:3000,https://frontend-gcohfcq16-haroon-khans-projects-5c7a0028.vercel.app,https://itxharoon-todo.hf.space,https://hackathon-ii-todo-app-2-18am-k9i3mqetb.vercel.app"
```

## Verification Steps
1. After updating the Vercel environment variable, redeploy your frontend
2. Test the connection by navigating to your frontend and trying to perform an API operation
3. Check browser developer tools Network tab to confirm API calls are reaching the backend

## Alternative Testing Method
If you want to test locally with the deployed backend:
1. Set `NEXT_PUBLIC_API_URL=https://hamza1222-todo.hf.space/api` in your local `.env.local` file
2. Run `npm run dev` and test the connection