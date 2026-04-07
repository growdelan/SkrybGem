# Specyfikacja techniczna

## Cel
SkrybGem to lokalna aplikacja webowa do dyktowania tekstu po polsku, której celem jest szybka zamiana wypowiedzi głosowej na poprawiony, czytelny tekst gotowy do dalszej edycji i skopiowania.

Problem, który rozwiązuje:
- eliminuje potrzebę ręcznego przepisywania mowy do tekstu,
- skraca czas potrzebny na poprawienie interpunkcji, wielkich liter i podstawowej czytelności tekstu,
- pozwala pracować lokalnie, bez zależności od zewnętrznych usług transkrypcyjnych.

Grupa docelowa:
- pojedynczy użytkownik lokalny pracujący na własnym komputerze,
- osoba dyktująca po polsku krótkie i średnie wypowiedzi do dalszego wklejenia w inne miejsce.

Zakres obowiązywania tej wersji:
- aplikacja webowa uruchamiana lokalnie,
- nagrywanie mikrofonu w modelu `Start/Stop`,
- wygenerowanie jednego finalnego tekstu po korekcie,
- ręczna edycja wyniku i skopiowanie do schowka.

Poza zakresem:
- historia transkrypcji,
- zapis na dysk i eksport,
- upload plików audio,
- wielojęzyczność,
- odpowiedzi głosowe i tryb konwersacyjny,
- integracje systemowe typu automatyczne wklejanie do aktywnego okna.

---

## Zakres funkcjonalny (high-level)
Kluczowe use-case’i:
- szybkie podyktowanie notatki i skopiowanie poprawionego tekstu,
- przygotowanie krótkiej wiadomości lub szkicu tekstu bez ręcznego stawiania interpunkcji,
- zamiana mówionego roboczego szkicu na tekst nadający się do dalszej redakcji.

Główny przepływ użytkownika:
- użytkownik otwiera aplikację i widzi prosty ekran z kontrolą nagrywania oraz obszarem wyniku,
- rozpoczyna nagranie jednym kliknięciem,
- kończy nagranie drugim kliknięciem,
- aplikacja przechodzi do stanu przetwarzania i zwraca finalny tekst po korekcie,
- użytkownik edytuje wynik ręcznie, jeśli chce,
- użytkownik kopiuje aktualny tekst jednym kliknięciem.

Aplikacja nie robi w tej wersji:
- nie pokazuje surowej transkrypcji jako głównego wyniku,
- nie przechowuje historii sesji,
- nie przetwarza plików audio,
- nie działa jako ogólny asystent AI,
- nie odpowiada głosem,
- nie obsługuje kamery ani innych źródeł wejścia poza mikrofonem.

---

## Architektura i przepływ danych
Opis architektury na poziomie koncepcyjnym.

1. Główne komponenty systemu
- lokalny interfejs webowy odpowiedzialny za obsługę użytkownika, stany nagrywania, wyświetlanie wyniku, ręczną edycję i kopiowanie,
- lokalny backend aplikacji odpowiedzialny za przyjęcie nagrania, uruchomienie przetwarzania i zwrócenie finalnego tekstu,
- warstwa modelowa odpowiedzialna za rozpoznanie mowy i korektę tekstu w jednym przepływie.

2. Przepływ danych między komponentami
- użytkownik nagrywa wypowiedź przez interfejs webowy,
- nagranie trafia do lokalnego backendu,
- backend przekazuje dane audio do warstwy modelowej,
- warstwa modelowa zwraca finalny tekst po korekcie,
- backend przekazuje wynik do interfejsu,
- użytkownik edytuje i kopiuje tekst po stronie interfejsu.

3. Granice odpowiedzialności
- frontend odpowiada za doświadczenie użytkownika i lokalny stan interfejsu,
- backend odpowiada za orkiestrację przetwarzania i obsługę błędów,
- model odpowiada za jakość transkrypcji i podstawową redakcję tekstu,
- trwałe przechowywanie danych nie jest częścią tej wersji produktu.

---

## Komponenty techniczne
Lista kluczowych komponentów technicznych i ich odpowiedzialności.

- Interfejs webowy: rozpoczęcie i zakończenie nagrywania, prezentacja stanów, edycja tekstu, kopiowanie do schowka.
- Obsługa mikrofonu: pobranie audio od użytkownika w bieżącej sesji.
- Lokalny backend: przyjęcie żądania przetwarzania, walidacja podstawowych warunków wejścia, zwrot finalnego tekstu lub kontrolowanego błędu HTTP.
- Warstwa transkrypcji i korekty: zamiana nagrania WAV na poprawiony tekst po polsku.
- Integracja modelowa: uruchomienie modelu klasy `E2B` przez LiteRT-LM.
- Testy smoke: potwierdzenie, że minimalny przepływ end-to-end działa dla pierwszej wersji.

---

