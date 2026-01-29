# Deployment Instructions for Updated Backend

## To update your Hugging Face Space with the new CORS configuration:

1. Commit and push the changes to your backend repository:
```bash
cd C:\Users\VC\Desktop\agents_and_Skills\backend
git add .
git commit -m "Update CORS configuration to include vercel frontend URL"
git push origin main  # or whatever your main branch is named
```

2. The Hugging Face Space should automatically rebuild with the new configuration.

## If automatic rebuild doesn't happen:

1. Go to your Hugging Face Space dashboard
2. Find your space: hamza1222-todo
3. Go to the "Files" tab
4. Click on the refresh/rebuild button if available

## For the frontend, you need to update the environment variable on Vercel:

1. Go to https://vercel.com/
2. Navigate to your project: hackathon-ii-todo-app-2-18am-k9i3mqetb
3. Go to Settings → Environment Variables
4. Add/update the variable:
   - Key: NEXT_PUBLIC_API_URL
   - Value: https://hamza1222-todo.hf.space/api
5. Redeploy your project after adding the environment variable

## Testing the Connection

After making both updates:

1. Visit your frontend: https://hackathon-ii-todo-app-2-18am-k9i3mqetb.vercel.app/
2. Open browser developer tools (F12)
3. Go to the Network tab
4. Try to perform an action that communicates with the backend (like logging in or viewing tasks)
5. Check that requests are being sent to https://hamza1222-todo.hf.space/api and receiving responses