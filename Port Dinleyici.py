import socket
import threading

def handle_client(client_socket, address, protocol):
    """
    Her bağlantı için ayrı bir iş parçacığında çalışacak.
    İstemciden gelen veriyi alır ve tekrar gönderir (Echo).
    """
    try:
        while True:
            # TCP bağlantısı için veri al
            if protocol == "tcp":
                data = client_socket.recv(1024)
            elif protocol == "udp":
                data, address = client_socket.recvfrom(1024)

            if not data:
                break  # Bağlantı kapanmışsa çık

            # Gelen veriyi geri gönder (Echo fonksiyonu)
            if protocol == "tcp":
                client_socket.sendall(data)
            elif protocol == "udp":
                client_socket.sendto(data, address)

    except Exception as e:
        print(f"Bağlantı hatası: {e}")
    finally:
        if protocol == "tcp":
            client_socket.close()
        print(f"Bağlantı kapandı: {address}")

def start_server(host, port, protocol):
    """
    Sunucu başlatılır, gelen bağlantıları kabul eder ve her biri için iş parçacığı oluşturur.
    """
    if protocol == "tcp":
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"TCP Sunucu {host}:{port} adresinde dinliyor...")
        
        while True:
            client_socket, address = server_socket.accept()
            print(f"Yeni bağlantı (TCP): {address}")

            # Yeni istemci için iş parçacığı başlat
            client_handler = threading.Thread(target=handle_client, args=(client_socket, address, protocol))
            client_handler.start()

    elif protocol == "udp":
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.bind((host, port))
        print(f"UDP Sunucu {host}:{port} adresinde dinliyor...")

        while True:
            data, address = server_socket.recvfrom(1024)
            print(f"Yeni UDP bağlantısı: {address}")

            # Gelen veriyi geri gönder
            server_socket.sendto(data, address)

if __name__ == "__main__":
    # Kullanıcıdan port numarası ve protokol seçimi alınacak
    host = "0.0.0.0"  # Tüm IP adreslerinden erişilebilir olacak
    port = int(input("Port numarasını girin: "))
    protocol = input("Protokol (TCP/UDP) seçin: ").lower()
    
    if protocol not in ["tcp", "udp"]:
        print("Geçersiz protokol seçimi! Lütfen 'TCP' veya 'UDP' seçin.")
        exit()

    # Sunucu başlatılır
    start_server(host, port, protocol)
