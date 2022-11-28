from modules.importer import *
from modules.basic_functions import *
import comarator as comp

WORKING_FILE = None
OPEN_CONFIG = False
OPEN_LOAD = False
OPEN_SAVE = False
OPEN_LOADING = False
X, Y = None, None
FILE_LOADED = False
MAX_MIN = [None, None]
MAX_MIN_EX = [None, None]

RESULTS = None

BASE_DIR = os.getcwd()

CONF_DIPLAY = {
    "fluo_filter" : False,
    "Normalization" : "MinMax",
    "Filter" : False,
}

USE_INDEXES = {"NORM_CORR": False, 
                "CONV": False, 
                "FFT_CONV": False, 
                "HQI": False,
                "DISCR" : False,
                "CORRE" : False,
                "DIFF" : False,
                "Normalization" : "Stat",
                "List_results" : 10,
                "Filter": False,
                "Fluo_filter": False,
                "DB" : None,
                }

LIST_BOOL = ["NORM_CORR", "CONV", "FFT_CONV", "HQI", "DISCR", "CORRE", "DIFF", "Filter"]

def hello():
    print('hello!')

def clear_checks(data):
    for check in data:
        if isinstance(check, tk.Checkbutton):
            check.deselect()
        if isinstance(check, tk.Radiobutton):
            check.deselect()
        if isinstance(check, tk.Spinbox):
            check.delete(0, 10)

def use_config(root, data):
    global OPEN_CONFIG
    global USE_INDEXES
    USE_INDEXES["NORM_CORR"] = data[0].get()
    USE_INDEXES["CONV"] = data[1].get()
    USE_INDEXES["FFT_CONV"] = data[2].get()
    USE_INDEXES["HQI"] = data[3].get()
    USE_INDEXES["DISCR"] = data[4].get()
    USE_INDEXES["CORRE"] = data[5].get()
    USE_INDEXES["DIFF"] = data[6].get()
    USE_INDEXES["Normalization"] = data[7].get()
    USE_INDEXES["List_results"] = data[8].get()
    USE_INDEXES["Filter"] = data[9].get()  
    USE_INDEXES["Fluo_filter"] = data[10].get()
    USE_INDEXES["DB"] = data[11].get()  
    root.destroy()
    OPEN_CONFIG = False
    #print the value of the checks

def save_configuration(data):
    global OPEN_CONFIG, OPEN_SAVE
    global USE_INDEXES
    OPEN_SAVE = True
    USE_INDEXES["NORM_CORR"] = data[0].get()
    USE_INDEXES["CONV"] = data[1].get()
    USE_INDEXES["FFT_CONV"] = data[2].get()
    USE_INDEXES["HQI"] = data[3].get()
    USE_INDEXES["DISCR"] = data[4].get()
    USE_INDEXES["CORRE"] = data[5].get()
    USE_INDEXES["DIFF"] = data[6].get()
    USE_INDEXES["Normalization"] = data[7].get()
    USE_INDEXES["List_results"] = data[8].get()
    USE_INDEXES["Filter"] = data[9].get()   
    USE_INDEXES["DB"] = data[10].get()

    #open a path to save the configuration
    path = filedialog.asksaveasfilename(initialdir = BASE_DIR, title = "Select file",filetypes = (("cnf files","*.cnf"),("all files","*.*"))) 
    if path:
        with open(path + '.cnf', 'w') as file:
            file.write(str(USE_INDEXES))
    OPEN_SAVE = False
    #print the value of the checks

def error_message(root, message, title = 'Error'):
    top = tk.Toplevel(root)
    top.title(title)
    top.geometry('300x100')
    top.resizable(True, True)
    error = tk.Label(top, text=message)
    error.pack()
    error.grid(row=0, column=0)

def load_configuration(top, root):
    global USE_INDEXES
    global OPEN_CONFIG
    path = filedialog.askopenfilename(initialdir = BASE_DIR, title = "Select file",filetypes = (("cnf files","*.cnf"),("all files","*.*")))
    all_good = True
    if path:
        with open(path, 'r') as file:
            content = file.read()
        content = content.replace("{", "").replace("}", "").replace(' ', '').replace("'", "").split(',')
        for el in content:
            if el:
                eli = el.split(":")
                if eli[0] not in USE_INDEXES.keys():
                    all_good = False
                    break
        if not all_good:
            error_message(root, "The configuration file is not valid")
            return
        for element in content:
            if element:
                print(element)
                element = element.split(":")
                if element[0] in LIST_BOOL:
                    USE_INDEXES[element[0]] = element[1] == '1'
                elif element[1].isdigit():
                    USE_INDEXES[element[0]] = int(element[1])
                else:
                    USE_INDEXES[element[0]] = element[1]

    else:
        error_message(root, "The configuration file is not valid")
    root.update()
    top.destroy()
    OPEN_CONFIG = False
    configuration_window(root)