## Decyzje techniczne
Jawne decyzje techniczne wraz z uzasadnieniem.

Każda decyzja powinna zawierać:
- Decyzja:
- Uzasadnienie:
- Konsekwencje:

- Decyzja: Pierwsza wersja produktu będzie lokalną aplikacją webową z lokalnym backendem.
  Uzasadnienie: Wynika bezpośrednio z PRD, który wskazuje przeglądarkę i lokalny backend jako docelową platformę v1.
  Konsekwencje: Zakres implementacji obejmuje interfejs przeglądarkowy i warstwę backendową, ale nie obejmuje aplikacji desktop native ani CLI jako głównego produktu.

- Decyzja: Rozpoznawanie mowy i korekta tekstu będą oparte o model klasy `E2B` uruchamiany przez LiteRT-LM.
  Uzasadnienie: Jest to jawne założenie produktowe zapisane w PRD oraz kierunek inspirowany podejściem z repozytorium `parlor`.
  Konsekwencje: Specyfikacja zakłada lokalne przetwarzanie modelowe i wyklucza zewnętrzne usługi transkrypcyjne jako podstawę v1.

- Decyzja: Podstawowy wynik w v1 to wyłącznie finalny tekst po korekcie, bez eksponowania surowej transkrypcji w głównym interfejsie.
  Uzasadnienie: PRD definiuje jeden wynik końcowy jako podstawowe doświadczenie użytkownika.
  Konsekwencje: Projekt interfejsu i roadmapa skupiają się na jakości finalnego tekstu, edycji i kopiowaniu, a nie na wielowidokowym porównywaniu wyników.

- Decyzja: Bieżąca implementacja v1 używa LiteRT-LM ładowanego przy starcie procesu na podstawie zmiennej środowiskowej `MODEL_PATH`.
  Uzasadnienie: Milestone 1 i 2 wymagają realnej lokalnej integracji modelowej, a nie dalszego używania bootstrapowego procesora.
  Konsekwencje: Aplikacja może wystartować bez modelu, ale endpoint transkrypcji zwraca wtedy kontrolowany błąd `503`, dopóki użytkownik nie wskaże poprawnego pliku `.litertlm`.

- Decyzja: Frontend wysyła do backendu nagranie WAV przygotowane lokalnie w przeglądarce.
  Uzasadnienie: Ścieżka audio LiteRT-LM jest najbezpieczniejsza dla jawnego formatu wejściowego, a aplikacja ma wspierać tylko format generowany przez własny frontend.
  Konsekwencje: Backend waliduje podstawową strukturę WAV i odrzuca inne formaty jako błąd wejścia użytkownika.

---

## Jakość i kryteria akceptacji
Wspólne wymagania jakościowe dla całego projektu:

- aplikacja ma prowadzić użytkownika przez prosty i jednoznaczny przepływ `Start` → `Stop` → przetwarzanie → edycja → kopiowanie,
- wynik ma zachowywać sens wypowiedzi użytkownika i poprawiać podstawową czytelność tekstu,
- użytkownik ma zawsze widzieć aktualny stan aplikacji: gotowość, nagrywanie, przetwarzanie albo błąd,
- brak dostępu do mikrofonu ma być obsłużony czytelnym komunikatem,
- puste albo zbyt krótkie nagranie nie może skutkować mylącym finalnym tekstem,
- błąd przetwarzania ma pozwalać na ponowienie próby bez utraty kontroli nad interfejsem,
- aplikacja ma działać bez wymogu zewnętrznych usług transkrypcyjnych dla podstawowego przepływu.

---

## Zasady zmian i ewolucji
- zmiany funkcjonalne → aktualizacja `ROADMAP.md`
- zmiany architektoniczne → aktualizacja tej specyfikacji
- nowe zależności → wpis do `## Decyzje techniczne`
- refactory tylko w ramach aktualnego milestone’u
- rozszerzenia produktu wykraczające poza v1 muszą wynikać z kolejnych PRD albo jawnej aktualizacji obecnego zakresu
- elementy oznaczone jako poza zakresem nie powinny być dodawane przy okazji milestone’ów v1 bez aktualizacji dokumentacji

---

## Powiązanie z roadmapą
- Szczegóły milestone’ów i ich statusy znajdują się w `ROADMAP.md`.
- Roadmapa ma realizować minimalny działający slice w Milestone 0.5, a następnie rozwijać aplikację w kierunku pełnego przepływu opisanego w PRD.
- Każdy milestone musi wspierać co najmniej jeden element celu produktu, zakresu funkcjonalnego lub wspólnych kryteriów jakościowych opisanych w tej specyfikacji.

---

## Status specyfikacji
- Data utworzenia: 2026-04-07
- Ostatnia aktualizacja: 2026-04-07
- Aktualny zakres obowiązywania: SkrybGem v1 opisany w `prd/000-initial-prd.md`
