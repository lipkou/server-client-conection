from example_classes import Animal, Car, Book
import socket
import threading
import pickle
import random
import time

# pl: maksymalna liczba klientów
# ukr: максимальна кількість клієнтів
MAX_CLIENTS = 3
clients_count = 0
clients_lock = threading.Lock()

# pl: maksymalna liczba klientów
# ukr: максимальна кількість клієнтів
MAX_CLIENTS = 3
clients_count = 0
clients_lock = threading.Lock()

# pl: inicjalizuję mapę obiektów
# ukr: ініціалізую карту об'єктів
object_map = {}
for i in range(1, 5):
    object_map[f"animal_{i}"] = Animal(f"Animal_{i}", random.randint(1, 10))
    object_map[f"car_{i}"] = Car(f"Model_{i}", 2000 + random.randint(-5, 25))
    object_map[f"book_{i}"] = Book(f"Book_{i}", 100 + random.randint(-2, 5) * 10)

# pl: obsługa klienta w osobnym wątku
# ukr: обробка клієнта в окремому потоці
def handle_client(client_socket, client_address):
    global clients_count
    try:
        # pl: losowe opóźnienie symulujące obciążenie serwera
        # ukr: випадкова затримка для імітації навантаження
        time.sleep(random.randint(2, 10))

        # pl: odbieram id klienta
        # ukr: приймаю id клієнта
        client_id = int(client_socket.recv(1024).decode())

        with clients_lock:
            if clients_count >= MAX_CLIENTS:
                # pl: za dużo klientów, odmawiam połączenia
                # ukr: занадто багато клієнтів — відмовляю у з'єднанні
                client_socket.send(b"REFUSED")
                print("\33[94m(SERVER)\33[0m Odrzucono klienta:", client_id)
                return
            else:
                # pl: akceptuję klienta
                # ukr: приймаю клієнта
                clients_count += 1
                client_socket.send(b"OK")
                print("\33[94m(SERVER)\33[0m Obsługuje klienta:", client_id)

        while True:
            # pl: odbieram zapytanie o klasę obiektów
            # ukr: приймаю запит на клас об'єктів
            data = client_socket.recv(1024).decode()
            if not data:
                break

            requested_class = data.strip().lower()
            # pl: filtruję obiekty według nazwy klasy
            # ukr: фільтрую об'єкти за назвою класу
            objects_to_send = [obj for key, obj in object_map.items() if key.startswith(requested_class)]

            if not objects_to_send:
                # pl: brak obiektów tej klasy — wysyłam losowy obiekt
                # ukr: немає об'єктів цього класу — відправляю випадковий
                random_key = random.choice(list(object_map.keys()))
                objects_to_send = [object_map[random_key]]

            # pl: serializuję obiekty i wysyłam
            # ukr: серіалізую об'єкти і відправляю
            serialized = pickle.dumps(objects_to_send)
            client_socket.send(serialized)

            print("\33[94m(SERVER)\33[0m Wysłałem do klienta", client_id, ":", [obj.opis() for obj in objects_to_send])

    except Exception as e:
        print("\33[94m(SERVER)\33[0m Błąd:", e)
    finally:
        with clients_lock:
            clients_count -= 1
        client_socket.close()

# pl: uruchamiam serwer
# ukr: запускаю сервер
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen()
print("\33[94m(SERVER)\33[0m Serwer nasłuchuje na porcie 12345")

while True:
    client_sock, addr = server_socket.accept()
    threading.Thread(target=handle_client, args=(client_sock, addr), daemon=True).start()


