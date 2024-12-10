from googleapiclient.discovery import build
from datetime import datetime
from config.config import CALENDAR_ID

class GmailService:
    @staticmethod
    def list_labels(credentials):
        service = build('gmail', 'v1', credentials=credentials)
        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])

        if not labels:
            print('No labels found.')
            return []
        
        return labels

    @staticmethod
    def print_labels(labels):
        if not labels:
            return
        
        print('Labels:')
        for label in labels:
            print(f"{label['name']} - {label['id']}")
            
    @staticmethod
    def setup_watch(credentials, topic_name: str):
        """
        Sets up Gmail API push notifications to a Cloud Pub/Sub topic
        """
        try:
            service = build('gmail', 'v1', credentials=credentials)
            request = {
                'labelIds': ['Label_8361647661331376318'],
                'topicName': topic_name,
                'labelFilterAction': 'include'
            }
            response = service.users().watch(userId='me', body=request).execute()
            print(f"Watch setup successfully. Response: {response}")
            return response
        except Exception as e:
            print(f"An error occurred setting up watch: {str(e)}")
            raise
        
    @staticmethod
    def create_calendar_events(credentials, events_data: list[dict]):
        """
        Creates calendar events from a list of event dictionaries.
        
        Args:
            credentials: Google OAuth2 credentials
            events_data: List of dictionaries containing event information
                        Each dict should have: 
                        - day: str
                        - month: str
                        - year: str
                        - start_time: str
                        - end_time: str
                        
        """
        try:
            service = build('calendar', 'v3', credentials=credentials)
            
            for event_data in events_data:
                # Create datetime strings in RFC3339 format
                date_str = f"{event_data['year']}-{event_data['month']}-{event_data['day']}"
                start_datetime = f"{date_str}T{event_data['start_time']}:00"
                end_datetime = f"{date_str}T{event_data['end_time']}:00"

                event = {
                    'summary': 'PacuraMED',
                    'location': "Ullernchausseen 111, 0284 Oslo, Norge",
                    'start': {
                        'dateTime': start_datetime,
                        'timeZone': 'Europe/Oslo',
                    },
                    'end': {
                        'dateTime': end_datetime,
                        'timeZone': 'Europe/Oslo',
                    },
                }

                try:
                    event_result = service.events().insert(
                        calendarId=CALENDAR_ID,
                        body=event
                    ).execute()
                    print(f"Event created: {event_result.get('htmlLink')}")
                except Exception as e:
                    print(f"Failed to create event for {date_str}: {str(e)}")
                    continue

        except Exception as e:
            print(f"An error occurred while creating calendar events: {str(e)}")
            raise
        