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

    rown = 0
    # check boxes
    check_norm_corr = tk.Checkbutton(top, text='Normalised Correlation')
    check_norm_corr.grid(row=rown, column=0, sticky='w')
    check_norm_corr.config(variable=check_norm_corr_var)
    if USE_INDEXES["NORM_CORR"]:
        check_norm_corr.select()
    rown += 1
    

    check_conv = tk.Checkbutton(top, text='Convolution')
    check_conv.grid(row=rown, column=0, sticky='w')
    check_conv.config(variable=check_conv_var)
    if USE_INDEXES["CONV"]:
        check_conv.select()
    rown += 1

    check_fft_conv = tk.Checkbutton(top, text='FFT Convolution')
    check_fft_conv.grid(row=rown, column=0, sticky='w')
    check_fft_conv.config(variable=check_fft_conv_var)
    if USE_INDEXES["FFT_CONV"]:
        check_fft_conv.select()
    rown += 1

    check_hqi = tk.Checkbutton(top, text='Hit Quality Index')
    check_hqi.grid(row=rown, column=0, sticky='w')
    check_hqi.config(variable=check_hqi_var)
    if USE_INDEXES["HQI"]:
        check_hqi.select()
    rown += 1

    check_discr = tk.Checkbutton(top, text='Discrete Wavelet Transform')
    # check_discr.grid(row=rown, column=0, sticky='w')
    check_discr.config(variable=check_discr_var)
    # if USE_INDEXES["DISCR"]:
    #     check_discr.select()
    # rown += 1

    check_corre = tk.Checkbutton(top, text='Correlation')
    check_corre.grid(row=rown, column=0, sticky='w')
    check_corre.config(variable=check_corre_var)
    if USE_INDEXES["CORRE"]:
        check_corre.select()
    rown += 1

    check_diff = tk.Checkbutton(top, text='Differentiation')
    check_diff.grid(row=rown, column=0, sticky='w')
    check_diff.config(variable=check_diff_var)
    if USE_INDEXES["DIFF"]:
        check_diff.select()
    rown += 1

    # Normalization
    normalization_label = tk.Label(top, text='Normalization')
    normalization_label.grid(row=rown, column=0, sticky='w')
    rown += 1

    normalization_stat = tk.Radiobutton(top, text='Statistical', variable=normalization_var, value='Stat')
    normalization_stat.grid(row=rown, column=0, sticky='w')
    if normalization_var.get() == 'Stat':
        normalization_stat.select()
    else:
        normalization_stat.deselect()
    rown += 1


    normalization_max = tk.Radiobutton(top, text='MaxMin', variable=normalization_var, value='MaxMin')
    normalization_max.grid(row=rown, column=0, sticky='w')
    #radio button delelected by default
    if normalization_var.get() == 'MaxMin':
        normalization_max.select()
    else:
        normalization_max.deselect()
    rown += 1

    list_results_label = tk.Label(top, text='List results')
    list_results_label.grid(row=rown, column=0, sticky='w')
    rown += 1

    list_results = tk.Spinbox(top, from_=1, to=100, width=5, textvariable=list_results_var)
    list_results.grid(row=rown, column=0, sticky='w')
    rown += 1

    # Filter tk.checkbutton
    check_filter = tk.Checkbutton(top, text='Filter')
    check_filter.grid(row=rown, column=0, sticky='w')
    check_filter.config(variable=filter_var)
    if USE_INDEXES["Filter"]:
        check_filter.select()
    rown += 1

    check_fluo_filter = tk.Checkbutton(top, text='Fluorescence Filter beta')
    check_fluo_filter.grid(row=rown, column=0, sticky='w')
    check_fluo_filter.config(variable=fluo_filter_var)
    if USE_INDEXES["Fluo_filter"]:
        check_fluo_filter.select()
    rown += 1

    # select folder
    
    folder_label = tk.Label(top, text= 'Database Folder: ').grid(row=rown, column=0)
    folder_entry = tk.Entry(top)#.grid(row=0, column =1)
    folder_entry.grid(row=rown, column =1)
    if USE_INDEXES["DB"]:
        folder_entry.insert(0, USE_INDEXES["DB"])
    folder_button = tk.Button(top, text = "Browse", command= lambda: folder_entry.insert(0, filedialog.askdirectory())).grid(row=rown, column =2)
    rown += 1


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

    text = tk.Label(top, text='Loading')
    #centet the text
    text.pack()
    giro = ["__", "\\", "|", "/"]
    while not event.is_set():
        top.grab_set()
        top.focus_set()
        top.focus_force()
        top.update()
        # rotating text

        for i in range(4):
            text['text']  = 'Loading ' + giro[i]
            top.update()
            time.sleep(0.2)
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
    top.resizable(1, 1)
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
            # if file starts with #
            if file[0] == '#' or len(file) < 5 :
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
    # Get the global variable MAX_MIN
    global MAX_MIN
    # Check if both entries minim and maxim are not empty
    if minim.get() and maxim.get():
        # Try to convert the string in the entries to float
        try:
            MAX_MIN[0] = float(minim.get())
            MAX_MIN[1] = float(maxim.get())
        except:
            # If the conversion is not successful, an error message is shown
            error_message(root, 'Invalid number')
            # If the conversion is not successful, the global variable MAX_MIN is set to None
            MAX_MIN = [None, None]
    else:
        # If one or both entries are empty, the global variable MAX_MIN is set to None
        MAX_MIN = [None, None]

