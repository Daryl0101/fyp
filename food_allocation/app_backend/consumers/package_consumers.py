import json
from channels.generic.websocket import WebsocketConsumer, async_to_sync


class PackageConsumer(WebsocketConsumer):
    def connect(self):
        async_to_sync(self.channel_layer.group_add)("package", self.channel_name)
        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)("package", self.channel_name)

    def package_state_update(self, event):
        self.send(text_data=json.dumps(event.get("message")))
