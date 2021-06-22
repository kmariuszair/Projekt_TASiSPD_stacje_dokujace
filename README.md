# Projekt_TASiSPD_stacje_dokujace
Projekt z TASiSPD

## Intrukcja uruchomienia (na platformie Windows 64-bit):

1) instalacja środowiska Anaconda (https://www.anaconda.com/products/individual#Downloads)
2) dodanie ścieżek do zmiennej środowiskowej, systemowej PATH - "C:\Users\USERNAME\anaconda3" oraz "C:\Users\USERNAME\anaconda3\Scripts"
3) aktywacja shella - "conda init cmd.exe"
4) ponowne uruchomienie shella
5) aktywacja środowiska base (>> conda activate base)
6) doinstalowanie ffmpeg (>> conda install ffmpeg)
7) uruchomienie skryptu z podaną ścieżką do interpretera conda (>> C:\Users\USERNAME\anaconda3\python.exe "sciezka/do/skryptu/main.py")

## Obajśnienia plików konfiguracyjnych
### — details\caseX\robots.dat
Pliki binarne zapisane za pomocją modułu *pickle*. Zawierają słowniki mapujące (string) ID robota na słownik zawierający informacje o nim. 
Pola w słowniku opisującym robota:
'starting_position'     : pozycja startowa w symulacji

'battery_size'          : rozmiar baterii

'starting_battery_level': stan baterii ba początku symulacji

'max_load'              : maksymalne obciążenie robota

'id'                    : ID robota (int)

'size'                  : wymiary robota

'max_loading_speed'     : maksymalna prędkość ładowania

'weight'                : masa własna robota

'power'                 : moc robota

'max_speed'             : maksymalna prędkość

'name'                  : nazwa

'price'                 : cena

'link'                  : link do strony z robotem

### — details\caseX\docks.dat
Analogiczne pliki binarne jak w poprzednim przypadku. Tym razem słowniki zawierają informacje o stacjach dokujących
'position'              : pozycja stacji dokującej przed optymalizacją

'loading_speed'         : prędkość ładowania

'price'                 : cena

'name'                  : nazwa

'link'                  : link do strony ze stacją dokującą

### — maps\caseX\barriers.npy
Plik zapisany za pomocą funkcji *numpy.save*. Zawiera informacje o barierach na mapie. Wartość 1 oznacza brak możliwości poruszania się robota po danej komórce 
oraz brak możliwości ustawienia w danym miejscu stacji dokującej. Wartość 2 oznacza, że w danym miejscu może poruszać się robot, 
ale nie można postawić stacji dokującej. Wartość 0 oznacza swobodę za równo w poruszaniu się robotem jak i ustawiania stacji dokującej.

### — maps\caseX\init_docking_stations.npy
Plik zapisany za pomocą funkcji *numpy.save*. Zawiera informacje o pozycji oraz prędkości ładowania stacji dokujących. Nie jest używany, gdy korzysta się z 
konfiguracji zapisanej w pliku binarnym *docks.dat*.

### — logs\caseX\subcase1a\caseX_D_docks.log
Plik tekstowy z logami przebiegu symulacji oraz optymalizacji dla danej liczby D stacji dokujących. Kolejne wartości D oznaczają zwiększanie liczby stacji dokujących 
na mapie. Jest to element badania wpływu ich ilości na potencjalny zysk.

### — plots\caseX\subcase1a\docks_no_D
Pliki graficzne oraz animacje uzyskane w trakcie symulacji pracy robotów oraz optymalizacji. Animacja z ruchem robotów oraz stacjami dokującymi jest rysowana dla
ruchu robotów przed optymalizacją pozycji stacji, a położenie stacji już po tej optymalizacji. D oznacza liczbę stacji dokujących na mapie dla danego przypadku.

### — settings\test_cases\caseX.json
Pliki JSON z kolejnymi scenariuszami testowymi
```json
{
    "main": [
        {
            "path_to_client_map":         "ścieżka do mapy z obciążeniem ruchem robotów, przy symulacji pole nieaktywne",
            "map_shape":                  "wymiar mapy",
            "clients_number":             "liczba klientów (suma obciążeń komórek), pole nieaktywne w przypadku symulacji",
            "max_clients_number_in_cell": "maksymalne obciążenie ruchem komórek, nieaktywne w przypadku symulacji",
            "n_max":                      "parametr Tabu-Search - maksymalna liczba stacji dokujących",
            "p_max":                      "parametr Tabu-Search - maksymalna ilość klientów wokół stacji dokującej",
            "d_max":                      "parametr Tabu-Search - maksymalna odległość stacji dokującej od klienta",
            "r":                          "parametr Tabu-Search - promień sąsiedztwa",
            "min_time_in_tl":             "parametr Tabu-Search - minimalny czas na liście tabu",
            "min_time_in_lt_tl":          "parametr Tabu-Search - minimalny czas na długoterminowej liście tabu",
            "time_lim":                   "maksymalny czas trwanie obliczeń optymalizacyjnych",
            "log_path":                   "ścieżka do zapisywania logów",
            "iteration_lim":              "maksymalna ilość iteracji algorytmu optymalizującego",
            "starting_solution":          "początkowe ułożenie stacji dokujących",
            "dynamic_neighborhood":       "parametr Tabu-Search - dynamiczne sąsiedztwo",
        }
    ],
    "DataCollectorPlotter": [
        {
            "allow_generate_dynamic_map_animation":   "dynamiczna animacja",
            "connect_dots_on_plot":                   "łączenie kropek na wykresach",
            "show_plot_of_Q_a":                       "pokaż wykres funkcji kosztu w danej iteracji algorytmu optymalizującego",
            "show_map_of_best_plt_position":          "pokaż mapę optymalnych pozycji stacji dokujących",
            "show_plot_of_total_taboo_list_elements": "pokaż wykres liczby wszystkich elementów na liście tabu",
            "show_map_of_total_moves":                "pokaż mapę ruchów",
            "show_plot_long_term_tabu_list_elements": "pokaż wykres liczby elementów na długoterminowej liście tabu w zależności od iteracji",
            "show_plot_elems_in_nei":                 "pokaż ilość przeszukanych elementów z sąsiedztwa (przydatne przy dynamicznym sąsiedztwie)"
        }
    ],
    "show_3D_client_map": [
        {
            "generate_3D_rotate_GIF": "pokaż GIFa 3D",
            "generate_2D":            "pokaż mapę 2D",
            "save_to_gif":            "zapisz do GIF"
        }
        ],
    "PlotSaver": [
        {
            "save_plot_to_file": "zapisuj wykresy i animacje",
            "path_to_save_plot": "ścieżka do zapisywania elementów"
        }
    ],
    "RobotsSimulation": [
        {
            "robots_number":        "liczba robotów",
            "sim_time":             "czas symulacji (iteracje)",
            "robots_settings":      "ścieżka do pliku binarnego z ustawieniami robotów",
            "docks_settings":       "ścieżka do pliku binarnego z ustawieniami stacji dokujących",
            "barriers_map":         "mapa przeszkód",
            "docking_stations_map": "mapa stacji dokujących (jeśli nie podano pliku binarnego z ustawieniami stacji)",
            "docking_stations_no":  "liczba stacji dokujących",
            "frame":                "maksymalna odległość stacji dokujących od ścian",
            "max_investment_cost":  "maksymalny koszt inwestycji",
            "max_maintenance_cost": "maksymalny koszt utrzymania instalacji"
        }
    ]
}
```