def configuration_window(root):
    global OPEN_CONFIG
    OPEN_CONFIG = True
    top = tk.Toplevel(root)
    top.title('Configuration')
    top.geometry('400x400')
    top.resizable(True, True)

    check_norm_corr_var = tk.IntVar(value = USE_INDEXES["NORM_CORR"])
    check_conv_var = tk.IntVar(value = USE_INDEXES["CONV"])
    check_fft_conv_var = tk.IntVar(value = USE_INDEXES["FFT_CONV"])
    check_hqi_var = tk.IntVar(value = USE_INDEXES["HQI"])
    check_discr_var = tk.IntVar(value = USE_INDEXES["DISCR"])
    check_corre_var = tk.IntVar(value = USE_INDEXES["CORRE"])
    check_diff_var = tk.IntVar(value = USE_INDEXES["DIFF"])
    normalization_var = tk.StringVar(value = USE_INDEXES["Normalization"])
    list_results_var = tk.IntVar(value = USE_INDEXES["List_results"])
    filter_var = tk.IntVar(value = USE_INDEXES["Filter"])
    fluo_filter_var = tk.IntVar(value = USE_INDEXES["Fluo_filter"])
    db_var = tk.StringVar(value = USE_INDEXES["DB"])

    # check boxes
    check_norm_corr = tk.Checkbutton(top, text='Normalised Correlation')
    check_norm_corr.grid(row=0, column=0, sticky='w')
    check_norm_corr.config(variable=check_norm_corr_var)
    if USE_INDEXES["NORM_CORR"]:
        check_norm_corr.select()
    

    check_conv = tk.Checkbutton(top, text='Convolution')
    check_conv.grid(row=1, column=0, sticky='w')
    check_conv.config(variable=check_conv_var)
    if USE_INDEXES["CONV"]:
        check_conv.select()

    check_fft_conv = tk.Checkbutton(top, text='FFT Convolution')
    check_fft_conv.grid(row=2, column=0, sticky='w')
    check_fft_conv.config(variable=check_fft_conv_var)
    if USE_INDEXES["FFT_CONV"]:
        check_fft_conv.select()

    check_hqi = tk.Checkbutton(top, text='Hit Quality Index')
    check_hqi.grid(row=3, column=0, sticky='w')
    check_hqi.config(variable=check_hqi_var)
    if USE_INDEXES["HQI"]:
        check_hqi.select()

    check_discr = tk.Checkbutton(top, text='Discrete Wavelet Transform')
    check_discr.grid(row=4, column=0, sticky='w')
    check_discr.config(variable=check_discr_var)
    if USE_INDEXES["DISCR"]:
        check_discr.select()

    check_corre = tk.Checkbutton(top, text='Correlation')
    check_corre.grid(row=5, column=0, sticky='w')
    check_corre.config(variable=check_corre_var)
    if USE_INDEXES["CORRE"]:
        check_corre.select()

    check_diff = tk.Checkbutton(top, text='Differentiation')
    check_diff.grid(row=6, column=0, sticky='w')
    check_diff.config(variable=check_diff_var)
    if USE_INDEXES["DIFF"]:
        check_diff.select()

    # Normalization
    normalization_label = tk.Label(top, text='Normalization')
    normalization_label.grid(row=7, column=0, sticky='w')

    normalization_stat = tk.Radiobutton(top, text='Statistical', variable=normalization_var, value='Stat')
    normalization_stat.grid(row=8, column=0, sticky='w')
    if normalization_var.get() == 'Stat':
        normalization_stat.select()
    else:
        normalization_stat.deselect()


    normalization_max = tk.Radiobutton(top, text='MaxMin', variable=normalization_var, value='MaxMin')
    normalization_max.grid(row=9, column=0, sticky='w')
    #radio button delelected by default
    if normalization_var.get() == 'MaxMin':
        normalization_max.select()
    else:
        normalization_max.deselect()

    list_results_label = tk.Label(top, text='List results')
    list_results_label.grid(row=10, column=0, sticky='w')

    list_results = tk.Spinbox(top, from_=1, to=100, width=5, textvariable=list_results_var)
    list_results.grid(row=11, column=0, sticky='w')

    # Filter tk.checkbutton
    check_filter = tk.Checkbutton(top, text='Filter')
    check_filter.grid(row=12, column=0, sticky='w')
    check_filter.config(variable=filter_var)
    if USE_INDEXES["Filter"]:
        check_filter.select()

    check_fluo_filter = tk.Checkbutton(top, text='Fluorescence Filter beta')
    check_fluo_filter.grid(row=13, column=0, sticky='w')
    check_fluo_filter.config(variable=fluo_filter_var)
    if USE_INDEXES["Fluo_filter"]:
        check_fluo_filter.select()

    # select folder
    
    folder_label = tk.Label(top, text= 'Database Folder: ').grid(row=15, column=0)
    folder_entry = tk.Entry(top)#.grid(row=0, column =1)
    folder_entry.grid(row=15, column =1)
    if USE_INDEXES["DB"]:
        folder_entry.insert(0, USE_INDEXES["DB"])
    folder_button = tk.Button(top, text = "Browse", command= lambda: folder_entry.insert(0, filedialog.askdirectory())).grid(row=15, column =2)



    # save the checks
    data = [check_norm_corr_var, check_conv_var, check_fft_conv_var, check_hqi_var, check_discr_var, check_corre_var, check_diff_var, normalization_var, list_results_var, filter_var, fluo_filter_var, folder_entry]
    boxes = [check_norm_corr, check_conv, check_fft_conv, check_hqi, check_discr, check_corre, check_diff, normalization_stat, normalization_max, list_results, list_results, check_filter, check_fluo_filter, folder_button, folder_entry]

    # clear button
    clear_button = tk.Button(top, text='Clear', command=lambda : clear_checks(boxes))
    clear_button.grid(row=16, column=0)

    #close button

    close_button = tk.Button(top, text='Use', command=lambda : use_config(top, data))
    close_button.grid(row=16, column=1)

    save_button = tk.Button(top, text='Save', command=lambda : save_configuration(data))
    save_button.grid(row=16, column=2)

    load_button = tk.Button(top, text='Load', command=lambda : load_configuration(top, root))
    load_button.grid(row=16, column=3)


