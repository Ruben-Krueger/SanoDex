from azure.communication.callautomation import CallAutomationClient

class ACSClient:
    def __init__(self, connection_string):
        self.client = CallAutomationClient.from_connection_string(connection_string)

    def handle_incoming_call(self, call_data):
        call_connection = self.client.create_call_connection(call_data)
        return call_connection.call_connection_id