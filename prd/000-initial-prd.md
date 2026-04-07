# PRD 000: SkrybGem v1

## Dokument
- Wersja: 1.0
- Status: draft zaakceptowany do dalszej specyfikacji technicznej
- Zakres: wyłącznie pierwsza wersja produktu
- Język produktu: polski

## 1. Cel produktu
SkrybGem v1 to lokalna aplikacja webowa do dyktowania tekstu po polsku. Użytkownik ma móc nacisnąć przycisk rozpoczęcia nagrywania, wypowiedzieć treść do mikrofonu, zatrzymać nagranie, a następnie otrzymać poprawioną transkrypcję gotową do dalszej edycji i skopiowania.

Produkt ma rozwiązać prosty, konkretny problem: szybkie zamienienie mowy na czytelny, uporządkowany tekst bez konieczności korzystania z usług chmurowych, zewnętrznych API lub ręcznego poprawiania całej interpunkcji od zera.

## 2. Problem użytkownika
Użytkownik chce mówić naturalnie, ale finalnie potrzebuje tekstu, który nadaje się do wklejenia do notatki, wiadomości, dokumentu albo innego narzędzia. Surowa transkrypcja mowy zwykle zawiera błędy typowe dla mówionego języka:

- brak interpunkcji,
- brak wielkich liter,
- nieuporządkowane zdania,
- wypełniacze i potoczny rytm wypowiedzi,
- słabszą czytelność przy dłuższych wypowiedziach.

SkrybGem v1 ma skrócić drogę od wypowiedzi głosowej do finalnego tekstu, który użytkownik jeszcze szybko przeczyta, poprawi w razie potrzeby i skopiuje.

## 3. Grupa docelowa
Pierwsza wersja produktu jest przeznaczona dla pojedynczego użytkownika lokalnego, który:

- pracuje na własnym komputerze,
- chce szybko dyktować po polsku,
- zależy mu na prywatności i lokalnym przetwarzaniu,
- nie potrzebuje rozbudowanego systemu archiwizacji ani pracy zespołowej,
- oczekuje prostego interfejsu i krótkiej ścieżki do gotowego tekstu.

Nie zakłada się w v1 pracy wieloużytkownikowej, kont, synchronizacji ani współdzielenia danych.

## 4. Wizja v1
Produkt ma być mały, czytelny i jednofunkcyjny. Główna wartość ma wynikać z połączenia czterech rzeczy:

- prostego uruchomienia lokalnie,
- nagrywania jednym prostym przepływem `Start/Stop`,
- automatycznej poprawy transkrypcji,
- możliwości ręcznej edycji przed kopiowaniem.

To nie ma być ogólny asystent głosowy ani aplikacja do rozmowy z AI. To ma być narzędzie do sprawnego tworzenia gotowego tekstu z mowy.

## 5. Zakres produktu w v1

### W zakresie
Do pierwszej wersji wchodzą:

- lokalna aplikacja webowa uruchamiana na komputerze użytkownika,
- interfejs z głównym przyciskiem rozpoczęcia i zakończenia nagrywania,
- użycie mikrofonu jako jedynego źródła wejścia,
- przetworzenie nagrania lokalnie przy użyciu modelu klasy `E2B` uruchamianego przez LiteRT-LM,
- wygenerowanie jednego finalnego tekstu po korekcie,
- możliwość ręcznej edycji finalnego tekstu przez użytkownika,
- możliwość skopiowania finalnego tekstu jednym kliknięciem,
- podstawowe komunikaty stanu i błędu,
- działanie w języku polskim.

### Poza zakresem
Do v1 nie wchodzą:

- historia wcześniejszych transkrypcji,
- automatyczny zapis na dysk,
- eksport do plików,
- upload plików audio,
- transkrypcja już istniejących nagrań,
- obsługa wielu języków,
- automatyczne wykrywanie języka,
- odpowiedzi głosowe,
- tryb konwersacyjny,
- kamera i wejście wideo,
- integracja z aktywnym oknem systemu,
- automatyczne wklejanie tekstu do innych aplikacji,
- konta użytkowników,
- ustawienia chmurowe,
- zewnętrzne API do transkrypcji,
- tryb hands-free oparty o automatyczny VAD jako główny mechanizm produktu.

