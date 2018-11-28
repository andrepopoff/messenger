import json


class MessageHandler:
    @staticmethod
    def get_message(client_sock):
        """
        Receives a message from a client
        """
        byte_message = client_sock.recv(1024)

        if isinstance(byte_message, bytes):
            json_message = byte_message.decode('utf-8')
            message = json.loads(json_message)  # from json to dict
            if isinstance(message, dict):
                return message
            else:
                raise TypeError
        else:
            raise TypeError

    @staticmethod
    def prepare_response(client_message):
        """
        Generates a response to the client
        """
        if 'action' in client_message and client_message['action'] == 'presence' \
                and 'time' in client_message and isinstance(client_message['time'], float):
            return {'response': 200}
        return {'response': 400, 'error': 'Invalid request'}

    @staticmethod
    def send_message(client_sock, response):
        """
        Sends a response to the client
        """
        if isinstance(response, dict):
            json_message = json.dumps(response)
            byte_message = json_message.encode('utf-8')
            client_sock.send(byte_message)
        else:
            raise TypeError

    def read_requests(self, clients_for_reading, all_clients):
        """
        Reading messages that clients send
        """
        messages = []
        for sock in clients_for_reading:
            try:
                message = self.get_message(sock)
                print(message)
                messages.append(message)
            except:
                print('Client {} {} has disconnected'.format(sock.fileno(), sock.getpeername()))
                all_clients.remove(sock)

        return messages

    def write_responses(self, messages, clients_for_writing, all_clients):
        """
        Sending messages to clients who are waiting for them
        """
        for sock in clients_for_writing:
            # We will send every message to everyone
            for message in messages:
                try:
                    self.send_message(sock, message)
                except:
                    print('Client {} {} has disconnected'.format(sock.fileno(), sock.getpeername()))
                    sock.close()
                    all_clients.remove(sock)