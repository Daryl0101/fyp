import json
from channels.generic.websocket import WebsocketConsumer, async_to_sync


class AllocationConsumer(WebsocketConsumer):
    def connect(self):
        async_to_sync(self.channel_layer.group_add)("allocation", self.channel_name)
        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)("allocation", self.channel_name)

    def allocation_process(self, event):
        self.send(text_data=json.dumps(event))

    def accept_reject_allocation_family(self, event):
        self.send(text_data=json.dumps(event))
