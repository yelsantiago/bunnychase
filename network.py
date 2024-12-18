import pickle
import socket
from ip_address import get_local_ip

class Network:
    def get_server_ip(self):
        ''' Retrieve the server IP address from a file or prompt the user '''
        try:
            with open("server_ip.txt", "r") as f:
                server_ip = f.read().strip()
                print(f"Server IP address found: {server_ip}")
                return server_ip
        except FileNotFoundError:
            server_ip = input("Enter the server's IP address: ").strip()
            return server_ip
    
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Initialize socket
        self.server = self.prompt_server_ip()  # Prompt for the server's IP address
        self.port = 7000
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def prompt_server_ip(self):
        ''' Prompt the user for the server's IP address '''
        while True:
            server_ip = input("Enter the server's IP address: ").strip()
            if self.validate_ip(server_ip):
                return server_ip
            print("Invalid IP address. Please try again.")

    def validate_ip(self, ip):
        # Check format of ip address
        parts = ip.split('.')
        if len(parts) != 4:
            return False    # Ensure there are 4 octets
        if all(0 > int(part) > 255 for part in parts):
            return False 
        try:
            socket.inet_aton(ip)
            return True
        except (socket.error, ValueError):
            return False
        
    def test_conncect(self,ip):
        '''Test connection to the server'''
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            test_socket.settimeout(2)  # Set a timeout for the connection test
            test_socket.connect((ip, self.port))  # Attempt to connect
            test_socket.close()
            return True
        except (socket.error, socket.timeout):
            return False
    
        
    def connect(self):
        ''' This method attempts to connect to the server. '''
        try: # Try to connect to server.
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048)) # Load object data.
        except: # Pass if there are errors.
            print("Unable to connect to the server. Please check the IP address and try again.")
            exit()


    def send(self, data):
        ''' This method sends some data to the server. '''
        try: # Send information to server.
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e: # Print an error if there is.
            print(e)
    
    def getP(self):
        ''' This method gets the player. '''
        return self.p