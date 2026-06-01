import os
import requests
import time
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Lipa Haraka API Configuration
API_URL = 'https://lipaharakaapis.co.ke/api.php?action=api_stk'
API_KEY = os.getenv('LIPAHARAKA_API_KEY')
CHANNEL_ID = os.getenv('LIPAHARAKA_CHANNEL_ID', '16')

def send_stk_push(phone, amount, account_ref="BulkPayment"):
    """Send STK Push via Lipa Haraka API"""
    try:
        # Clean phone number
        phone = str(phone).replace('+', '').replace(' ', '').replace('-', '')
        if phone.startswith('0'):
            phone = '254' + phone[1:]
        elif not phone.startswith('254'):
            phone = '254' + phone

        data = {
            'api_key': API_KEY,
            'phone': phone,
            'amount': str(amount),
            'channel_id': CHANNEL_ID
        }

        response = requests.post(API_URL, data=data, timeout=30)
        result = response.json()

        return {
            "phone": phone,
            "status": "success" if result.get('success') or result.get('status') == 'success' else "failed",
            "response": result
        }

    except Exception as e:
        return {
            "phone": phone,
            "status": "failed",
            "error": str(e)
        }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/push', methods=['POST'])
def bulk_push():
    """Handle bulk STK push requests"""
    data = request.get_json()

    phone_numbers = data.get('phone_numbers', [])
    amount = data.get('amount', 1)
    delay = data.get('delay', 2)

    if not phone_numbers:
        return jsonify({"error": "No phone numbers provided"}), 400

    if not API_KEY:
        return jsonify({"error": "API key not configured"}), 500

    results = []

    for i, phone in enumerate(phone_numbers):
        result = send_stk_push(phone, amount)
        results.append(result)

        if i < len(phone_numbers) - 1 and delay > 0:
            time.sleep(delay)

    successful = sum(1 for r in results if r['status'] == 'success')
    failed = sum(1 for r in results if r['status'] == 'failed')

    return jsonify({
        "total": len(phone_numbers),
        "successful": successful,
        "failed": failed,
        "results": results
    })

@app.route('/api/test', methods=['POST'])
def test_single():
    """Test with a single number"""
    data = request.get_json()
    phone = data.get('phone')
    amount = data.get('amount', 1)

    if not phone:
        return jsonify({"error": "Phone number required"}), 400

    result = send_stk_push(phone, amount)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
