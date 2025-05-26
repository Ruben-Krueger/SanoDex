class Agent:

    def __init__(self, name="Nova"):
        self.context = ["<system>This is the start of the conversation.</system>"]
        self.name = name

    def prompt(self):
        return f"""
        - You are a helpful healthcare phone agent named {self.name}.
        - You are talking to a patient on the phone who is likely calling to schedule an appointment.
        - You can help them schedule an appointment or answer questions about the practice.
        - Do not reveal protected health information (PHI) without verifying the patient's identity.
        - You are using the following context to help the patient:
        {self.context}
        """

    def get_appoinment_times(self):
        # Mock data with dates and times for the upcoming week
        appointment_times = [
            "Monday, April 22nd - 10:00 AM",
            "Tuesday, April 23rd - 11:00 AM",
            "Wednesday, April 24th - 1:00 PM",
            "Thursday, April 25th - 10:30 AM",
            "Friday, April 26th - 11:30 AM",
            "Friday, April 26th - 4:00 PM",
        ]  
        return appointment_times
    

    def get_response(self):
        return "Hello, how can I help you today?"

    def handle_message(self, message):
        # Add user message with token
        self.context.append(f"<user>{message}</user>")
        
        # Generate and store assistant response
        response = self.get_response()
        self.context.append(f"<assistant>{response}</assistant>")
        
        return response



