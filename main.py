import socket
import threading


client_in_server = []


def client_proc(client, addr):
    msg = "Your Username: "
    client.sendall(bytes(msg, "utf-8"))
    username = client.recv(1024).decode("utf-8")
    print(f"Client: {client}\n Username: {username}\n connected to server!\n")
    msg = "You're connected!\n"
    client.sendall(bytes(msg, "utf-8"))
    client_in_server.append(client)
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            if not message:
                break
            if message.startswith("/private"):
                parts = message.split(' ', 2)
                if len(parts) >= 3:
                    recipient, private_message = parts[1], parts[2]
                    recipient.sendall(bytes(private_message, "utf-8"))

            elif message == "/quit\n":
                break
            else:
                username = username.rstrip('\n')
                message = username + ": " + message
                print(message)
                for recipient in client_in_server:
                    if recipient == client:
                        continue
                    print(recipient)
                    recipient.sendall(bytes(message, "utf-8"))
        except Exception as e:
            print("err: " + e.__str__())
    # xoa client khi ngat ket noi
    client_in_server.remove(client)
    client.close()
    message = f"{username} disconnected!"

    print(message)
    for recipient in client_in_server:
        if recipient == client:
            continue
        recipient.sendall(bytes(message, "utf-8"))

def start_server():
    HOST = "127.0.0.1"
    PORT = 8000

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(5)

    while True:
        print("Waiting for new client\n")
        client, addr = s.accept()
        print("New client accepted, client = %d\n", client)
        client_handler = threading.Thread(target = client_proc, args = (client, addr))
        client_handler.start()

if __name__ == "__main__":
    start_server()