def loading_window(event):
    global OPEN_LOADING
    OPEN_LOADING = True
    
    top = tk.Tk()
    top.title('Loading')
    top.geometry('300x200')
    top.resizable(0, 0)
    while not event.is_set():
        top.grab_set()
        top.focus_set()
        top.focus_force()
        top.update()
        time.sleep(0.2)

    top.destroy()
    OPEN_LOADING = False
    return


def start(root):
    if OPEN_CONFIG or OPEN_LOAD or OPEN_SAVE:
        error_message(root, 'Please close the other windows first')
        return
    event = th.Event()
    thread = th.Thread(target=loading_window, args=(event,))
    thread.start()
    try:
        main_fin = comp.main_v(WORKING_FILE, USE_INDEXES, MAX_MIN, MAX_MIN_EX)
    except Exception as e:
        main_fin = None
        error_message(root, e)
    finally:
        event.set()
        thread.join()
        if main_fin is not None:
            show_results(root, main_fin)
        return main_fin

def show_results(root, main_fin):
    top = tk.Toplevel(root)
    top.title('Results')
    top.geometry('800x600')
    top.resizable(0, 0)
    top.grab_set()
    top.focus_set()
    top.focus_force()

    # create a Frame for the Text and Scrollbar
    txt_frm = tk.Frame(top)
    txt_frm.pack(fill='both', expand=True)
    # ensure a consistent GUI size
    txt_frm.grid_propagate(False)
    # implement stretchability
    txt_frm.grid_rowconfigure(0, weight=1)
    txt_frm.grid_columnconfigure(0, weight=1)

    # create a Text widget
    txt = tk.Text(txt_frm, borderwidth=3, relief='sunken')
    txt.grid(row=0, column=0, sticky='nsew', padx=2, pady=2)

    # create a Scrollbar and associate it with txt
    scrollb = tk.Scrollbar(txt_frm, command=txt.yview)
    scrollb.grid(row=0, column=1, sticky='nsew')
    txt['yscrollcommand'] = scrollb.set
    for key, lista in main_fin.items():
            txt.insert('end',f'{key}: \n\t' + '\n\t'.join( [ str(val[0]).replace('/', '\\\\') + ' = ' + str(val[1]) for val in lista] ) + ' \n\n')
    txt.config(state='disabled')

    # close button
    close_button = tk.Button(top, text='Close', command=top.destroy)
    close_button.pack(side='bottom')

    save_button = tk.Button(top, text='Save', command=lambda : save_results(main_fin))
    save_button.pack(side='bottom')

    return

