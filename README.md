# s30723-python-game
do testów jednostkowych trzeba użyc  python -m pytest tests/
aby uruchomic gre w terminalu, należy użyć polecenia python.py, poruszamy sie wsadem po planszy.

aby zainstalowac odpowiednie pakiety
pip install -r requirements.txt

w stworzyc plik .env w projekcie MONGO_URI=mongodb+srv://s30723:gumadozycia@extrem1k.qfwowbb.mongodb.net/?retryWrites=true&w=majority&appName=extrem1k
aby przetestowac funkcjonalnosci crud wpisac w terminalu pytest

Użyłem bazy danych z chmurze atlas mongodb cloud



🔧 Co wykonuje pipeline:
1. Instalacja środowiska
Ustawia wersję Pythona (3.11)

Instaluje zależności z requirements.txt

Uruchamia kontener z MongoDB

2. Testowanie
Uruchamia testy jednostkowe (pytest)

Sprawdza pokrycie kodu (coverage)

3. Kontrola jakości kodu
Linting (flake8)

Formatowanie (black, isort)

4. Bezpieczeństwo
Analiza luk w zależnościach (safety)

Skanowanie kodu (bandit)

5. Testy uruchamiania aplikacji
Sprawdzenie czy moduły gry i API dają się zaimportować bez błędów

🧪 Jak przetestować działanie pipeline?
Wprowadź zmianę w pliku .py lub testowym

Zrób git push do main lub pull_request

Wejdź w repozytorium na zakładkę Actions:

Zobaczysz, że workflow się uruchomił

Sprawdź poszczególne kroki i logi

📛 Badge statusu:
Badge w README pokazuje aktualny stan pipeline:
