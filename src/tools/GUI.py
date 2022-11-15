from modules.importer import *
import modules.gui_functions as gf

BASE_DB = 'data\\DB'
FILES_TO_COMPARE = []


def main_window_tk():
    root = tk.Tk()
    root.title('Spectra Comparator')
    root.geometry('400x400')
    root.resizable(True, True)

    
    file_var = tk.StringVar()
    file_var.set('No file loaded')
    #text box
    if gf.FILE_LOADED:
        file_var.set(gf.WORKING_FILE)
    file_box = tk.Entry(root, textvariable=file_var)
    file_box.grid(row=2, column=1)

    load_button = tk.Button(root, text='Load File', command=lambda : gf.select_file(root, file_box))
    load_button.grid(row=2, column=0)
    gf.up_menu(root, file_box)
    # create a menu
    gf.limit_data(root)



    root.mainloop()
    #tk.mainloop()


    # display the menu

if __name__ == '__main__':
    main_window_tk()