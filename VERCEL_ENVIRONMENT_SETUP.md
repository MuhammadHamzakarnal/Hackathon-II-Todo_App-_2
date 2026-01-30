# Vercel Environment Setup for Todo App

## Required Environment Variables

To connect your Vercel frontend to the Hugging Face backend, you need to set the following environment variable in your Vercel project:

### NEXT_PUBLIC_API_URL
- **Key**: `NEXT_PUBLIC_API_URL`
- **Value**: `https://hamza1222-todo.hf.space/api`

## How to Set Environment Variables on Vercel

1. Go to https://vercel.com/
2. Sign in to your account
3. Navigate to your project: `hackathon-ii-todo-app-2-18am-k9i3mqetb`
4. Go to Settings → Environment Variables
5. Add the following variable:
   - Key: `NEXT_PUBLIC_API_URL`
   - Value: `https://hamza1222-todo.hf.space/api`
6. Save the changes
7. Redeploy your project for the changes to take effect

## Verification

After setting the environment variable:

1. Visit your frontend: https://hackathon-ii-todo-app-2-18am-k9i3mqetb.vercel.app/
2. Open browser developer tools (F12)
3. Go to the Network tab
4. Try to perform an action that communicates with the backend
5. Verify that requests are being sent to https://hamza1222-todo.hf.space/api