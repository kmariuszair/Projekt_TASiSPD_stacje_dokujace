import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib import animation
from typing import Dict
from src.SettingMenager import setting_menager
from src.PlotSaver import save_plot_to_file, save_anim_to_file
"""
    Funkcja służaca do reprezentacji graficznej macierzy klientów 
    !!!   UWAGA   !!!
    Aby użyć opcji generowania animacji na podstawie mapy klientów należy zainstalować moduł ffmpeg
    Inaczej program się zawiesi 
    TODO: ZAINSTALOWAC MODUL FFMPEG
"""


def plot_client_map(_client_map:np.array, max_clients_number_in_cell: int,
                    generate_3D_rotate_GIF: bool = False, generate_2D:bool = False):
    """

    :param client_map: Mapa rozmieszczenia klientów
    :param max_clients_number_in_cell: Maksymalna ilość klientów jaka może byc w danej komórce
    :param generate_3D_rotate_GIF: Parametr służący do utworzenia animowanego modelu mapy klientów
    :param generate_2D: Parametr służący do reprezentacji mapy klientów w postaci 2D
    :return:
    """
    client_map = np.copy(_client_map)
    data = setting_menager.get_plot_client_map_settings()
    generate_3D_rotate_GIF = data['generate_3D_rotate_GIF']
    generate_2D = data['generate_2D']
    save_to_gif = data['save_to_gif']
    if generate_2D:
        fig = plt.figure(figsize=(16, 12))
        ax = fig.add_subplot(111)
        im = ax.imshow(client_map, origin='lower', interpolation='None', cmap='Reds')
        plt.xlabel('Pozycja osi Y')
        plt.ylabel('Pozycja osi X')
        plt.title('Ilość klientów w danym miejscu')
        size = client_map.shape
        for (j, i), label in np.ndenumerate(client_map):
            ax.text(j, i, label, ha='center', va='center')
        plt.xticks(range(0, size[1]))
        plt.yticks(range(0, size[0]))
        fig.colorbar(im)
        save_plot_to_file(plt, 'client_map')
        plt.show()
    else:
        x_size = 0.5
        y_size = 0.5
        fig = plt.figure()
        ax = plt.axes(projection="3d")
        map_size = client_map.shape
        cmap = cm.get_cmap('viridis', max_clients_number_in_cell)
        for x in range(0, map_size[0]):
            for y in range(0, map_size[1]):
                ax.bar3d(x, y, 0, x_size, y_size, client_map[x][y], color=cmap.colors[client_map[x][y]])
        plt.gca().invert_xaxis()
        plt.title('Rozmieszczenie klientów na mapie')
        ax.set_xlabel('Pozycja X')
        ax.set_ylabel('Pozycja Y')
        ax.set_zlabel('Ilość klientów na \ndanym obszarze')
        save_plot_to_file(plt, 'client_map')
        plt.show()
        if generate_3D_rotate_GIF:
            def animate(i):
                ax.view_init(elev=10., azim=i)
                return fig,
            # Utwórz animację na podstawie mapy
            anim = animation.FuncAnimation(fig, animate, frames=360, interval=20, blit=True)
            # Zapisz animację do pliku pod formatem GIF
            if save_to_gif:
                save_anim_to_file(anim, 'client_map.gif')
            else:
                save_anim_to_file(anim, 'client_map.mp4')


