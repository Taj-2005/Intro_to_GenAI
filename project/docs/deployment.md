# Deployment Guide

This guide provides step-by-step instructions for deploying all components of the Fake Job Posting Detection System.

## Prerequisites

- Python 3.8+
- Node.js 18+
- MongoDB Atlas account (or local MongoDB)
- Git
- Cloud platform accounts (AWS/Render/Railway/DigitalOcean for backend, Vercel/Netlify for frontend)

## 1. Backend Deployment (FastAPI)

### Option A: Deploy to Render

1. **Create Render Account:**
   - Sign up at https://render.com
   - Create a new Web Service

2. **Prepare Repository:**
   ```bash
   cd backend
   # Ensure requirements.txt is up to date
   ```

3. **Configure Render:**
   - Connect your GitHub repository
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `uvicorn app:app --host 0.0.0.0 --port $PORT`
   - Add environment variables:
     - `MONGO_URI`: Your MongoDB connection string
     - `DATABASE_NAME`: `job_analysis_db`
     - `PYTHON_VERSION`: `3.11`

4. **Deploy:**
   - Click "Create Web Service"
   - Render will build and deploy automatically

### Option B: Deploy to AWS EC2

1. **Launch EC2 Instance:**
   ```bash
   # Choose Ubuntu 22.04 LTS
   # Instance type: t2.micro or larger
   # Configure security group: Allow HTTP (80), HTTPS (443), SSH (22)
   ```

2. **SSH into Instance:**
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-ip
   ```

3. **Install Dependencies:**
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv nginx -y
   ```

4. **Clone and Setup:**
   ```bash
   git clone your-repo-url
   cd project/backend
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

5. **Upload Model Files:**
   ```bash
   # From your local machine, upload trained models
   scp -r ml_model/models ubuntu@your-ec2-ip:~/project/backend/
   ```

6. **Create Systemd Service:**
   ```bash
   sudo nano /etc/systemd/system/job-detector.service
   ```
   
   Add:
   ```ini
   [Unit]
   Description=Fake Job Detector API
   After=network.target

   [Service]
   User=ubuntu
   WorkingDirectory=/home/ubuntu/project/backend
   Environment="PATH=/home/ubuntu/project/backend/venv/bin"
   ExecStart=/home/ubuntu/project/backend/venv/bin/uvicorn app:app --host 0.0.0.0 --port 8000
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

7. **Start Service:**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable job-detector
   sudo systemctl start job-detector
   ```

8. **Configure Nginx:**
   ```bash
   sudo nano /etc/nginx/sites-available/job-detector
   ```
   
   Add:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```
   
   ```bash
   sudo ln -s /etc/nginx/sites-available/job-detector /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

### Option C: Deploy to Railway

1. **Install Railway CLI:**
   ```bash
   npm i -g @railway/cli
   railway login
   ```

2. **Initialize Project:**
   ```bash
   cd backend
   railway init
   ```

3. **Set Environment Variables:**
   ```bash
   railway variables set MONGO_URI=your-mongodb-uri
   railway variables set DATABASE_NAME=job_analysis_db
   ```

4. **Deploy:**
   ```bash
   railway up
   ```

## 2. Database Deployment (MongoDB Atlas)

1. **Create MongoDB Atlas Account:**
   - Sign up at https://www.mongodb.com/cloud/atlas

2. **Create Cluster:**
   - Choose free tier (M0)
   - Select region closest to your backend
   - Create cluster

3. **Configure Database Access:**
   - Go to "Database Access"
   - Create database user
   - Set username and password

4. **Configure Network Access:**
   - Go to "Network Access"
   - Add IP address: `0.0.0.0/0` (for development)
   - For production, add specific IPs

5. **Get Connection String:**
   - Go to "Clusters" → "Connect"
   - Choose "Connect your application"
   - Copy connection string
   - Replace `<password>` with your database password

6. **Update Backend:**
   - Set `MONGO_URI` environment variable to connection string
   - Format: `mongodb+srv://username:password@cluster.mongodb.net/`

## 3. Frontend Deployment (Next.js)

### Deploy to Vercel

1. **Install Vercel CLI:**
   ```bash
   npm i -g vercel
   ```

2. **Login:**
   ```bash
   vercel login
   ```

3. **Deploy:**
   ```bash
   cd frontend
   vercel
   ```