def use_exclusion(root, ex_minim, ex_maxim):
    global MAX_MIN_EX
    # check if both entry boxes are filled
    if ex_minim.get() and ex_maxim.get():
        try:
            # try to convert the values to floats
            max_excl = float(ex_maxim.get())
            min_excl = float(ex_minim.get())
            if max_excl >= min_excl:
                # if the minimum exclusion zone is smaller than the maximum, assign the values
                MAX_MIN_EX[0] = min_excl
                MAX_MIN_EX[1] = max_excl
                # open page with a message
            else:
                # if the maximum exclusion zone is smaller than the minimum, open page with error message
                error_message(root, 'Invalid number')
        except:
            # if an error occurs, open page with error message
            error_message(root, 'Invalid number')
    else:
        # if one of the entry boxes is not filled, set the exclusion zone to None
        MAX_MIN_EX = [None, None]

def modify_enter(root):
    top = tk.Toplevel(root)
    top.title('Modify Enter')
    top.geometry('550x250')
    top.resizable(False, False)
    top.focus_set()
    top.grab_set()

    # button check for guassian filter
    check_gauss = tk.IntVar()
    check_gauss_button = tk.Checkbutton(top, text='Gaussian Filter (odd)', variable=check_gauss)
    check_gauss_button.grid(row=0, column=0)

    # value for the gaussian filter
    gauss_value = tk.StringVar()
    gauss_entry = tk.Entry(top, textvariable=gauss_value)
    gauss_entry.grid(row=0, column=1)
    gauss_entry.insert(0, '3')

    # button for baseline correction
    check_base = tk.IntVar()
    button_baseline = tk.Checkbutton(top, text='Baseline Correction', variable=check_base)
    button_baseline.grid(row=1, column=0)

    #label for the baseline correction
    baseline_label = tk.Label(top, text='window_length (odd)')
    baseline_label.grid(row=1, column=1)
    # value for the baseline correction

    baseline_value = tk.StringVar()
    baseline_entry = tk.Entry(top, textvariable=baseline_value)
    baseline_entry.grid(row=1, column=2)
    baseline_entry.insert(0, '401')

    #label for the baseline correction
    poly_label = tk.Label(top, text='polyorder')
    poly_label.grid(row=2, column=1)
    # value for the baseline correction

    poly_value = tk.StringVar()
    poly_entry = tk.Entry(top, textvariable=poly_value)
    poly_entry.grid(row=2, column=2)
    poly_entry.insert(0, '3')

    #diff label
    diff_label = tk.Label(top, text='Diff')
    diff_label.grid(row=3, column=0)
    #diff value
    diff_value = tk.StringVar()
    diff_entry = tk.Entry(top, textvariable=diff_value)
    diff_entry.grid(row=3, column=1)
    diff_entry.insert(0, '10')

    #Display checkboxs
    displayoriginal_check = tk.IntVar()
    display_check_button = tk.Checkbutton(top, text='Display Orginal', variable=displayoriginal_check)
    display_check_button.grid(row=5, column=0)

    displaymodified_check = tk.IntVar()
    display_check_button = tk.Checkbutton(top, text='Display Baseline', variable=displaymodified_check)
    display_check_button.grid(row=6, column=0)

    displaydifference_check = tk.IntVar()
    display_check_button = tk.Checkbutton(top, text='Display Difference', variable=displaydifference_check)
    display_check_button.grid(row=7, column=0)

    diplaygau_check = tk.IntVar()
    display_check_button = tk.Checkbutton(top, text='Display Filtered', variable=diplaygau_check) 
    display_check_button.grid(row=8, column=0)

    check_boxes = [displayoriginal_check, diplaygau_check, displaymodified_check, displaydifference_check]



    #button use all
    use_all_button = tk.Button(top, text='Display', command=lambda : use_all(top, check_gauss, gauss_value, check_base, baseline_value, poly_value, diff_value, 'Diplay', check_boxes))
    use_all_button.grid(row=4, column=0)

    #button save modified
    save_modified_button = tk.Button(top, text='Save Modified', command=lambda : use_all(top, check_gauss, gauss_value, check_base, baseline_value, poly_value, diff_value, 'SaveMod'))
    save_modified_button.grid(row=4, column=1)

    #save difference
    save_diff_button = tk.Button(top, text='Save Difference', command=lambda : use_all(top, check_gauss, gauss_value, check_base, baseline_value, poly_value, diff_value, 'SaveDiff'))
    save_diff_button.grid(row=4, column=2)

    # use
    use_button = tk.Button(top, text='Use', command=lambda : use_all(top, check_gauss, gauss_value, check_base, baseline_value, poly_value, diff_value, 'USE'))
    use_button.grid(row=4, column=3)




