# Bulk STK Push Bot - Lipa Haraka API

A Flask web application for sending bulk M-Pesa STK Push notifications via the Lipa Haraka API.

## Features

- **Bulk Input**: Paste numbers one per line or comma-separated
- **Auto-formatting**: Converts `07...` and `+254...` to `254...` automatically
- **Rate Limiting**: Configurable delay between requests to avoid API throttling
- **Progress Tracking**: Real-time progress bar during bulk sending
- **Quick Test**: Test single number before bulk sending
- **Results Dashboard**: Success/failure stats with per-number details

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and fill in your API credentials:
   ```bash
   cp .env.example .env
   ```
4. Run the app:
   ```bash
   python app.py
   ```

## Deploy to Render

1. Push to GitHub
2. Connect repository on [Render](https://render.com)
3. Set environment variables in Render dashboard
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `gunicorn app:app`

## API Endpoints

- `GET /` - Web interface
- `POST /api/push` - Bulk STK push
- `POST /api/test` - Single number test

## Important Notes

- Subscribe to Lipa Haraka APIs at [lipaharakaapis.co.ke](https://lipaharakaapis.co.ke)
- Cost: KES 400/month with 2 free 24-hour trials
- Use rate limiting to avoid API throttling