## 6. Kluczowe założenia produktowe

### 6.1. Prywatność
Produkt ma działać w pełni lokalnie. Nagranie i transkrypcja mają pozostawać na urządzeniu użytkownika. Po przygotowaniu środowiska i modelu aplikacja ma być używalna offline.

### 6.2. Prostota interakcji
Podstawowy przepływ ma opierać się o klikany model `Start/Stop`. Nie należy projektować v1 wokół push-to-talk ani pełnej automatyki wykrywania końca mowy jako głównego zachowania produktu.

### 6.3. Jeden wynik końcowy
Podstawowy interfejs ma prezentować wyłącznie finalny tekst po korekcie. Surowa transkrypcja nie jest częścią podstawowego doświadczenia użytkownika w v1.

### 6.4. Bieżąca sesja bez trwałej pamięci
Produkt ma obsługiwać tylko bieżącą sesję roboczą. Zamknięcie lub odświeżenie aplikacji nie musi zachowywać wcześniejszego wyniku.

## 7. Główne use-case'i

### Use-case 1: szybkie dyktowanie notatki
Użytkownik chce szybko podyktować treść, otrzymać poprawiony tekst, wprowadzić drobne poprawki i skopiować wynik.

### Use-case 2: redakcja krótkiej wiadomości
Użytkownik mówi naturalnie, bez dyktowania znaków interpunkcyjnych, a system przygotowuje tekst w formie bardziej czytelnej i gotowej do wysłania po ręcznej kontroli.

### Use-case 3: zamiana mówionego szkicu na tekst roboczy
Użytkownik dyktuje dłuższy szkic akapitu lub listy myśli, a system porządkuje zapis do formy łatwej do dalszej edycji.

## 8. Główny przepływ użytkownika

### Przepływ podstawowy
1. Użytkownik otwiera aplikację.
2. Użytkownik widzi prosty główny ekran z obszarem nagrywania i obszarem wyniku.
3. Użytkownik naciska przycisk `Start nagrywania`.
4. Aplikacja przechodzi do stanu nagrywania i jasno to komunikuje.
5. Użytkownik mówi do mikrofonu po polsku.
6. Użytkownik naciska przycisk `Stop`.
7. Aplikacja kończy nagranie i przechodzi do stanu przetwarzania.
8. System lokalnie tworzy poprawioną transkrypcję.
9. Aplikacja wyświetla finalny tekst w polu edycyjnym.
10. Użytkownik ręcznie poprawia tekst, jeśli chce.
11. Użytkownik naciska `Kopiuj`.
12. Tekst trafia do schowka.

### Oczekiwane właściwości przepływu
- przepływ ma być czytelny bez dodatkowych instrukcji,
- użytkownik ma zawsze wiedzieć, czy aplikacja nagrywa, przetwarza czy jest gotowa,
- użytkownik nie musi widzieć surowych danych technicznych ani etapów modelu,
- wynik ma być gotowy do edycji i kopiowania bez dodatkowego przełączania widoków.

## 9. Wymagania funkcjonalne

### 9.1. Nagrywanie
Aplikacja musi:

- umożliwiać rozpoczęcie nagrywania jednym kliknięciem,
- umożliwiać zatrzymanie nagrywania jednym kliknięciem,
- korzystać z mikrofonu urządzenia użytkownika,
- jasno sygnalizować aktywny stan nagrywania,
- blokować niejednoznaczne stany interfejsu, np. jednoczesne nagrywanie i przetwarzanie.

### 9.2. Przetwarzanie transkrypcji
System musi:

