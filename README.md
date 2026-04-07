# SkrybGem

Lokalna aplikacja webowa do dyktowania i odbierania poprawionego tekstu po polsku z użyciem LiteRT-LM.

## Wymagania
- macOS na Apple Silicon
- Python 3.13 zarządzany przez `uv`
- lokalny plik modelu `.litertlm` zgodny z LiteRT-LM

Przed uruchomieniem uzupełnij plik `.env` w katalogu projektu.

Model można pobrać stąd:
- [litert-community/gemma-4-E2B-it-litert-lm](https://huggingface.co/litert-community/gemma-4-E2B-it-litert-lm/tree/main)

Domyślne zmienne używane przez aplikację:
```env
MODEL_PATH=/pelna/sciezka/do/modelu.litertlm
SKRYBGEM_HOST=127.0.0.1
SKRYBGEM_PORT=8000
```

## Uruchamianie
```bash
uv run python -m skrybgem
```

Domyślnie aplikacja startuje pod adresem ustawionym przez `SKRYBGEM_HOST` i `SKRYBGEM_PORT` z `.env`.

## Testy
```bash
uv run python -m unittest discover -s tests -p "test_*.py"
```

## Ręczny smoke test
1. Ustaw `MODEL_PATH` w `.env` na lokalny plik `.litertlm`.
2. Uruchom aplikację komendą z sekcji uruchamiania.
3. Otwórz adres pokazany w terminalu.
4. Zezwól przeglądarce na dostęp do mikrofonu.
5. Nagraj krótką wypowiedź po polsku.
6. Sprawdź, że aplikacja zwraca finalny tekst, pozwala go edytować i skopiować.
