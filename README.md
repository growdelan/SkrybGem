# SkrybGem

Lokalna aplikacja webowa do dyktowania i odbierania poprawionego tekstu po polsku z użyciem LiteRT-LM.

## Wymagania
- macOS na Apple Silicon
- Python 3.13 zarządzany przez `uv`
- lokalny plik modelu `.litertlm` zgodny z LiteRT-LM

Przed uruchomieniem ustaw zmienną `MODEL_PATH` wskazującą na lokalny plik modelu.

## Uruchamianie
```bash
MODEL_PATH=/ścieżka/do/modelu.litertlm uv run python -m skrybgem
```

Domyślnie aplikacja startuje pod adresem `http://127.0.0.1:8000`.

Opcjonalnie można zmienić host i port:
```bash
MODEL_PATH=/ścieżka/do/modelu.litertlm SKRYBGEM_PORT=8010 uv run python -m skrybgem
```

## Testy
```bash
uv run python -m unittest discover -s tests -p "test_*.py"
```

## Ręczny smoke test
1. Ustaw `MODEL_PATH` na lokalny plik `.litertlm`.
2. Uruchom aplikację komendą z sekcji uruchamiania.
3. Otwórz adres pokazany w terminalu.
4. Zezwól przeglądarce na dostęp do mikrofonu.
5. Nagraj krótką wypowiedź po polsku.
6. Sprawdź, że aplikacja zwraca finalny tekst, pozwala go edytować i skopiować.
