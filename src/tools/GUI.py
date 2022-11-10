from modules.importer import *
import modules.gui_functions as gf

BASE_DB = 'data\\DB'
FILES_TO_COMPARE = []

GRAPH = None


def main_window_tk():
    root = tk.Tk()
    root.title('Spectra Comparator')
    root.geometry('400x400')
    root.resizable(True, True)
    gf.up_menu(root)
    # create a menu

    #display a graph
    gf.display_graph(root, GRAPH)


    tk.mainloop()


    # display the menu

if __name__ == '__main__':
    main_window_tk()