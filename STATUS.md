# Aktualny stan projektu

## Co działa
- lokalna aplikacja webowa uruchamiana komendą `uv run python -m skrybgem`
- prosty interfejs z przyciskiem `Start nagrywania`, przyciskiem kopiowania, statusem i edytowalnym polem wyniku
- backend HTTP z endpointem przetwarzania nagrania i kontrolowanym mapowaniem błędów
- pełny przepływ: nagranie → konwersja do WAV → przetwarzanie LiteRT-LM → finalny tekst → ręczna edycja → kopiowanie
- testy automatyczne dla warstwy API, logiki transkrypcji i kontraktu interfejsu

## Co jest skończone
- PRD bazowy w `prd/000-initial-prd.md`
- uzupełnione `spec.md`
- uzupełniona roadmapa z milestone'ami dla v1
- zaimplementowany i zweryfikowany Milestone 0.5
- poprawka błędu renderowania UI po wdrożeniu Milestone 0.5
- zaimplementowany Milestone 1: stabilizacja podstawowego przepływu użytkownika
- zaimplementowany Milestone 2: jakość wyniku i finalizacja tekstu

## Co jest w trakcie
- brak aktywnego milestone'u implementacyjnego
- brak kolejnych milestone'ów w roadmapie

## Co jest następne
- kolejna praca wymaga nowego zakresu planowania albo aktualizacji roadmapy
- ręczny smoke test z prawdziwym lokalnym plikiem `.litertlm` na docelowej maszynie użytkownika

## Blokery i ryzyka
- brak pliku modelu `.litertlm` w repo, więc pełny ręczny smoke z prawdziwym modelem zależy od lokalnej konfiguracji `MODEL_PATH`
- jakość finalnego tekstu zależy od realnego modelu i jakości nagrania użytkownika
- port `8000` może być zajęty przez wcześniej uruchomioną instancję lokalną; w takim przypadku trzeba uruchomić aplikację na innym porcie lub zamknąć poprzedni proces

## Ostatnie aktualizacje
- 2026-04-07: wygenerowano bazowy PRD, specyfikację i roadmapę
- 2026-04-07: wdrożono Milestone 0.5 jako minimalny działający slice aplikacji webowej
- 2026-04-07: poprawiono błąd renderowania interfejsu spowodowany nieprawidłowym zamknięciem tagu `style`
- 2026-04-07: wdrożono LiteRT-LM, walidację WAV, mapowanie błędów i rozszerzone testy dla Milestone 1 i 2
