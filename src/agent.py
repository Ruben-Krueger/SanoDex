class Agent:
    def __init__(self, name="Nova"):
        self.context = []
        self.name = name
        

    def run(self):
        pass

    def handle_message(self, message):
        self.context.append(message)
        return "Hello, how can I help you today?"