def save_results(main_fin): 
    file = filedialog.asksaveasfilename(initialdir = BASE_DIR, title = "Select file", filetypes = (("txt files","*.txt"),("all files","*.*")))
    with open(file + '.txt', 'w') as f:
        for key, lista in main_fin.items():
            f.write(f'{key}: \n\t' + '\n\t'.join( [ str(val[0]).replace('/', '\\\\') + ' = ' + str(val[1]) for val in lista] ) + ' \n\n')

def configuration_display(root):

    top = tk.Toplevel(root)
    top.title('Configuration Display')
    top.geometry('800x600')
    top.resizable(0, 0)
    top.grab_set()
    top.focus_set()
    top.focus_force()

    fluo_filter_var = tk.IntVar()
    fluo_filter_var.set(CONF_DIPLAY["fluo_filter"])
    filter_var = tk.IntVar()
    filter_var.set(CONF_DIPLAY["Filter"])
    normalization_var = tk.StringVar()
    normalization_var.set(CONF_DIPLAY["Normalization"])

    #check boxes
    check_norm_corr = tk.Checkbutton(top, text='Fluo Filter', variable=fluo_filter_var, onvalue=True, offvalue=False)
    check_norm_corr.grid(row=0, column=0)
    check_conv = tk.Checkbutton(top, text='Filter', variable=filter_var, onvalue=True, offvalue=False)
    check_conv.grid(row=1, column=0)

    #radio buttons
    normalization_stat = tk.Radiobutton(top, text='MinMax', variable=normalization_var, value='MinMax')
    normalization_stat.grid(row=2, column=0)
    normalization_stat = tk.Radiobutton(top, text='Stat', variable=normalization_var, value='Stat')
    normalization_stat.grid(row=3, column=0)


    load_button = tk.Button(top, text='Use', command=lambda : use_config_display(top, {"fluo_filter": fluo_filter_var.get(), 
                                                                                "Filter": filter_var.get(), 
                                                                                "Normalization": normalization_var.get()}))
    load_button.grid(row=4, column=0)

    close_button = tk.Button(top, text='Close', command=top.destroy)
    close_button.grid(row=5, column=0)

def use_config_display(top, config):
    global CONF_DIPLAY
    for key, value in config.items():
        CONF_DIPLAY[key] = value
    top.destroy()
    return 


def gui_norm(x : list, y : list):
    y = clear_y_V(x, y, CONF_DIPLAY["Filter"], CONF_DIPLAY["Normalization"], CONF_DIPLAY["fluo_filter"])
    return x, y

def display_files(files):
    x, y = load_data(WORKING_FILE)
    x, y = gui_norm(x, y)
    name = os.path.basename(WORKING_FILE)
    plt.plot(x, y, label=name)
    if isinstance(files, list) and files[0] != '':
        for file in files:
            if '#' in file:
                continue
            if '=' in file:
                file = file.split('=')[0]
            try:
                file = file.replace('\t', '')
                if file[-1] == ' ':
                    file = file[:-1]
                x, y = load_data(file)
                x, y = gui_norm(x, y)
                name = os.path.basename(file)
                plt.plot(x, y, label=name)
            except:
                error_message(tk.Tk(), 'Error loading file: ' + file)
    plt.legend()
    plt.show()

def display_filex(root):
    if FILE_LOADED:
    # box where user can paste the files
        top = tk.Toplevel(root)
        top.title('Files to display')
        top.geometry('400x400')
        top.resizable(True, True)

        # create a Frame for the Text and Scrollbar
        txt_frm = tk.Frame(top)
        txt_frm.pack(fill='both', expand=True)
        # ensure a consistent GUI size
        txt_frm.grid_propagate(False)
        # implement stretchability
        txt_frm.grid_rowconfigure(0, weight=1)
        txt_frm.grid_columnconfigure(0, weight=1)
        
        # create a Text widget
        txt = tk.Text(txt_frm, borderwidth=3, relief='sunken')
        txt.grid(row=0, column=0, sticky='nsew', padx=2, pady=2)

        # create a Scrollbar and associate it with txt
        scrollb = tk.Scrollbar(txt_frm, command=txt.yview)
        scrollb.grid(row=0, column=1, sticky='nsew')
        txt['yscrollcommand'] = scrollb.set

        #configuration button
        conf_button = tk.Button(top, text='Config', command=lambda : configuration_display(top))
        conf_button.pack(side='bottom')

        display_button = tk.Button(top, text='Display', command=lambda : display_files(txt.get('1.0', 'end').splitlines()))
        display_button.pack(side='bottom')
    else:
        error_message(root, 'First load a file')


