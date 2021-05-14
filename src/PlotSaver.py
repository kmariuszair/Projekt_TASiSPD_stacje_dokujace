import matplotlib.pyplot as plt
from matplotlib import animation
from src.DataCollectorPlotter import setting_menager
from src.FileMenager import is_path_to_file_exists, generate_path_to_file
"""
    Jest to zbiór funckji odpowiedzialnych za zapis uzyskanych wykresów i animacji do plików.
    Zapis i ścieżka zapisu jest zdefiniowana w pliku konfiguracyjnym.
"""


def save_plot_to_file(plt_to_save: plt.plot, file_name):
    data = setting_menager.get_PlotSaver_settings()
    if data['save_plot_to_file']:
        if data['path_to_save_plot'] is None or data['path_to_save_plot'] == '':
            path_with_file_name = 'plots/' + file_name + '.png'
        else:
            path_with_file_name = data['path_to_save_plot'] + '/' + file_name + '.png'
        if not is_path_to_file_exists(path_with_file_name):
            generate_path_to_file(path_with_file_name)
        plt_to_save.savefig(path_with_file_name)


def save_anim_to_file(anim_to_save: animation.FuncAnimation, file_name):
    data = setting_menager.get_PlotSaver_settings()
    if data['save_plot_to_file']:
        if data['path_to_save_plot'] is None or data['path_to_save_plot'] == '':
            path_with_file_name = 'plots/' + file_name
        else:
            path_with_file_name = data['path_to_save_plot'] + '/' + file_name
        if not is_path_to_file_exists(path_with_file_name):
            generate_path_to_file(path_with_file_name)
        anim_to_save.save(path_with_file_name)