- przyjąć nagranie z bieżącej sesji,
- przetworzyć je lokalnie,
- wygenerować jeden finalny tekst po korekcie,
- zachować sens wypowiedzi użytkownika,
- poprawić podstawowe elementy redakcyjne tekstu.

### 9.3. Jakość wyniku
Finalny tekst ma:

- zawierać poprawioną interpunkcję,
- stosować wielkie litery tam, gdzie są oczywiste,
- porządkować zdania do formy czytelnej pisemnie,
- wygładzać oczywiste cechy mowy potocznej tylko wtedy, gdy nie zmienia to sensu,
- nie dopisywać nowych informacji, których użytkownik nie wypowiedział.

### 9.4. Edycja wyniku
Aplikacja musi:

- pokazywać finalny tekst w polu, które można edytować,
- pozwalać użytkownikowi swobodnie poprawić tekst po stronie interfejsu,
- nie wymagać ponownego przetwarzania tylko dlatego, że użytkownik chce poprawić kilka słów ręcznie.

### 9.5. Kopiowanie
Aplikacja musi:

- umożliwiać skopiowanie finalnego, aktualnie widocznego tekstu jednym kliknięciem,
- kopiować także wersję po ręcznych poprawkach użytkownika,
- potwierdzać powodzenie akcji kopiowania zrozumiałym komunikatem.

## 10. Wymagania niefunkcjonalne

### 10.1. Lokalność działania
Rozpoznawanie i korekta tekstu mają działać bez zewnętrznych usług transkrypcyjnych. Produkt ma być projektowany jako rozwiązanie local-first.

### 10.2. Prostota UX
Interfejs ma być prosty, skupiony na jednym zadaniu i pozbawiony zbędnych paneli, historii i trybów pracy.

### 10.3. Czytelność stanu
Użytkownik ma zawsze wiedzieć:

- czy mikrofon jest dostępny,
- czy aplikacja nagrywa,
- czy trwa przetwarzanie,
- czy wynik jest gotowy do edycji i kopiowania,
- czy wystąpił błąd wymagający reakcji.

### 10.4. Przewidywalność
Produkt ma zachowywać się konsekwentnie. Kliknięcie `Start` zawsze zaczyna nową sesję nagrywania, a kliknięcie `Stop` zawsze kończy bieżące nagranie i rozpoczyna przetwarzanie.

## 11. Interfejs użytkownika na poziomie produktu
PRD nie definiuje warstwy wizualnej w szczegółach, ale ustala minimalny układ funkcjonalny:

- jeden główny obszar sterowania nagrywaniem,
- jasny wskaźnik aktualnego stanu,
- jeden główny edytowalny obszar tekstowy z finalnym wynikiem,
- przycisk kopiowania,
- komunikaty błędów i stanów widoczne dla użytkownika.

Interfejs ma eksponować finalny rezultat, a nie mechanikę modelu.

## 12. Oczekiwane zachowanie modelu na poziomie produktu
Warstwa modelowa ma być dla użytkownika przezroczysta, ale produktowo zakładamy:

- użycie modelu klasy `E2B`,
- uruchomienie przez LiteRT-LM,
- inspirację podejściem z repozytorium `parlor`,
- połączenie rozpoznania mowy i korekty tekstu w jednym przepływie,
- brak osobnego doświadczenia „chatowego”.

Na poziomie produktu wynik ma być traktowany jako poprawiona transkrypcja, nie jako swobodna odpowiedź modelu.

## 13. Scenariusze sukcesu

### Scenariusz A: standardowe użycie
- użytkownik otwiera aplikację,
- widzi gotowy interfejs do nagrania i wynik,
- zaczyna nagrywanie jednym kliknięciem,
- kończy nagranie drugim kliknięciem,
- otrzymuje poprawiony tekst,
- edytuje go ręcznie,
- kopiuje go jednym kliknięciem.

### Scenariusz B: brak dostępu do mikrofonu
- użytkownik otwiera aplikację,
- aplikacja wykrywa brak dostępu do mikrofonu albo odrzucenie uprawnień,
- użytkownik dostaje jasny komunikat,
- nagrywanie nie może zostać rozpoczęte do czasu rozwiązania problemu.