4. **Set Environment Variables:**
   - Go to Vercel dashboard
   - Project → Settings → Environment Variables
   - Add: `NEXT_PUBLIC_API_URL` = your backend URL

5. **Redeploy:**
   ```bash
   vercel --prod
   ```

### Deploy to Netlify

1. **Install Netlify CLI:**
   ```bash
   npm i -g netlify-cli
   ```

2. **Login:**
   ```bash
   netlify login
   ```

3. **Build and Deploy:**
   ```bash
   cd frontend
   npm run build
   netlify deploy --prod
   ```

4. **Set Environment Variables:**
   - Netlify dashboard → Site settings → Environment variables
   - Add: `NEXT_PUBLIC_API_URL`

## 4. Chrome Extension Packaging

1. **Prepare Extension:**
   ```bash
   cd chrome_extension
   ```

2. **Update API URL:**
   - Edit `popup.js`
   - Change `API_BASE_URL` to your deployed backend URL

3. **Create Icons:**
   - Create icon files: `icon16.png`, `icon48.png`, `icon128.png`
   - Minimum sizes: 16x16, 48x48, 128x128 pixels

4. **Load in Chrome:**
   - Open Chrome → `chrome://extensions/`
   - Enable "Developer mode"
   - Click "Load unpacked"
   - Select `chrome_extension` folder

5. **Package for Distribution (Optional):**
   - Click "Pack extension"
   - Select `chrome_extension` folder
   - Creates `.crx` file for distribution

## 5. Environment Variables Summary

### Backend (.env)
```bash
MONGO_URI=mongodb+srv://user:pass@cluster.mongodb.net/
DATABASE_NAME=job_analysis_db
API_HOST=0.0.0.0
API_PORT=8000
```

### Frontend (.env.local)
```bash
NEXT_PUBLIC_API_URL=https://your-backend-url.com
```

### Chrome Extension (popup.js)
```javascript
const API_BASE_URL = 'https://your-backend-url.com';
```

## 6. Post-Deployment Checklist

- [ ] Backend is accessible and `/health` endpoint returns 200
- [ ] MongoDB connection is working
- [ ] Frontend can connect to backend
- [ ] Chrome extension can analyze jobs
- [ ] All environment variables are set
- [ ] CORS is configured correctly
- [ ] SSL/HTTPS is enabled (for production)
- [ ] Model files are uploaded to backend server
- [ ] Database collections are created automatically
- [ ] Error logging is configured

## 7. Monitoring and Maintenance

### Health Checks

Set up monitoring for:
- Backend API availability
- MongoDB connection
- Model inference time
- Error rates

### Logs

- Backend logs: Check application logs for errors
- MongoDB logs: Monitor database performance
- Frontend logs: Check browser console for errors

### Updates

1. **Update Model:**
   - Retrain model with new data
   - Upload new model files to server
   - Restart backend service

2. **Update Backend:**
   - Push code changes
   - Restart service (auto on Render/Railway)

3. **Update Frontend:**
   - Push code changes
   - Vercel/Netlify auto-deploys

## 8. Troubleshooting

### Backend Issues

**Problem:** Model not loading
- **Solution:** Ensure model files are in correct path: `ml_model/models/`

**Problem:** MongoDB connection failed
- **Solution:** Check connection string, network access, credentials

**Problem:** CORS errors
- **Solution:** Update `allow_origins` in `app.py` with frontend URL

### Frontend Issues

**Problem:** Cannot connect to backend
- **Solution:** Check `NEXT_PUBLIC_API_URL` environment variable

**Problem:** Build fails
- **Solution:** Ensure all dependencies are in `package.json`

### Extension Issues

**Problem:** Extension not extracting data
- **Solution:** Check if page matches content script patterns in `manifest.json`

**Problem:** API calls failing
- **Solution:** Update `API_BASE_URL` in `popup.js`

## 9. Production Considerations

1. **Security:**
   - Use HTTPS for all connections
   - Restrict CORS to specific origins
   - Use environment variables for secrets
   - Enable MongoDB authentication

2. **Performance:**
   - Enable caching where appropriate
   - Use CDN for frontend assets
   - Optimize model inference time
   - Database indexing

3. **Scalability:**
   - Use load balancers for multiple backend instances
   - MongoDB Atlas auto-scaling
   - Consider Redis for caching

4. **Backup:**
   - Regular MongoDB backups
   - Version control for code
   - Model versioning