def up_menu(root, file_box):
    menu = tk.Menu(root)
    root.config(menu=menu)

    #create the file object)
    file = tk.Menu(menu)

    #adds a command to the menu option, calling it exit, and the
    #command it runs on event is client_exit
    file.add_command(label='Open..', command=lambda : select_file(root, display=False, file_box=file_box))
    file.add_command(label='Save Graph..', command=hello)
    file.add_command(label='Save Data..', command=hello)
    file.add_command(label='Configuration', command=lambda : configuration_window(root))
    file.add_command(label='Exit', command=root.quit)

    # added "file" to our menu
    menu.add_cascade(label='File', menu=file)

    # create the file object)
    edit = tk.Menu(menu)

    # adds a command to the menu option, calling it exit, and the
    # command it runs on event is client_exit
    edit.add_command(label='Undo')

    # added "file" to our menu
    menu.add_cascade(label='Edit', menu=edit)

    # create the file object)
    help_ = tk.Menu(menu)

    # adds a command to the menu option, calling it exit, and the
    # command it runs on event is client_exit
    help_.add_command(label='About')

    # added "file" to our menu
    menu.add_cascade(label='Help', menu=help_)

def select_file(root, display = False, file_box = None):        
    global X, Y
    global FILE_LOADED, WORKING_FILE

    base_dir = os.getcwd()
    if FILE_LOADED:
        base_dir = os.path.dirname(WORKING_FILE)
    file = filedialog.askopenfilename(initialdir= base_dir, title='Select File',
                                        filetypes=(('txt files', '*.txt'), ('all files', '*.*')))
    x,y = load_data(file)
    X, Y = x, y
    FILE_LOADED = True
    WORKING_FILE = file
    #refresh the file box
    if file_box:
        file_box.delete(0, 'end')
        file_box.insert(0, os.path.basename(WORKING_FILE))

def limit_data(root):
    minim = tk.StringVar()
    maxim = tk.StringVar()
    
    min_label = tk.Label(root, text='Min')
    min_label.grid(row=0, column=0)
    min_entry = tk.Entry(root, textvariable=minim)
    min_entry.grid(row=0, column=1)
    min_entry.insert(0, 'None')
    
    max_label = tk.Label(root, text='Max')
    max_label.grid(row=0, column=2)
    max_entry = tk.Entry(root, textvariable=maxim)
    max_entry.grid(row=0, column=4)
    max_entry.insert(0, 'None')

    use_button = tk.Button(root, text='Use', command=lambda : use_limit(root, minim, maxim))
    use_button.grid(row=0, column=5)

    # exclusion zone 
    ex_minim = tk.StringVar()
    ex_maxim = tk.StringVar()
    
    ex_min_label = tk.Label(root, text='Min Exclusion')
    ex_min_label.grid(row=1, column=0)
    ex_min_entry = tk.Entry(root, textvariable=ex_minim)
    ex_min_entry.grid(row=1, column=1)
    ex_min_entry.insert(0, 'None')



    ex_max_label = tk.Label(root, text='Max Exclusion')
    ex_max_label.grid(row=1, column=2)
    ex_max_entry = tk.Entry(root, textvariable=ex_maxim)
    ex_max_entry.grid(row=1, column=4)
    ex_max_entry.insert(0, 'None')

    ex_use_button = tk.Button(root, text='Use', command=lambda : use_exclusion(root, ex_minim, ex_maxim))
    ex_use_button.grid(row=1, column=5)

def use_limit(root, minim, maxim):
    global MAX_MIN
    if minim.get() and maxim.get():
        try:
            MAX_MIN[0] = float(minim.get())
            MAX_MIN[1] = float(maxim.get())
            error_message(root, 'Max e Min set', title='Success')
        except:
            error_message(root, 'Invalid number')
    else:
        MAX_MIN = [None, None]

def use_exclusion(root, ex_minim, ex_maxim):
    global MAX_MIN_EX
    if ex_minim.get() and ex_maxim.get():
        try:
            MAX_MIN_EX[0] = float(ex_minim.get())
            MAX_MIN_EX[1] = float(ex_maxim.get())
            # open page with a message
            error_message(root, 'Exclusion zone set', title='Success')

        except:
            error_message(root, 'Invalid number')
    else:
        MAX_MIN_EX = [None, None]

