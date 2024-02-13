import socket

def run_client():
    host = '127.0.0.1'
    port = 12000

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((host, port))
        print(client_socket.recv(1024).decode())

        while True:
            guess = input("Enter your guess: ")
            client_socket.send(guess.encode())
            
            try:
                response = client_socket.recv(1024).decode()
            except ConnectionAbortedError:
                print("Connection closed unexpectedly by the server.")
                break
            
            print(response)

            if "Congratulations" in response or "Game over" in response:
                break

    except ConnectionError as e:
        print(f"ConnectionError: {e}")
    except Exception as e:
        print(f"Error: {e}")

    finally:
        client_socket.close()

if __name__ == "__main__":
    run_client()
