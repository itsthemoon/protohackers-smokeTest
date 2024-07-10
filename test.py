import socket
import threading
import time
import random
import string

SERVER_HOST = 'localhost'
SERVER_PORT = 8080
NUM_CLIENTS = 5
MAX_MESSAGE_LENGTH = 1024

def random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def client_thread(client_id):
    print(f"Client {client_id} starting")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_HOST, SERVER_PORT))
        
        total_sent = 0
        total_received = 0
        
        for _ in range(random.randint(1, 5)):
            message = random_string(random.randint(10, MAX_MESSAGE_LENGTH))
            s.sendall(message.encode())
            total_sent += len(message)
            
            received_data = b''
            while len(received_data) < len(message):
                chunk = s.recv(MAX_MESSAGE_LENGTH)
                if not chunk:
                    break
                received_data += chunk
            
            total_received += len(received_data)
            
            assert received_data.decode() == message, f"Client {client_id}: Received data doesn't match sent data"
            
            time.sleep(0.1)
        
        s.shutdown(socket.SHUT_WR)
        
        while True:
            chunk = s.recv(MAX_MESSAGE_LENGTH)
            if not chunk:
                break
            total_received += len(chunk)
        
        assert total_sent == total_received, f"Client {client_id}: Total sent ({total_sent}) doesn't match total received ({total_received})"
        print(f"Client {client_id} finished successfully")

def main():
    threads = []
    for i in range(NUM_CLIENTS):
        t = threading.Thread(target=client_thread, args=(i,))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    print("All clients finished. Test completed successfully!")

if __name__ == "__main__":
    main()