from modules.importer import *
import modules.gui_functions as gf



def main_window_tk():
    root = tk.Tk()
    root.title('Spectra Comparator')
    root.geometry('530x400')
    root.resizable(True, True)

    file_var = tk.StringVar()
    file_var.set('No file loaded')
    #text box
    if gf.FILE_LOADED:
        file_var.set(gf.WORKING_FILE)
    file_box = tk.Entry(root, textvariable=file_var)
    file_box.grid(row=2, column=1)

    filter_var = tk.StringVar()
    filter_var.set('No filter loaded')
    #text box
    if gf.FILTER_FILE:
        filter_var.set(gf.FILTER_FILE)
    filter_box = tk.Entry(root, textvariable=filter_var)
    filter_box.grid(row=3, column=2)

    load_button = tk.Button(root, text='Load File', command=lambda : gf.select_file(root, False, file_box))
    load_button.grid(row=2, column=0)
    gf.up_menu(root, file_box)
    # create a menu
    gf.limit_data(root)
    
    load_filter_button = tk.Button(root, text='Load Filter', command=lambda : gf.select_filter_file(root, filter_box))
    load_filter_button.grid(row=3, column=0)
    #start button
    start_button = tk.Button(root, text='Start', command=lambda : gf.start(root))
    start_button.grid(row=4, column=0)

    #display button
    display_button = tk.Button(root, text='Display', command=lambda : gf.display_filex(root))
    display_button.grid(row=4, column=1)

    #modyfication button
    mod_button = tk.Button(root, text='Modify noise', command=lambda : gf.modify_enter(root))
    mod_button.grid(row=4, column=2)

    #filter subtraction button
    filter_button = tk.Button(root, text='Filter Subtraction', command=lambda : gf.filter_subtraction(root))
    filter_button.grid(row=5, column=0)

    root.mainloop()



if __name__ == '__main__':
    main_window_tk()