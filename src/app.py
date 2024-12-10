from flask import Flask, request, jsonify
from src.services.gmail_service import GmailService
from src.auth.authenticator import GmailAuthenticator
from src.services.webhook_handler import WebhookHandler
from config.config import CREDENTIALS_DIR

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/webhook', methods=['POST'])
def gmail_webhook():
    try:
        # Get credentials
        credentials = GmailAuthenticator.authenticate(CREDENTIALS_DIR)
        
        # Process the webhook
        webhook_handler = WebhookHandler()
        processed_message = webhook_handler.process_gmail_update(request.json, credentials)
        processed_schedules = webhook_handler.process_schedules(processed_message)
        if not processed_schedules:
            print("No schedules found")
            return jsonify({"status": "success", "message": "No schedules found"}), 200
        
        gmail_service = GmailService()
        gmail_service.create_calendar_events(credentials, processed_schedules)
        
        return jsonify({"status": "success", "message": "Update processed"})
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

