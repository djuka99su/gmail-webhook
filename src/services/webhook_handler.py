import base64
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from libs.utils import get_schedules

class WebhookHandler:
    @staticmethod
    def process_schedules(msg):
        """Extract email details from the message"""
        headers = msg.get('payload', {}).get('headers', [])
        
        # Get subject and sender from headers
        subject = next((h['value'] for h in headers if h['name'].lower() == 'subject'), 'No Subject')
        sender = next((h['value'] for h in headers if h['name'].lower() == 'from'), 'No Sender')
        
        # Get body
        payload = msg.get('payload', {})
        body = ''

        def get_body_from_parts(parts):
            for part in parts:
                if part['mimeType'] == 'text/plain':
                    return base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                elif part['mimeType'] == 'text/html':
                    return base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                elif 'parts' in part:
                    # Recursively check nested parts
                    result = get_body_from_parts(part['parts'])
                    if result:
                        return result
            return ''

        if 'parts' in payload:
            # Multipart message
            body = get_body_from_parts(payload['parts'])
        elif 'body' in payload and 'data' in payload['body']:
            # Single part message
            body = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')
        
        schedule = [] 
    
        if "Schedule" in body:
            schedule = get_schedules(body)
            
        print(schedule)
        
        return schedule


    @staticmethod
    def process_gmail_update(request_json, credentials):
        """
        Process Gmail push notification
        """
        try:
            if request_json is None:
                return {"status": "error", "message": "No request data received"}

            # Initialize Gmail service
            service = build('gmail', 'v1', credentials=credentials)
            
            try:
                # Get the most recent message
                messages = service.users().messages().list(
                    userId='me',
                    maxResults=1,
                    labelIds=['Label_8361647661331376318']
                ).execute()
                
                if 'messages' in messages:
                    msg = service.users().messages().get(
                        userId='me',
                        id=messages['messages'][0]['id'],
                        format='full'
                    ).execute()
                    
                    return msg
                 
                
                return {"status": "error", "message": "No messages found"}
                    
            except HttpError as error:
                if error.resp.status == 404:
                    print("Message no longer exists or is inaccessible")
                    return {"status": "warning", "message": "Message no longer available"}
                raise
            
        except Exception as e:
            print(f"Error processing Gmail update: {str(e)}")
            raise