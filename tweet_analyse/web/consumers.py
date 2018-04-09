import json

from channels.generic.websocket import WebsocketConsumer

from web.tasks import generate_report


class AnalyseConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        data = json.loads(text_data)
        if data['action'] == "generate":
            query = data['q']
            self.send(text_data=json.dumps({
                'message': "generating"
            }))
            generate_report.delay(query, self.channel_name)

    def update_client(self, event):
        data = event['data']
        # Send message to WebSocket
        self.send(text_data=json.dumps(data))