class DataCollectorPlotter:
    """
    Klasa zawierająca funkcjonalności związane ze zbieraniem informacji o przebiegu działania algorytmu
    oraz z ich reprezentacją graficzną.
    """
    def __init__(self, client_map: np.array = None,
                 load_setting_from_file: bool = False,
                 generate_dynamic_map_of_total_moves= True,
                 connect_dots_on_plot= True,
                 show_plot_of_Q_a= True,
                 show_map_of_best_plt_position=True,
                 show_plot_of_total_taboo_list_elements=True,
                 show_map_of_total_moves=True,
                 show_plot_long_term_tabu_list_elements=True,
                 show_plot_elems_in_nei=True,
                 show_plot_av_cadence= True,
                 show_plot_av_long_cadence= True,
                 show_plot_elems_in_short_tabu= True,
                 show_plot_elems_in_long_tabu = True
                ):
        """Inicjalizacja parametrów klasy oraz zmiennnych"""
        self.__generate_3D_plots = False
        self.__iteration_count = 0
        self.__x_a_list = []
        self.__Q_a_list = []
        self.__Tabu_list = []
        self.__long_term_Tabu_list = []
        self.__av_cadence = []
        self.__av_long_cadence = []
        self.__elems_in_short_tabu = []
        self.__elems_in_long_tabu = []
        self.__elems_in_nei_list = []
        self.__min_Q_a_pos = 0
        self.__client_map = client_map
        """
        Parametry dopowiedzialne za generoanie odpowiednich wykresów i animacji
        Jeśli nie jest włączone wczytywanie konfiguracji z pliku wtedy wczytaj domyślne
        """
        if load_setting_from_file:
            data = setting_menager.get_DataCollector_settings()
            self.__generate_dynamic_map_of_total_moves = data['allow_generate_dynamic_map_animation']
            self.__connect_dots_on_plot = data['connect_dots_on_plot']
            self.__show_plot_of_Q_a = data['show_plot_of_Q_a']
            self.__show_map_of_best_plt_position = data['show_map_of_best_plt_position']
            self.__show_plot_of_total_taboo_list_elements = data['show_plot_of_total_taboo_list_elements']
            self.__show_map_of_total_moves = data['show_map_of_total_moves']
            self.__show_plot_long_term_tabu_list_elements = data['show_plot_long_term_tabu_list_elements']
            self.__show_plot_elems_in_nei = data['show_plot_elems_in_nei']
            self.__show_plot_av_cadence = show_plot_av_cadence
            self.__show_plot_av_long_cadence = show_plot_av_long_cadence
            self.__show_plot_elems_in_short_tabu = show_plot_elems_in_short_tabu
            self.__show_show_plot_elems_in_long_tabu = show_plot_elems_in_long_tabu
        else:
            self.__generate_dynamic_map_of_total_moves = generate_dynamic_map_of_total_moves
            self.__connect_dots_on_plot = connect_dots_on_plot
            self.__show_plot_of_Q_a = show_plot_of_Q_a
            self.__show_map_of_best_plt_position = show_map_of_best_plt_position
            self.__show_plot_of_total_taboo_list_elements = show_plot_of_total_taboo_list_elements
            self.__show_map_of_total_moves = show_map_of_total_moves
            self.__show_plot_long_term_tabu_list_elements = show_plot_long_term_tabu_list_elements
            self.__show_plot_elems_in_nei = show_plot_elems_in_nei
            self.__show_plot_av_cadence = show_plot_av_cadence
            self.__show_plot_av_long_cadence = show_plot_av_long_cadence
            self.__show_plot_elems_in_short_tabu = show_plot_elems_in_short_tabu
            self.__show_show_plot_elems_in_long_tabu = show_plot_elems_in_long_tabu

    def collect_data(self, x_a_itr: np.array, Q_a_itr: float, tabu_list: np.array,
                     long_term_tabu_list: np.array, elems_in_nei: int,
                     av_cadence: float, av_long_cadence: float,
                     elems_in_short_tabu: float, elems_in_long_tabu: float
                     ):
        """
        Funkcja zbierająca odpowiednie dane do reprezentacji przebiegu algorytmu.
        Są to paramentry algorytmu w danej iteracji
        :param x_a_itr: Bieżące rozmieszczenie stacji dokujących
        :param Q_a_itr: Funkcja kosztu w
        :param tabu_list: Krótkoterminowa lista tabu
        :param long_term_tabu_list: Długoterminowa lista tabu
        :param elems_in_nei: Ilość elementów przeanalizowana w danej iteracji
        :param av_cadence: "Średni wiek" zabronienia z listy krótkoterminowej tabu search
        :param av_long_cadence: "Średni wiek" zabronienia z listy długoterminowej tabu search
        :param elems_in_short_tabu: Ilość zabronień wynikająca z listy krótkoterminowej
        :param elems_in_long_tabu: Ilość zabronień wynikająca z listy długoterminowej
        :return:
        """
        self.__x_a_list.append(np.copy(x_a_itr.T))
        self.__Q_a_list.append(Q_a_itr)
        self.__Tabu_list.append(np.copy(tabu_list).T)
        self.__long_term_Tabu_list.append(np.copy(long_term_tabu_list).T)
        self.__av_cadence.append(av_cadence)
        self.__av_long_cadence.append(av_long_cadence)
        self.__elems_in_short_tabu.append(elems_in_short_tabu)
        self.__elems_in_long_tabu.append(elems_in_long_tabu)
        self.__elems_in_nei_list.append(np.copy(elems_in_nei))
        if Q_a_itr < self.__Q_a_list[self.__min_Q_a_pos]:
            self.__min_Q_a_pos = self.__iteration_count
        self.__iteration_count = self.__iteration_count + 1

    def plot_data(self):
        """
        Funkcja rysująca odpowiednie wykresy.
        Wywołuje odpowiednie metody klasy odpowiedzialne ze geneorwanie poszczególnych wykresów i analiz.
        Każdy wykres można włązyć/wyłączyć poprzez ustawienia klasy lub plik konfiguracyjny.
        !!! Wyłączenie reprezentacji graficznej wykresu, wyłącza zapis danego wykresu do pliku !!!
        :return:
        """
        if self.__show_plot_of_Q_a:  # Wykres wartości fukncji celu w danej iteracji
            self.__plot_Q_a()
        if self.__show_map_of_best_plt_position:  # Mapa optymalnego rozmieszczenia stacji dokujących
            self.__plot_plt_map()
        if self.__show_plot_of_total_taboo_list_elements:  # Wykres ilości elementów na liście tabu w danej itracji
            self.__plot_tabu_list_elements()
        if self.__show_plot_long_term_tabu_list_elements:  # Wykres ilości elementów na długoterminowej liście tabu
            self.__plot_long_term_tabu_list_elements()
        if self.__show_plot_av_cadence:     # Wykres "średni wiek" zabronienia (średnio ile iteracji wstecz było dodane zabronienie z listy krótk.)
            self.__plot_av_cadence()
        if self.__show_plot_av_long_cadence: # Wykres "średni wiek" zabronienia (średnio ile iteracji wstecz było dodane zabronienie z długo. term.)
            self.__plot_av_long_cadence()
        if self.__elems_in_short_tabu:  # Wykres ilości zabronień wynikająca z listy krótkoterminowej
            self.__plot_elems_in_short_tabu()
        if self.__elems_in_long_tabu:   #Wykres ilości zabronień wynikająca z listy długoterminowej
            self.__plot_elems_in_long_tabu()
        if self.__show_plot_elems_in_nei:   # Wykres ilości przeszukanych elementów w sąsiedztwie w danej iteracji
            self.__plot_elems_in_nei()
        if self.__show_map_of_total_moves:  # Mapa wszystkich ruchów wykonanych podczas działania algorytmu
            self.__generate_plot_of_moves()
        if self.__generate_dynamic_map_of_total_moves:  # Animacja przemieszczeń stacji dokujących podczas działania algorytmu
            self.__generate_dynamic_map_of_moves()

    def __plot_Q_a(self):
        """
        Funkcja reprezentująca wykres funkcji celu w danej iteracji
        """
        fig = plt.figure()
        x = np.linspace(1, self.__iteration_count, self.__iteration_count, endpoint=True)
        plt.plot(x, self.__Q_a_list, 'bo')
        if self.__connect_dots_on_plot:
            plt.plot(x, self.__Q_a_list)
        plt.plot(self.__min_Q_a_pos+1, self.__Q_a_list[self.__min_Q_a_pos], 'ro')
        plt.xlabel('Numer iteracji')
        plt.ylabel('Wartośc funkcji celu')
        plt.title('Wykres wartości funkcji celu w danej iteracji')
        save_plot_to_file(plt, 'Wartosc_funkcji')
        plt.show()

    def __plot_plt_map(self):
        """
        Funkcja reprezentująca optymalne rozmieszczenie stacji dokujących
        """
        if self.__client_map is None:
            fig = plt.figure()
            ax = fig.add_subplot(111)
            x_a = self.__x_a_list[self.__min_Q_a_pos]
            im = ax.imshow(x_a, origin='lower', interpolation='None', cmap='Reds')
            plt.xlabel('Pozycja osi Y')
            plt.ylabel('Pozycja osi X')
            plt.title('Optymalna pozycja stacji dokujących')
            save_plot_to_file(plt, 'Optymalna_pozycja_stacji_dokujacych')
            plt.show()
        else:
            fig = plt.figure()
            ax = fig.add_subplot(111)
            x_a = self.__x_a_list[self.__min_Q_a_pos]
            im = ax.imshow(self.__client_map, origin='lower', interpolation='None', cmap='viridis')
            x_size = x_a.shape[0]
            y_size = x_a.shape[1]
            for x in range(0, x_size):
                for y in range(0, y_size):
                    if x_a[x][y] == 1:
                        plt.plot(x, y, 'ro')
            plt.xlabel('Pozycja osi Y')
            plt.ylabel('Pozycja osi X')
            plt.title('Optymalna pozycja stacji dokujących')
            fig.colorbar(im)
            save_plot_to_file(plt, 'Optymalna_pozycja_stacji_dokujacych')
            plt.show()

    def __generate_dynamic_map_of_moves(self):
        """
        Podczas generacji dynamicznej mapy pojawia się błąd na początku filmu, jednak po przewinięciu filmu od
        połowy dany błąd znika. Może być on wynikać bezpośrednio z działania biblioteki odpowiedzialnej za generowanie
        filmu lub jest to błąd z funkcji renderującej.
        Wystarczy zmienić odtwarzać na VLC i problem znika.
        """
        if self.__client_map is None:
            raise ValueError('Nie można wygenerować zmian stacji dokujących bez mapy klientów!')
        x_size = self.__client_map.shape[1]
        y_size = self.__client_map.shape[0]
        frame_offset = 3
        fig, ax = plt.subplots()
        x_a_copy = np.copy(self.__x_a_list)
        """
            Funkcja wewnętrza służąca do generowania klatki animacjia. 
            Animuje ona ruch wykonany przez stacje dokujące w danej iteracji.
        """
        def animate(frame):
            if frame >= self.__iteration_count:
                frame = self.__iteration_count - 1
            plt.clf()
            im = plt.imshow(self.__client_map, origin='lower', interpolation='None', cmap='viridis')
            x_a = x_a_copy[frame]
            for x in range(0, x_size):
                for y in range(0, y_size):
                    if x_a[x][y] == 1:
                        plt.plot(x, y, 'ro')
            # Utwórz macierz ruchu i na jej podstawie narysuj strzałki
            if frame > 0:
                move = x_a_copy[frame] - x_a_copy[frame - 1]
                pos_arrow_head = np.where(move == 1)
                x_arrow_head = pos_arrow_head[0][0]
                y_arrow_head = pos_arrow_head[1][0]
                pos_arrow_begin = np.where(move == -1)
                x_arrow_begin = pos_arrow_begin[0][0]
                y_arrow_begin = pos_arrow_begin[1][0]
                dx = x_arrow_head - x_arrow_begin
                dy = y_arrow_head - y_arrow_begin
                ax.annotate("", xy=(0.5, 0.5), xytext=(0, 0), arrowprops = dict(arrowstyle="->"))
                plt.arrow(x_arrow_begin, y_arrow_begin, dx, dy, color='white', width=0.005,
                          length_includes_head=True, head_width=0.1, head_length=0.15)
                plt.scatter(x_arrow_begin, y_arrow_begin, facecolors='none', edgecolors='white')
            plt.xlabel('Pozycja osi Y')
            plt.ylabel('Pozycja osi X')
            if frame == self.__min_Q_a_pos:
                title = 'Optymalna pozycja stacji dokujących dla iteracji {}\n Funkcja celu: {}'.format(frame + 1, self.__Q_a_list[self.__min_Q_a_pos])
                plt.title(title, color='r')
            else:
                title = 'Pozycja stacji dokujących dla iteracji {}\n Funkcja celu: {}'.format(frame + 1, self.__Q_a_list[frame])
                plt.title(title)

            plt.colorbar(im)
            return fig,

        # Utwórz animację na podstawie mapy
        # Offset ma na celu uniknięcie pewnego buga podczas generacji
        anim = animation.FuncAnimation(fig, animate, frames=self.__iteration_count + frame_offset,
                                       interval=250, blit=True)
        # Zapisz animację do pliku pod formatem mp4
        save_anim_to_file(anim, 'dynamic_plt.mp4')

    def __generate_plot_of_moves(self):
        """
        Funkcja służąca do wygenerowania mapy wszystkich ruchów jakie miały miejsce podczas działania algorytmu
        :return:
        """
        if self.__client_map is None:
            raise ValueError('Nie można wygenerować zmian stacji dokujących bez mapy klientów!')
        x_size = self.__client_map.shape[1]
        y_size = self.__client_map.shape[0]
        fig, ax = plt.subplots()
        im = plt.imshow(self.__client_map, origin='lower', interpolation='None', cmap='viridis')
        x_a_copy = self.__x_a_list
        for itr in range(1, self.__iteration_count):
            # Utwórz macierz ruchu i na jej podstawie narysuj strzałki
            move = x_a_copy[itr] - x_a_copy[itr - 1]
            pos_arrow_head = np.where(move == 1)
            x_arrow_head = pos_arrow_head[0][0]
            y_arrow_head = pos_arrow_head[1][0]
            pos_arrow_begin = np.where(move == -1)
            x_arrow_begin = pos_arrow_begin[0][0]
            y_arrow_begin = pos_arrow_begin[1][0]
            dx = x_arrow_head - x_arrow_begin
            dy = y_arrow_head - y_arrow_begin
            ax.annotate("", xy=(0.5, 0.5), xytext=(0, 0), arrowprops = dict(arrowstyle="->"))
            plt.arrow(x_arrow_begin, y_arrow_begin, dx, dy, color='white', width=0.005,
                      length_includes_head=True, head_width=0.1, head_length=0.15)
            plt.scatter(x_arrow_begin, y_arrow_begin, facecolors='none', edgecolors='white')
        # Zaznaczenie finalnej pozycji stacji dokujących
        x_a = x_a_copy[self.__iteration_count - 1]
        for x in range(0, x_size):
            for y in range(0, y_size):
                if x_a[x][y] == 1:
                    plt.plot(x, y, 'ro')
        plt.xlabel('Pozycja osi Y')
        plt.ylabel('Pozycja osi X')
        title = 'Mapa przemieszczen podczas działania algorytmu'
        plt.title(title)
        plt.colorbar(im)
        save_plot_to_file(plt, 'Mapa_przemieszczen_stacji_dokujacych')
        plt.show()

    def __plot_tabu_list_elements(self):
        """
        Funkcja służąca do generacji wykresu ilości elementów na liście Tabu
        """
        tabu_list_elements = []
        for tabu in self.__Tabu_list:
            tabu_list_elements.append(np.count_nonzero(tabu))
        fig = plt.figure()
        x = np.linspace(1, self.__iteration_count, self.__iteration_count, endpoint=True)
        plt.plot(x, tabu_list_elements, 'bo')
        if self.__connect_dots_on_plot:
            plt.plot(x, tabu_list_elements)
        plt.xlabel('Numer iteracji')
        plt.ylabel('Ilość elementów na liście tabu')
        plt.title('Ilość elementów na liście tabu w danej iteracji')
        save_plot_to_file(plt, 'Ilosc_elementow_tabo_list')
        plt.show()

    def __plot_long_term_tabu_list_elements(self):
        """
        Funkcja służąca do generacji wykresu ilości elementów na liście Tabu
        """
        tabu_list_elements = []
        for tabu in self.__long_term_Tabu_list:
            tabu_list_elements.append(np.count_nonzero(tabu))
        fig = plt.figure()
        x = np.linspace(1, self.__iteration_count, self.__iteration_count, endpoint=True)
        plt.plot(x, tabu_list_elements, 'ro')
        if self.__connect_dots_on_plot:
            plt.plot(x, tabu_list_elements, 'r')
        plt.xlabel('Numer iteracji')
        plt.ylabel('Ilość elementów na długoterminowej liście tabu')
        plt.title('Ilość elementów na długoterminowej liście tabu w danej iteracji')
        save_plot_to_file(plt, 'Ilosc_elementow_dlugoterminowej_tabo_list')
        plt.show()

    def __plot_av_cadence(self):
        """
            Generowanie wykresu średniego wieku zabronien na liście Tabu krótkoterminowej
        """
        x = np.linspace(1, self.__iteration_count, self.__iteration_count, endpoint=True)
        plt.plot(x, self.__av_cadence, 'yo')
        if self.__connect_dots_on_plot:
            plt.plot(x, self.__av_cadence, 'y')
        plt.xlabel('Numer iteracji')
        plt.ylabel('Średni wiek zabronienia krótoterminowej listy tabu ')
        plt.title('Średni wiek zabronienia krótoterminowej listy tabu w danej iteracji')
        save_plot_to_file(plt, 'Sredni_wiek_elementow_krototerminowej_tabo_list')
        plt.show()

    def __plot_av_long_cadence(self):
        """
            Generowanie wykresu średniego wieku zabronien na liście Tabu długoterminowej
        """
        x = np.linspace(1, self.__iteration_count, self.__iteration_count, endpoint=True)
        plt.plot(x, self.__av_long_cadence, 'mo')
        if self.__connect_dots_on_plot:
            plt.plot(x, self.__av_long_cadence, 'm')
        plt.xlabel('Numer iteracji')
        plt.ylabel('Średni wiek zabronienia długoterminowej listy tabu ')
        plt.title('Średni wiek zabronienia długoterminowej listy tabu w danej iteracji')
        save_plot_to_file(plt, 'Sredni_wiek_elementow_dlugoterminowej_tabo_list')
        plt.show()

    def __plot_elems_in_short_tabu(self):
        """
            Generowanie wykresu ilości zabronień wynikająca z listy krótkoterminowej
        """
        x = np.linspace(1, self.__iteration_count, self.__iteration_count, endpoint=True)
        plt.plot(x, self.__elems_in_short_tabu, 'co')
        if self.__connect_dots_on_plot:
            plt.plot(x, self.__elems_in_short_tabu, 'c')
        plt.xlabel('Numer iteracji')
        plt.ylabel('Ilość zabronień wynikająca z listy krótkoterminowej ')
        plt.title('Ilość zabronień wynikająca z listy krótkoterminowej w danej iteracji')
        save_plot_to_file(plt, 'Ilosc_zabronien_krototerminowej_tabo_list')
        plt.show()

    def __plot_elems_in_long_tabu(self):
        """
            Generowanie wykresu ilości zabronień wynikająca z listy długoterminowej
        """
        x = np.linspace(1, self.__iteration_count, self.__iteration_count, endpoint=True)
        plt.plot(x, self.__elems_in_long_tabu, 'co')
        if self.__connect_dots_on_plot:
            plt.plot(x, self.__elems_in_long_tabu, 'c')
        plt.xlabel('Numer iteracji')
        plt.ylabel('Ilość zabronień wynikająca z listy długoterminowej ')
        plt.title('Ilość zabronień wynikająca z listy długoterminowej w danej iteracji')
        save_plot_to_file(plt, 'Ilosc_zabronien_dlugoterminowej_tabo_list')
        plt.show()

    def __plot_elems_in_nei(self):
        """"
            Wykres ilości przeszukanych elementów w sąsiedztwie w danej iteracji
        """
        x = np.linspace(1, self.__iteration_count, self.__iteration_count, endpoint=True)
        plt.plot(x, self.__elems_in_nei_list, 'go')
        if self.__connect_dots_on_plot:
            plt.plot(x, self.__elems_in_nei_list, 'g')
        plt.xlabel('Numer iteracji')
        plt.ylabel('Ilość elementów przeszukanych w sąsiedztwie')
        plt.title('Ilość elementów przeszukanych w sąsiedztwie w danej iteracji')
        save_plot_to_file(plt, 'Ilosc_przeszukanych_elementow_w_sasiedztwie')
        plt.show()


def generate_plot_of_telemetry(telemetry_data: Dict):
    """
        Funkcja służy do utworzenia wykresu przedstawiającego dane zebrane przez telemetrię
    """
    fig, ax = plt.subplots(figsize=(16, 9))
    # Sortowanie według łacznego czasu wykonania
    telemetry_data = dict(sorted(telemetry_data.items(), key=lambda x: x[1], reverse=True))
    name_of_function = telemetry_data.keys()
    total_time = telemetry_data.values()
    # Generowanie wykresu
    y_pos = np.arange(len(name_of_function))
    ax.barh(y_pos, total_time, align='center')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(name_of_function)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Łączny czas wykonania w sekundach')
    ax.set_title('Czas wykonania poszczególnych funkcji algorytmu')
    save_plot_to_file(plt, 'telemetria')
    plt.show()

