# API Troubleshooting Guide: "Unexpected token '<'" Error

## Understanding the Error

The error "Unexpected token '<', '<!DOCTYPE "... is not valid JSON" occurs when your JavaScript frontend expects a JSON response from an API endpoint, but instead receives HTML content (usually an error page or redirect response).

## Common Causes

1. **Incorrect API endpoint path** - The URL doesn't exist on the backend
2. **Server redirect** - The server redirects to an HTML page (like an error page)
3. **Backend error** - The backend encounters an error and returns an HTML error page
4. **Missing API prefix** - The API prefix is not properly configured

## Step-by-Step Troubleshooting

### Step 1: Verify Backend API Endpoints

Test your backend endpoints directly in the browser or using curl:

```bash
# Health check
curl -X GET https://hamza1222-todo.hf.space/api/health

# API documentation
curl -X GET https://hamza1222-todo.hf.space/docs
```

Expected response for `/api/health` should be:
```json
{"status": "healthy"}
```

### Step 2: Check Available Endpoints

Your backend should expose these endpoints:
- `GET /api/health` - Health check
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user (requires auth)
- `GET /api/tasks` - Get user tasks (requires auth)
- `POST /api/tasks` - Create new task (requires auth)
- `PUT /api/tasks/{id}` - Update task (requires auth)
- `DELETE /api/tasks/{id}` - Delete task (requires auth)

### Step 3: Browser Network Tab Analysis

1. Open browser DevTools (F12)
2. Go to the Network tab
3. Perform the action that triggers the error
4. Look for the failed request
5. Check:
   - The exact URL being called
   - The response status code
   - The response content (click on the request → Response tab)
   - Request headers
   - Response headers

### Step 4: Frontend Configuration Check

Verify your frontend is configured with the correct API URL:

In your frontend code, check for:
```javascript
// Should be set to your backend URL
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://hamza1222-todo.hf.space/api';
```

### Step 5: Environment Variable Verification

On Vercel, ensure the environment variable is correctly set:
- Key: `NEXT_PUBLIC_API_URL`
- Value: `https://hamza1222-todo.hf.space/api`

Note: The `/api` suffix is important as your backend routes are prefixed with `/api`.

## Debugging Checklist

- [ ] Backend is deployed and running
- [ ] CORS configuration includes your frontend domain
- [ ] Frontend environment variable points to correct backend URL
- [ ] API endpoints exist and return JSON (not HTML)
- [ ] Authentication tokens are properly included in requests (for protected routes)
- [ ] No typos in API endpoint paths

## Testing Your Backend

Before testing with the frontend, verify your backend works independently:

1. Visit `https://hamza1222-todo.hf.space/docs` to see the API documentation
2. Visit `https://hamza1222-todo.hf.space/api/health` to check if the health endpoint works
3. Use the Swagger UI to test your API endpoints directly

## Common Fixes

### Fix 1: Correct API URL Format
Make sure your frontend uses the complete API path:
- ✅ Correct: `https://hamza1222-todo.hf.space/api/auth/login`
- ❌ Incorrect: `https://hamza1222-todo.hf.space/auth/login`

### Fix 2: Check for Trailing Slashes
Some APIs are sensitive to trailing slashes:
- Be consistent with or without trailing slashes
- Check your backend configuration

### Fix 3: Verify Authentication Headers
For protected routes, ensure your frontend sends the authorization header:
```javascript
headers: {
  'Content-Type': 'application/json',
  'Authorization': `Bearer ${accessToken}`
}
```

## Additional Resources

If the issue persists:
1. Check the Hugging Face Space logs for any backend errors
2. Verify that your requirements.txt includes all necessary dependencies
3. Ensure your Dockerfile properly exposes the correct port (7860)
4. Confirm that your backend starts correctly and listens on 0.0.0.0:7860
5. Make sure your backend has a proper root endpoint that returns JSON