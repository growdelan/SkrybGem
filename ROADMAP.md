# Roadmapa (milestones)

## Statusy milestone’ów
Dozwolone statusy:
- planned
- in_progress
- done
- blocked

---

## Milestone 0.5: Minimal end-to-end slice (done)

Cel:
- aplikacja uruchamia się lokalnie jako minimalna webowa wersja SkrybGem
- użytkownik może przejść przez najprostszy pełny przepływ od nagrania do otrzymania finalnego tekstu
- istnieje minimalne potwierdzenie, że przepływ end-to-end działa

Definition of Done:
- aplikację da się uruchomić jednym poleceniem opisanym w README.md
- użytkownik może rozpocząć nagranie, zakończyć je i zobaczyć finalny tekst po korekcie w jednym prostym widoku
- istnieje co najmniej jeden smoke test dla minimalnego przepływu end-to-end
- testy przechodzą lokalnie
- brak placeholderów w kodzie w zakresie objętym milestone’em

Zakres:
- minimalny entrypoint aplikacji webowej
- minimalna obsługa mikrofonu i przycisków `Start/Stop`
- minimalna ścieżka przetwarzania prowadząca do finalnego tekstu po korekcie
- minimalny ekran z wynikiem możliwym do ręcznej edycji i skopiowania
- smoke test end-to-end dla najprostszego scenariusza sukcesu

Uwagi:
- zrealizowano bootstrapowy lokalny backend HTTP i prosty frontend webowy
- Milestone 0.5 używa deterministycznego procesora bootstrapowego pod docelowym kontraktem backendowym
- po wdrożeniu poprawiono błąd renderowania interfejsu wynikający z nieprawidłowego zamknięcia tagu `style`

---

## Milestone 1: Stabilizacja podstawowego przepływu użytkownika (done)

Cel:
- domknąć podstawowy przepływ użytkownika opisany w PRD tak, aby był przewidywalny i odporny na podstawowe błędy wejścia
- zapewnić czytelną komunikację stanów aplikacji i błędów

Definition of Done:
- aplikacja komunikuje stany gotowości, nagrywania, przetwarzania i błędu
- brak dostępu do mikrofonu jest obsłużony czytelnym komunikatem
- puste albo zbyt krótkie nagranie jest obsłużone bez zwracania mylącego wyniku
- błąd przetwarzania pozwala użytkownikowi ponowić próbę bez zablokowania interfejsu
- istnieją testy pokrywające co najmniej scenariusze: brak mikrofonu, puste nagranie i błąd przetwarzania

Zakres:
- dopracowanie stanów interfejsu w ramach pojedynczego głównego widoku
- obsługa błędów i komunikatów użytkownika dla kluczowych przypadków z PRD
- doprecyzowanie zachowania aplikacji przy nieudanym lub bezwartościowym nagraniu
- rozszerzenie testów o scenariusze negatywne i graniczne

Uwagi:
- milestone nie rozszerza produktu o historię, upload plików ani wielojęzyczność
- wdrożono kontrolowane mapowanie błędów `400/422/503/500` oraz komunikaty UI dla stanów i błędów nagrywania
- rozszerzono testy automatyczne o scenariusze negatywne i graniczne dla backendu

---

## Milestone 2: Jakość wyniku i finalizacja tekstu (done)

Cel:
- podnieść jakość finalnego tekstu do poziomu zgodnego z obietnicą produktu dla polskiego dyktowania
- domknąć końcową część przepływu: edycję i kopiowanie gotowego tekstu

Definition of Done:
- finalny wynik zawiera poprawioną interpunkcję i wielkie litery w typowych przypadkach
- finalny wynik zachowuje sens wypowiedzi i nie jest traktowany jak odpowiedź konwersacyjna modelu
- użytkownik może ręcznie edytować wynik przed kopiowaniem
- użytkownik może skopiować aktualny tekst jednym kliknięciem i otrzymuje potwierdzenie wykonania akcji
- istnieją testy potwierdzające podstawowy przepływ edycji i kopiowania

Zakres:
- dopracowanie jakości finalnego tekstu zgodnie z zakresem PRD
- utrwalenie zasady prezentacji jednego finalnego wyniku bez surowej transkrypcji w podstawowym UI
- obsługa ręcznej edycji wyniku
- obsługa kopiowania do schowka i komunikatu o powodzeniu

Uwagi:
- milestone nie dodaje historii sesji ani trwałego przechowywania danych
- bootstrapowy wynik stały został zastąpiony integracją LiteRT-LM z wymuszeniem pojedynczego finalnego tekstu
- frontend przygotowuje WAV przed wysyłką, a wynik pozostaje edytowalny i kopiowalny w jednym widoku
