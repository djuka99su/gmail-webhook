from src.auth.authenticator import GmailAuthenticator
from src.services.gmail_service import GmailService
from config.config import CREDENTIALS_DIR, PUBSUB_TOPIC
from src.app import app

def setup_gmail_watch():
    try:
        # Authenticate
        credentials = GmailAuthenticator.authenticate(CREDENTIALS_DIR)
        
        # Initialize Gmail service
        gmail_service = GmailService()
        
        # Get labels
        # labels = gmail_service.list_labels(credentials)
        # gmail_service.print_labels(labels)
        
        # Setup watch
        gmail_service.setup_watch(credentials, PUBSUB_TOPIC)
        
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == '__main__':
    # Setup Gmail watch
    setup_gmail_watch()
    
    # Start the Flask server
    app.run(port=5000, debug=True) 