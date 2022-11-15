from modules.importer import *
from modules.basic_functions import *

WORKING_FILE = None
OPEN_CONFIG = False
OPEN_LOAD = False
OPEN_SAVE = False
X, Y = None, None
FILE_LOADED = False

BASE_DIR = os.getcwd()


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

def load_config(root, data):
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

    #open a path to save the configuration
    path = filedialog.asksaveasfilename(initialdir = BASE_DIR, title = "Select file",filetypes = (("cnf files","*.cnf"),("all files","*.*"))) 
    if path:
        with open(path + '.cnf', 'w') as file:
            file.write(str(USE_INDEXES))
    OPEN_SAVE = False
    #print the value of the checks

def error_message(root, message):
    top = tk.Toplevel(root)
    top.title('Error')
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
                    USE_INDEXES[element[0]] = '1' == element[1]
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

    # Filter tk.Radiobutton
    filter_label = tk.Label(top, text='Filter')
    filter_label.grid(row=12, column=0, sticky='w')
    
    filter_true = tk.Radiobutton(top, text='True', variable=filter_var, value=True)
    filter_true.grid(row=13, column=0, sticky='w')
    if filter_var.get() == True:
        filter_true.select()
    else:
        filter_true.deselect()

    filter_false = tk.Radiobutton(top, text='False', variable=filter_var, value=False)
    filter_false.grid(row=14, column=0, sticky='w')
    if filter_var.get() == False:
        filter_false.select()
    else:
        filter_false.deselect()

    # save the checks
    data = [check_norm_corr_var, check_conv_var, check_fft_conv_var, check_hqi_var, check_discr_var, check_corre_var, check_diff_var, normalization_var, list_results_var, filter_var]
    boxes = [check_norm_corr, check_conv, check_fft_conv, check_hqi, check_discr, check_corre, check_diff, normalization_stat, normalization_max, list_results, list_results, filter_true, filter_false]

    # clear button
    clear_button = tk.Button(top, text='Clear', command=lambda : clear_checks(boxes))
    clear_button.grid(row=15, column=0)

    #close button

    close_button = tk.Button(top, text='Use', command=lambda : load_config(top, data))
    close_button.grid(row=15, column=1)

    save_button = tk.Button(top, text='Save', command=lambda : save_configuration(data))
    save_button.grid(row=15, column=2)

    load_button = tk.Button(top, text='Load', command=lambda : load_configuration(top, root))
    load_button.grid(row=15, column=3)


def start(root):
    if OPEN_CONFIG or OPEN_LOAD or OPEN_SAVE:
        error_message(root, 'Please close the other windows first')
        return
    


def display_graph(root, x = None, y = None):
    if FILE_LOADED:
        plt.plot(X, Y)
        plt.show()

    else:
        top = tk.Toplevel(root)
        top.title('Graph')
        top.geometry('400x400')
        top.resizable(True, True)

        graph = tk.Canvas(top, width=200, height=100)
        graph.pack()
        graph.grid(row=0, column=0)
        graph.create_line(0, 0, 200, 100)
        graph.create_line(0, 100, 200, 0, fill='red', dash=(4, 4))
        graph.create_rectangle(50, 25, 150, 75, fill='blue')

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
    if display:
        display_graph(root, x, y)
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

def start_comparison(root):
    pass