### Scenariusz C: puste lub zbyt krótkie nagranie
- użytkownik rozpoczyna i szybko kończy nagranie albo nic nie mówi,
- system nie zwraca mylącej transkrypcji,
- użytkownik dostaje zrozumiałą informację, że nie udało się uzyskać sensownego tekstu.

### Scenariusz D: błąd przetwarzania
- po zakończeniu nagrania występuje błąd po stronie przetwarzania,
- użytkownik dostaje komunikat o niepowodzeniu,
- interfejs wraca do stanu, z którego można ponowić próbę,
- aplikacja nie blokuje się w stanie pośrednim.

## 14. Kryteria akceptacji v1
Wersję pierwszą uznajemy za zgodną z PRD, jeśli:

- użytkownik może uruchomić lokalną aplikację webową i zobaczyć główny ekran,
- aplikacja umożliwia nagrywanie mikrofonu w modelu `Start/Stop`,
- po zakończeniu nagrania aplikacja zwraca jeden finalny tekst po korekcie,
- użytkownik może ten tekst ręcznie edytować,
- użytkownik może skopiować aktualną treść jednym kliknięciem,
- aplikacja poprawnie komunikuje stany nagrywania, przetwarzania i gotowości,
- brak dostępu do mikrofonu jest obsłużony czytelnym błędem,
- puste lub bezwartościowe nagranie nie prowadzi do mylącego wyniku,
- błąd przetwarzania pozwala użytkownikowi ponowić próbę,
- system nie wymaga usług chmurowych do samej transkrypcji i korekty.

## 15. Miary sukcesu produktu
W v1 sukces ma być oceniany głównie jakościowo i użytkowo:

- użytkownik jest w stanie przejść od otwarcia aplikacji do skopiowania tekstu bez instrukcji krok po kroku,
- finalny tekst wymaga tylko lekkiej ręcznej korekty zamiast pełnego przepisywania,
- interfejs nie rozprasza dodatkowymi funkcjami,
- użytkownik rozumie, że aplikacja służy do szybkiego dyktowania i finalizacji tekstu, a nie do rozmowy z asystentem.

W pierwszej wersji nie zakłada się rozbudowanej analityki produktowej.

## 16. Ryzyka produktowe
- jakość rozpoznawania mowy może być nierówna dla różnych mikrofonów i warunków akustycznych,
- korekta tekstu może czasem być zbyt agresywna albo zbyt zachowawcza,
- użytkownik może oczekiwać pełnej zgodności z każdym stylem mówienia, co nie musi być realne w v1,
- czas przetwarzania lokalnego może wpływać na odbiór produktu przy słabszym sprzęcie.

Ryzyka te nie rozszerzają zakresu v1, ale powinny być uwzględnione przy dalszej specyfikacji technicznej i testach.

## 17. Future considerations
Poza v1 można rozważyć:

- historię lokalnych transkrypcji,
- obsługę wielu języków,
- upload plików audio,
- tryb szybkiego wklejania do aktywnej aplikacji,
- alternatywny model sterowania, np. push-to-talk lub VAD,
- bardziej zaawansowane opcje korekty stylu.

Te elementy nie są częścią tego PRD i nie powinny wpływać na zakres pierwszej implementacji.

## 18. Granice dokumentu
Ten PRD opisuje:

- cel produktu,
- potrzeby użytkownika,
- zakres funkcjonalny wersji pierwszej,
- kryteria akceptacji i oczekiwane zachowanie produktu.

Ten PRD nie opisuje:

- szczegółów architektury technicznej,
- podziału na moduły i pliki,
- kontraktów API,
- planu implementacyjnego milestone'ów,
- szczegółowego doboru zależności.

Te elementy mają zostać doprecyzowane później w `spec.md`, `ROADMAP.md` i `STATUS.md`.
