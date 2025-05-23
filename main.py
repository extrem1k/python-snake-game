import sys
import subprocess
import threading
import webbrowser
import time


def run_api():
    # Uruchom API na porcie 5000
    subprocess.run([sys.executable, "api.py"])


def run_server():
    # Uruchom serwer na porcie 8000
    subprocess.run([sys.executable, "server.py"])


if __name__ == "__main__":
    print("Uruchamianie gry Snake...")

    # Uruchom API w osobnym wątku
    api_thread = threading.Thread(target=run_api)
    api_thread.daemon = True
    api_thread.start()

    # Uruchom serwer w osobnym wątku
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()

    # Poczekaj 2 sekundy, aby serwery zdążyły się uruchomić
    time.sleep(2)

    # Otwórz przeglądarkę z grą
    print("Otwieranie gry w przeglądarce...")
    webbrowser.open("http://localhost:8000")

    try:
        # Utrzymuj główny wątek przy życiu, dopóki użytkownik nie przerwie programu
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nZamykanie aplikacji...")
        sys.exit(0)
