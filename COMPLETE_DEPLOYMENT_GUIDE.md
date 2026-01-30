# Complete Deployment Instructions to Fix Frontend-Backend Connection

## Overview
This guide will help you fix the connection issue between your Vercel frontend and Hugging Face backend.

## Current Status
- Frontend URL: https://hackathon-ii-todo-app-2-18am-k9i3mqetb.vercel.app/
- Backend URL: https://hamza1222-todo.hf.space/
- Issue: Frontend cannot connect to backend due to CORS misconfiguration and incorrect API URL

## Step-by-Step Solution

### Part 1: Update Backend Code (Completed)
The following changes have been made to your backend code:

1. Updated CORS configuration in `src/main.py` to include your Vercel frontend URL
2. Updated CORS_ORIGINS in `src/config.py` to include your Vercel frontend URL

### Part 2: Deploy Updated Backend to Hugging Face

1. Commit and push the updated code to your repository:
```bash
git add .
git commit -m "Fix CORS configuration for Vercel frontend connection"
git push origin main
```

2. Your Hugging Face Space should automatically rebuild. If not:
   - Go to your Hugging Face Space dashboard
   - Find your space: hamza1222-todo
   - Go to the "Files" tab
   - Click on the refresh/rebuild button

### Part 3: Configure Vercel Environment Variables

1. Go to https://vercel.com/
2. Navigate to your project: hackathon-ii-todo-app-2-18am-k9i3mqetb
3. Go to Settings → Environment Variables
4. Add/update the following variable:
   - Key: `NEXT_PUBLIC_API_URL`
   - Value: `https://hamza1222-todo.hf.space/api`
5. Save the changes
6. Redeploy your project after adding the environment variable

### Part 4: Verify the Connection

After completing both parts:

1. Wait for both deployments to complete
2. Visit your frontend: https://hackathon-ii-todo-app-2-18am-k9i3mqetb.vercel.app/
3. Open browser developer tools (F12)
4. Go to the Network tab
5. Try to perform an action that communicates with the backend (like registering, logging in, or viewing tasks)
6. Check that requests are being sent to https://hamza1222-todo.hf.space/api and receiving responses
7. Look for any remaining error messages in the Console tab

## Troubleshooting Specific "Unexpected token '<'" Error

This error occurs when the frontend receives HTML instead of JSON from the API. Here are specific steps to resolve it:

### 1. Verify API Endpoint Paths
Make sure your frontend is calling the correct API endpoints:
- Registration: `POST https://hamza1222-todo.hf.space/api/auth/register`
- Login: `POST https://hamza1222-todo.hf.space/api/auth/login`
- Get User: `GET https://hamza1222-todo.hf.space/api/auth/me`
- Get Tasks: `GET https://hamza1222-todo.hf.space/api/tasks`
- Create Task: `POST https://hamza1222-todo.hf.space/api/tasks`

### 2. Check Backend Health
Visit these URLs directly in your browser to verify they return JSON:
- `https://hamza1222-todo.hf.space/api/health`
- `https://hamza1222-todo.hf.space/docs` (should show Swagger UI)

### 3. Verify API Route Prefixes
The backend routes are structured as follows:
- Main prefix: `/api` (set in main.py)
- Auth routes: `/auth` (set in auth.py router)
- Tasks routes: `/tasks` (set in tasks.py router)
- Combined: `/api/auth/*` and `/api/tasks/*`

### 4. Frontend Request Headers
Ensure your frontend is sending the correct headers:
- Content-Type: `application/json`
- Authorization: `Bearer {token}` (for protected routes)

### 5. Check for Redirects
Sometimes the server redirects to a different URL. Check the Network tab in browser dev tools to see if there are any 301/302 redirects.

## Troubleshooting Tips

### If you still see CORS errors:
- Double-check that the URLs in your CORS configuration match exactly with your frontend domain
- Ensure there are no trailing slashes in URLs unless specified
- Clear your browser cache and try again

### If API calls are still failing:
- Verify that the `NEXT_PUBLIC_API_URL` environment variable is correctly set in Vercel
- Check that your backend is accessible by visiting: https://hamza1222-todo.hf.space/api/health

### Testing Locally with Deployed Backend:
If you want to test locally with the deployed backend:
1. Create a `.env.local` file in your frontend directory
2. Add: `NEXT_PUBLIC_API_URL=https://hamza1222-todo.hf.space/api`
3. Run `npm run dev` and test the connection

## Expected Result
Once properly configured, your frontend should be able to communicate seamlessly with your backend, allowing users to register, login, and manage their todo tasks.