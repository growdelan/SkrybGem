# Aktualny stan projektu

## Co działa
- lokalna aplikacja webowa uruchamiana komendą `uv run python -m skrybgem`
- prosty interfejs z przyciskiem `Start nagrywania`, przyciskiem kopiowania, statusem i edytowalnym polem wyniku
- minimalny backend HTTP z endpointem przetwarzania nagrania
- bootstrapowy pełny przepływ: nagranie → przetwarzanie → finalny tekst → ręczna edycja → kopiowanie
- smoke test sprawdzający stronę główną i minimalny przepływ API

## Co jest skończone
- PRD bazowy w `prd/000-initial-prd.md`
- uzupełnione `spec.md`
- uzupełniona roadmapa z milestone'ami dla v1
- zaimplementowany i zweryfikowany Milestone 0.5
- poprawka błędu renderowania UI po wdrożeniu Milestone 0.5

## Co jest w trakcie
- brak aktywnego milestone'u implementacyjnego
- następny logiczny etap to Milestone 1: stabilizacja podstawowego przepływu użytkownika

## Co jest następne
- obsługa błędów i stanów granicznych zgodnie z Milestone 1
- czytelne komunikaty dla braku dostępu do mikrofonu, pustego nagrania i błędu przetwarzania
- rozszerzenie testów o scenariusze negatywne i graniczne

## Blokery i ryzyka
- Milestone 0.5 używa bootstrapowego procesora deterministycznego zamiast docelowej integracji LiteRT-LM
- brak jeszcze pełnej jakości transkrypcji zgodnej z docelową obietnicą produktu
- port `8000` może być zajęty przez wcześniej uruchomioną instancję lokalną; w takim przypadku trzeba uruchomić aplikację na innym porcie lub zamknąć poprzedni proces

## Ostatnie aktualizacje
- 2026-04-07: wygenerowano bazowy PRD, specyfikację i roadmapę
- 2026-04-07: wdrożono Milestone 0.5 jako minimalny działający slice aplikacji webowej
- 2026-04-07: poprawiono błąd renderowania interfejsu spowodowany nieprawidłowym zamknięciem tagu `style`
