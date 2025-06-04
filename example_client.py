import socket
import pickle
import random
import time

client_id = random.randint(1, 100)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))

# pl: wysyłam id klienta do serwera
# ukr: відправляю id клієнта на сервер
client_socket.send(str(client_id).encode())
status = client_socket.recv(1024).decode()

if status == "REFUSED":
    print(f"\33[92m(CLIENT{client_id})\33[0m Odrzucono połączenie")
else:
    print(f"\33[92m(CLIENT{client_id})\33[0m Połączono")
    for cls in ['animal', 'car', 'book']:
        time.sleep(random.uniform(0.5, 1.5))
        client_socket.send(cls.encode())

        data = client_socket.recv(4096)
        try:
            objects = pickle.loads(data)
            for obj in objects:
                try:
                    print(f"\33[92m(CLIENT{client_id})\33[0m Otrzymano:", obj.opis())
                except AttributeError:
                    print(f"\33[92m(CLIENT{client_id})\33[0m Błąd rzutowania (niewłaściwy typ obiektu)")
        except Exception as e:
            print(f"\33[92m(CLIENT{client_id})\33[0m Błąd deserializacji:", e)

client_socket.close()