# s30723-python-game
do testów jednostkowych trzeba użyc  python -m pytest tests/
aby uruchomic gre w terminalu, należy użyć polecenia python.py

aby zainstalowac odpowiednie pakiety
pip install -r requirements.txt







DEMO I PREZENTACJA JEST W REPOZYTORIUM. TRZEBA JE POBRAC





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

[📛 Badge statusu:
Badge w README pokazuje aktualny stan pipeline:](https://github.com/PPY-2025/s30723-python-game/actions/workflows/ci.yml/badge.svg)
