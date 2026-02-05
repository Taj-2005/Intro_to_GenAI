# Quick Start Guide

Get the system running in 5 minutes!

## Prerequisites Check

```bash
python3 --version  # Should be 3.8+
node --version      # Should be 18+
```

## 1. Train Model (2 minutes)

```bash
cd ml_model
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python train.py
```

## 2. Start Backend (1 minute)

```bash
cd ../backend
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload
```

**Test:** Open http://localhost:8000/health

## 3. Start Frontend (1 minute)

```bash
cd ../frontend
npm install
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
npm run dev
```

**Test:** Open http://localhost:3000

## 4. Install Extension (1 minute)

1. Chrome → `chrome://extensions/`
2. Enable "Developer mode"
3. "Load unpacked" → Select `chrome_extension` folder
4. (Optional) Run `python create_icons.py` in chrome_extension/ for icons

## 5. Test It!

1. Go to a job posting on LinkedIn/Indeed
2. Click extension icon
3. Click "Analyze Job Posting"
4. See results!

OR

1. Go to http://localhost:3000
2. Paste a job description
3. Click "Analyze"

## Troubleshooting

**Model not loading?**
- Check `ml_model/models/` has .pkl files
- Re-run `python train.py`

**Backend errors?**
- Check MongoDB is running/accessible
- Verify model files exist

**Extension not working?**
- Check backend is running at http://localhost:8000
- Open browser console (F12) for errors

## Next Steps

- Read [SETUP.md](SETUP.md) for detailed setup
- Read [docs/deployment.md](docs/deployment.md) for production
- Read [docs/user_manual.md](docs/user_manual.md) for usage