def use_all(top, check_gauss, gauss_value, check_base, baseline_value, poly_value, diff_value, Wat, check_boxes=None):
    global WORKING_FILE
    if diff_value.get():
        try:
            DIFF = float(diff_value.get())
        except:
            error_message(top, 'Invalid number')
            DIFF = None

    if check_gauss.get():
        try:
            GAUSSIAN_FILTER = int(gauss_value.get())
            if GAUSSIAN_FILTER % 2 == 0:
                error_message(top, 'Invalid gaussian filter number')
                GAUSSIAN_FILTER = None
        except:
            error_message(top, 'Invalid number')
            GAUSSIAN_FILTER = None
    else:
        GAUSSIAN_FILTER = None

    if check_base.get():
        try:
            BASELINE_CORRECTION = int(baseline_value.get())
            if BASELINE_CORRECTION % 2 == 0:
                error_message(top, 'Invalid window_length number')
                BASELINE_CORRECTION = None
        except:
            error_message(top, 'Invalid number')
            BASELINE_CORRECTION = None
    else:
        BASELINE_CORRECTION = None

    if check_base.get():
        try:
            POLYORDER = int(poly_value.get())
        except:
            error_message(top, 'Invalid number')
            POLYORDER = None

    if FILE_LOADED:
        x_a, y_a = load_data(WORKING_FILE)
    else:
        error_message(top, 'No data loaded')
        return
    
    y_m = y_a
    y_g = y_a

    if GAUSSIAN_FILTER and check_gauss.get():
        y_g = scipy.ndimage.filters.gaussian_filter1d(y_a, GAUSSIAN_FILTER)

    if BASELINE_CORRECTION and check_base.get():
        y_m = savgol_filter(y_g, BASELINE_CORRECTION, POLYORDER)
    
    y_m = [val - DIFF for val in y_m]
    
    try:
        y_n = y_g - y_m
    except:
        y_n = [a-b for a, b in zip(y_g, y_m)]

    if Wat == 'Diplay':
        checki = [box.get() for box in check_boxes]
        if not checki[0]:
            y_a = None
        if not checki[1]:
            y_g = None
        if not checki[2]:
            y_m = None
        if not checki[3]:
            y_n = None
        mid_display(x_a, y_a, y_g, y_m, y_n)

    elif Wat == 'SaveMod':
        save_data(x_a, y_m)

    elif Wat == 'SaveDiff':
        save_data(x_a, y_n)

    elif Wat == 'USE':
        WORKING_FILE = [[x_a[i], y_n[i] ] for i in range(len(x_a))]

def save_data(x, y):
    save_file = filedialog.asksaveasfilename(defaultextension='.txt', filetypes=[('Text file', '*.txt')])
    if save_file:
        with open(save_file, 'w') as f:
            for i in range(len(x)):
                f.write(str(x[i]) + '\t' + str(y[i]) + '\n')

def mid_display(x, y_1 = None, y_g= None, y_2= None, y_3= None):
    if y_1 != None:
        plt.plot(x, y_1, label='Original')
    if y_g is not None:
        plt.plot(x, y_g, label='Gaussian')
    if y_2 is not None:
        plt.plot(x, y_2, label='Baseline')
    if y_3 is not None:
        plt.plot(x, y_3, label='Difference')
    plt.legend()
    plt.show()