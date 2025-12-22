from modules.importer import *
from modules.basic_functions import *
import comarator as comp

WORKING_FILE = None
FILTER_FILE = None
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
                "Normalization" : "MaxMin",
                "List_results" : 10,
                "Filter": False,
                "Fluo_filter": False,
                "DB" : None,
                }

LIST_BOOL = ["NORM_CORR", "CONV", "FFT_CONV", "HQI", "DISCR", "CORRE", "DIFF", "Filter"]
LIST_FIGURES = ["NORM_CORR", "CONV", "FFT_CONV", "HQI", "DISCR", "CORRE", "DIFF"]

def clear_checks(data):
    for check in data:
        if isinstance(check, tk.Checkbutton):
            check.deselect()
        if isinstance(check, tk.Radiobutton):
            check.deselect()
        if isinstance(check, tk.Spinbox):
            check.delete(0, 10)

def use_config(root, data):
    global OPEN_CONFIG, USE_INDEXES
    keys = ["NORM_CORR", "CONV", "FFT_CONV", "HQI", "DISCR", "CORRE", "DIFF", 
            "Normalization", "List_results", "Filter", "Fluo_filter", "DB"]
    for i, key in enumerate(keys):
        USE_INDEXES[key] = data[i].get()
    root.destroy()
    OPEN_CONFIG = False

def save_configuration(data):
    global OPEN_CONFIG, OPEN_SAVE, USE_INDEXES
    OPEN_SAVE = True
    keys = ["NORM_CORR", "CONV", "FFT_CONV", "HQI", "DISCR", "CORRE", "DIFF", 
            "Normalization", "List_results", "Filter", "DB"]
    for i, key in enumerate(keys):
        USE_INDEXES[key] = data[i].get()
    
    path = filedialog.asksaveasfilename(initialdir=BASE_DIR, title="Select file",
                                        filetypes=(("cnf files","*.cnf"),("all files","*.*"))) 
    if path:
        with open(path + '.cnf', 'w') as file:
            file.write(str(USE_INDEXES))
    OPEN_SAVE = False

def error_message(root, message, title = 'Error'):
    top = tk.Toplevel(root)
    top.title(title)
    top.geometry('400x180')
    top.resizable(False, False)
    top.configure(bg='#f5f6fa')
    top.transient(root)
    top.grab_set()
    
    # Center the window
    top.update_idletasks()
    width = top.winfo_width()
    height = top.winfo_height()
    x = (top.winfo_screenwidth() // 2) - (width // 2)
    y = (top.winfo_screenheight() // 2) - (height // 2)
    top.geometry(f'{width}x{height}+{x}+{y}')
    
    # Main frame
    main_frame = tk.Frame(top, bg='#f5f6fa', padx=25, pady=20)
    main_frame.pack(fill='both', expand=True)
    
    # Icon
    icon_label = tk.Label(main_frame, text='⚠️', 
                          font=('Segoe UI', 32), 
                          bg='#f5f6fa')
    icon_label.pack(pady=(0, 10))
    
    # Message
    message_label = tk.Label(main_frame, text=str(message), 
                            font=('Segoe UI', 10), 
                            bg='#f5f6fa', fg='#2c3e50',
                            wraplength=350, justify='center')
    message_label.pack(pady=(0, 20))
    
    # OK button
    ok_button = tk.Button(main_frame, text='OK', 
                         command=top.destroy,
                         font=('Segoe UI', 9, 'bold'), 
                         bg='#e74c3c', fg='white',
                         relief='flat', padx=30, pady=8,
                         cursor='hand2')
    ok_button.pack()
    
    # Focus the button
    ok_button.focus_set()
    
    # Bind Enter key to close
    top.bind('<Return>', lambda e: top.destroy())

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
    top.title('Analysis Configuration')
    top.geometry('520x660')
    top.resizable(False, False)
    top.configure(bg='#f5f6fa')
    
    # Keep window on top of parent
    top.transient(root)
    top.grab_set()
    top.focus_set()

    # Variables
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

    # Main container with scrollbar
    main_frame = tk.Frame(top, bg='#f5f6fa', padx=20, pady=15)
    main_frame.pack(fill='both', expand=True)

    # Analysis Methods Section
    methods_frame = tk.LabelFrame(main_frame, text='Analysis Methods', 
                                  font=('Segoe UI', 10, 'bold'),
                                  bg='#f5f6fa', fg='#2c3e50',
                                  padx=15, pady=10)
    methods_frame.pack(fill='x', pady=(0, 10))

    check_norm_corr = tk.Checkbutton(methods_frame, text='Normalised Correlation',
                                     variable=check_norm_corr_var, bg='#f5f6fa',
                                     font=('Segoe UI', 9))
    check_norm_corr.pack(anchor='w', pady=2)

    check_conv = tk.Checkbutton(methods_frame, text='Convolution',
                                variable=check_conv_var, bg='#f5f6fa',
                                font=('Segoe UI', 9))
    check_conv.pack(anchor='w', pady=2)

    check_fft_conv = tk.Checkbutton(methods_frame, text='FFT Convolution',
                                    variable=check_fft_conv_var, bg='#f5f6fa',
                                    font=('Segoe UI', 9))
    check_fft_conv.pack(anchor='w', pady=2)

    check_hqi = tk.Checkbutton(methods_frame, text='Hit Quality Index',
                               variable=check_hqi_var, bg='#f5f6fa',
                               font=('Segoe UI', 9))
    check_hqi.pack(anchor='w', pady=2)

    check_discr = tk.Checkbutton(methods_frame, text='Discrete Wavelet Transform',
                                 variable=check_discr_var, bg='#f5f6fa',
                                 font=('Segoe UI', 9))
    # check_discr.pack(anchor='w', pady=2)  # Still commented out

    check_corre = tk.Checkbutton(methods_frame, text='Correlation',
                                 variable=check_corre_var, bg='#f5f6fa',
                                 font=('Segoe UI', 9))
    check_corre.pack(anchor='w', pady=2)

    check_diff = tk.Checkbutton(methods_frame, text='Differentiation',
                                variable=check_diff_var, bg='#f5f6fa',
                                font=('Segoe UI', 9))
    check_diff.pack(anchor='w', pady=2)

    # Normalization Section
    norm_frame = tk.LabelFrame(main_frame, text='Normalization',
                               font=('Segoe UI', 10, 'bold'),
                               bg='#f5f6fa', fg='#2c3e50',
                               padx=15, pady=10)
    norm_frame.pack(fill='x', pady=(0, 10))

    normalization_max = tk.Radiobutton(norm_frame, text='MaxMin Normalization',
                                       variable=normalization_var, value='MaxMin',
                                       bg='#f5f6fa', font=('Segoe UI', 9))
    normalization_max.pack(anchor='w', pady=2)

    normalization_stat = tk.Radiobutton(norm_frame, text='Statistical Normalization',
                                        variable=normalization_var, value='Stat',
                                        bg='#f5f6fa', font=('Segoe UI', 9))
    normalization_stat.pack(anchor='w', pady=2)

    # Filters Section
    filters_frame = tk.LabelFrame(main_frame, text='Filters',
                                  font=('Segoe UI', 10, 'bold'),
                                  bg='#f5f6fa', fg='#2c3e50',
                                  padx=15, pady=10)
    filters_frame.pack(fill='x', pady=(0, 10))

    check_filter = tk.Checkbutton(filters_frame, text='Apply Filter',
                                  variable=filter_var, bg='#f5f6fa',
                                  font=('Segoe UI', 9))
    check_filter.pack(anchor='w', pady=2)

    check_fluo_filter = tk.Checkbutton(filters_frame, text='Fluorescence Filter (beta)',
                                       variable=fluo_filter_var, bg='#f5f6fa',
                                       font=('Segoe UI', 9))
    check_fluo_filter.pack(anchor='w', pady=2)

    # Results Section
    results_frame = tk.LabelFrame(main_frame, text='Results',
                                  font=('Segoe UI', 10, 'bold'),
                                  bg='#f5f6fa', fg='#2c3e50',
                                  padx=15, pady=10)
    results_frame.pack(fill='x', pady=(0, 10))

    results_inner = tk.Frame(results_frame, bg='#f5f6fa')
    results_inner.pack(fill='x')

    list_results_label = tk.Label(results_inner, text='Number of results:',
                                   bg='#f5f6fa', font=('Segoe UI', 9))
    list_results_label.pack(side='left', padx=(0, 10))

    list_results = tk.Spinbox(results_inner, from_=1, to=100, width=10,
                              textvariable=list_results_var,
                              font=('Segoe UI', 9))
    list_results.pack(side='left')

    # Database Section
    db_frame = tk.LabelFrame(main_frame, text='Database',
                             font=('Segoe UI', 10, 'bold'),
                             bg='#f5f6fa', fg='#2c3e50',
                             padx=15, pady=10)
    db_frame.pack(fill='x', pady=(0, 10))

    folder_inner = tk.Frame(db_frame, bg='#f5f6fa')
    folder_inner.pack(fill='x')

    folder_label = tk.Label(folder_inner, text='Folder:', bg='#f5f6fa',
                           font=('Segoe UI', 9))
    folder_label.pack(side='left', padx=(0, 10))

    folder_entry = tk.Entry(folder_inner, font=('Segoe UI', 9))
    folder_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
    if USE_INDEXES["DB"]:
        folder_entry.insert(0, USE_INDEXES["DB"])
    
    def browse_folder():
        folder = filedialog.askdirectory()
        if folder:
            folder_entry.delete(0, tk.END)
            folder_entry.insert(0, folder)
        top.lift()
        top.focus_set()
    
    folder_button = tk.Button(folder_inner, text="Browse", command=browse_folder,
                             font=('Segoe UI', 9), bg='#3498db', fg='white',
                             relief='flat', padx=15, pady=3)
    folder_button.pack(side='left')

    # Data for callbacks
    data = [check_norm_corr_var, check_conv_var, check_fft_conv_var, check_hqi_var, 
            check_discr_var, check_corre_var, check_diff_var, normalization_var, 
            list_results_var, filter_var, fluo_filter_var, folder_entry]
    boxes = [check_norm_corr, check_conv, check_fft_conv, check_hqi, check_discr, 
             check_corre, check_diff, normalization_stat, normalization_max, 
             list_results, list_results, check_filter, check_fluo_filter, 
             folder_button, folder_entry]

    # Buttons Section
    button_frame = tk.Frame(main_frame, bg='#f5f6fa')
    button_frame.pack(fill='x', pady=(10, 0))

    clear_button = tk.Button(button_frame, text='Clear', 
                            command=lambda: clear_checks(boxes),
                            font=('Segoe UI', 9), bg='#7f8c8d', fg='white',
                            relief='flat', padx=20, pady=8)
    clear_button.pack(side='left', padx=(0, 5))

    load_button = tk.Button(button_frame, text='Load Config',
                           command=lambda: load_configuration(top, root),
                           font=('Segoe UI', 9), bg='#95a5a6', fg='white',
                           relief='flat', padx=20, pady=8)
    load_button.pack(side='left', padx=5)

    save_button = tk.Button(button_frame, text='Save Config',
                           command=lambda: save_configuration(data),
                           font=('Segoe UI', 9), bg='#95a5a6', fg='white',
                           relief='flat', padx=20, pady=8)
    save_button.pack(side='left', padx=5)

    close_button = tk.Button(button_frame, text='Apply',
                            command=lambda: use_config(top, data),
                            font=('Segoe UI', 9, 'bold'), bg='#3498db', fg='white',
                            relief='flat', padx=25, pady=8)
    close_button.pack(side='right')

def loading_window(event):
    global OPEN_LOADING
    OPEN_LOADING = True
    
    top = tk.Tk()
    top.title('Processing')
    top.geometry('380x220')
    top.resizable(False, False)
    
    # Center the window on screen
    top.update_idletasks()
    width = top.winfo_width()
    height = top.winfo_height()
    x = (top.winfo_screenwidth() // 2) - (width // 2)
    y = (top.winfo_screenheight() // 2) - (height // 2)
    top.geometry(f'{width}x{height}+{x}+{y}')
    
    # Main frame with modern styling
    main_frame = tk.Frame(top, bg='#f5f6fa', padx=40, pady=35)
    main_frame.pack(fill='both', expand=True)
    
    # Icon
    icon_label = tk.Label(main_frame, text='⚡', 
                          font=('Segoe UI', 36), 
                          bg='#f5f6fa', fg='#3498db')
    icon_label.pack(pady=(0, 12))
    
    # Animated text
    text = tk.Label(main_frame, text='Processing', 
                   font=('Segoe UI', 12, 'bold'), 
                   bg='#f5f6fa', fg='#2c3e50')
    text.pack()
    
    # Animation characters
    giro = ["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]
    
    while not event.is_set():
        top.grab_set()
        top.focus_set()
        top.focus_force()
        top.update()

        for i in range(8):
            text['text'] = 'Processing ' + giro[i]
            top.update()
            time.sleep(0.2)
        time.sleep(0.1)

    top.destroy()
    OPEN_LOADING = False
    return

def start(root):
    if OPEN_CONFIG or OPEN_LOAD or OPEN_SAVE:
        error_message(root, 'Please close the other windows first')
        return
    continuation = False
    for index in USE_INDEXES:
        if index in LIST_FIGURES:
            if not USE_INDEXES[index]:
                pass
            else:
                continuation = True
    if continuation:
        pass
    else:
        error_message(root, f'Please select at least one analysis method') 
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
    top.title('Analysis Results - SpeComp')
    top.geometry('900x650')
    top.resizable(1, 1)
    top.configure(bg='#f5f6fa')
    top.transient(root)
    top.grab_set()
    top.focus_set()
    top.focus_force()

    # Header frame
    header_frame = tk.Frame(top, bg='#f5f6fa', padx=20, pady=15)
    header_frame.pack(fill='x')

    title_label = tk.Label(header_frame, text='📊 Analysis Results', 
                          font=('Segoe UI', 16, 'bold'),
                          bg='#f5f6fa', fg='#2c3e50')
    title_label.pack(anchor='w')

    subtitle_label = tk.Label(header_frame, text='Database comparison results ranked by similarity',
                             font=('Segoe UI', 9),
                             bg='#f5f6fa', fg='#7f8c8d')
    subtitle_label.pack(anchor='w', pady=(2, 0))

    # Separator
    separator = tk.Frame(top, height=2, bg='#bdc3c7')
    separator.pack(fill='x', padx=20)

    # Main content frame with padding
    content_frame = tk.Frame(top, bg='#f5f6fa', padx=20, pady=15)
    content_frame.pack(fill='both', expand=True)

    # create a Frame for the Text and Scrollbar
    txt_frm = tk.Frame(content_frame, bg='#ffffff', relief='solid', bd=1)
    txt_frm.pack(fill='both', expand=True)
    txt_frm.grid_rowconfigure(0, weight=1)
    txt_frm.grid_columnconfigure(0, weight=1)

    # create a Text widget with modern styling
    txt = tk.Text(txt_frm, 
                  borderwidth=0, 
                  relief='flat',
                  font=('Consolas', 9),
                  bg='#ffffff',
                  fg='#2c3e50',
                  wrap='none',
                  padx=15,
                  pady=10)
    txt.grid(row=0, column=0, sticky='nsew')

    # create a Scrollbar with better styling
    scrollb = tk.Scrollbar(txt_frm, command=txt.yview)
    scrollb.grid(row=0, column=1, sticky='nsew')
    txt['yscrollcommand'] = scrollb.set

    # Configure text tags for better formatting
    txt.tag_configure('algorithm', font=('Segoe UI', 10, 'bold'), foreground='#2980b9')
    txt.tag_configure('rank', foreground='#27ae60')
    txt.tag_configure('score', foreground='#e67e22')

    # Insert formatted results
    for key, lista in main_fin.items():
        txt.insert('end', f'● {key}\n', 'algorithm')
        for rank, (filepath, score) in enumerate(lista, start=1):
            filename = filepath.replace('/', '\\\\')
            only_filename = os.path.basename(filename)
            txt.insert('end', f'  {rank}. ', 'rank')
            txt.insert('end', f'{only_filename} ')
            txt.insert('end', f'(Score: {score:.4f})\n', 'score')
        txt.insert('end', '\n')
    
    txt.config(state='disabled')

    # Button frame with modern styling
    button_frame = tk.Frame(top, bg='#f5f6fa', pady=15)
    button_frame.pack(side='bottom', fill='x', padx=20)

    # Center the buttons
    button_container = tk.Frame(button_frame, bg='#f5f6fa')
    button_container.pack()

    # Save buttons with modern styling
    save_txt_button = tk.Button(button_container, text='💾 Save as TXT', 
                                command=lambda: save_results(main_fin),
                                font=('Segoe UI', 9),
                                bg='#95a5a6', fg='white',
                                relief='flat', padx=20, pady=8,
                                cursor='hand2')
    save_txt_button.pack(side='left', padx=5)

    save_csv_button = tk.Button(button_container, text='📊 Save as CSV', 
                                command=lambda: save_results_csv(main_fin),
                                font=('Segoe UI', 9),
                                bg='#27ae60', fg='white',
                                relief='flat', padx=20, pady=8,
                                cursor='hand2')
    save_csv_button.pack(side='left', padx=5)

    # Close button
    close_button = tk.Button(button_container, text='✖ Close', 
                            command=top.destroy,
                            font=('Segoe UI', 9),
                            bg='#e74c3c', fg='white',
                            relief='flat', padx=25, pady=8,
                            cursor='hand2')
    close_button.pack(side='left', padx=5)

    # Add hover effects
    def on_enter(e, btn, color):
        btn['background'] = color

    def on_leave(e, btn, color):
        btn['background'] = color

    save_txt_button.bind("<Enter>", lambda e: on_enter(e, save_txt_button, '#7f8c8d'))
    save_txt_button.bind("<Leave>", lambda e: on_leave(e, save_txt_button, '#95a5a6'))
    
    save_csv_button.bind("<Enter>", lambda e: on_enter(e, save_csv_button, '#229954'))
    save_csv_button.bind("<Leave>", lambda e: on_leave(e, save_csv_button, '#27ae60'))
    
    close_button.bind("<Enter>", lambda e: on_enter(e, close_button, '#c0392b'))
    close_button.bind("<Leave>", lambda e: on_leave(e, close_button, '#e74c3c'))

    return

def save_results(main_fin): 
    file = filedialog.asksaveasfilename(initialdir = BASE_DIR, title = "Select file", filetypes = (("txt files","*.txt"),("all files","*.*")))
    if file:
        with open(file.replace('.txt', '') + '.txt', 'w') as f:
            db_link = USE_INDEXES["DB"] if USE_INDEXES["DB"] else "Not specified"
            f.write(f'Database folder: {db_link}\n\n')
            for key, lista in main_fin.items():
                #only_filename = [ os.path.basename(val[0]) for val in lista ]
                f.write(f'Algorithm: {key}\n')
                for rank, (filepath, score) in enumerate(lista, start=1):
                    filename = filepath.replace('/', '\\\\')
                    only_filename = os.path.basename(filename)
                    f.write(f'  {rank}. {only_filename} (Score: {score:.4f})\n')
                #f.write(f'{key}: \n\t' + '\n\t'.join( [ str(val[0]).replace('/', '\\\\') + ' = ' + str(val[1]) for val in lista] ) + ' \n\n')

def save_results_csv(main_fin):
    """Save results to CSV format"""
    file = filedialog.asksaveasfilename(
        initialdir=BASE_DIR, 
        title="Save as CSV", 
        defaultextension=".csv",
        filetypes=(("CSV files", "*.csv"), ("all files", "*.*"))
    )
    if file:
        with open(file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # Write header
            writer.writerow(['Algorithm', 'Rank', 'Database', 'Spectrum', 'Score'])
            
            # Write data
            for algorithm, results_list in main_fin.items():
                for rank, (filepath, score) in enumerate(results_list, start=1):
                    writer.writerow([algorithm, rank, os.path.dirname(filepath), os.path.basename(filepath), score])

def configuration_display(root):

    top = tk.Toplevel(root)
    top.title('Display Configuration')
    top.geometry('350x220')
    top.resizable(False, False)
    top.transient(root)
    top.grab_set()
    top.focus_set()

    # Variables
    fluo_filter_var = tk.IntVar(value=CONF_DIPLAY["fluo_filter"])
    filter_var = tk.IntVar(value=CONF_DIPLAY["Filter"])
    normalization_var = tk.StringVar(value=CONF_DIPLAY["Normalization"])

    # Main frame with padding
    main_frame = tk.Frame(top, padx=20, pady=15)
    main_frame.pack(fill='both', expand=True)

    # Filters section
    filter_label = tk.Label(main_frame, text='Filters:', font=('Segoe UI', 10, 'bold'))
    filter_label.grid(row=0, column=0, sticky='w', pady=(0, 5))

    check_filter = tk.Checkbutton(main_frame, text='Apply Filter', variable=filter_var)
    check_filter.grid(row=1, column=0, sticky='w', padx=20, pady=2)

    check_fluo = tk.Checkbutton(main_frame, text='Fluorescence Filter', variable=fluo_filter_var)
    check_fluo.grid(row=2, column=0, sticky='w', padx=20, pady=2)

    # Separator
    separator = tk.Frame(main_frame, height=2, bd=1, relief='sunken')
    separator.grid(row=3, column=0, sticky='ew', pady=10)

    # Normalization section
    norm_label = tk.Label(main_frame, text='Normalization:', font=('Segoe UI', 10, 'bold'))
    norm_label.grid(row=4, column=0, sticky='w', pady=(0, 5))

    radio_minmax = tk.Radiobutton(main_frame, text='Min-Max Normalization', 
                                   variable=normalization_var, value='MinMax')
    radio_minmax.grid(row=5, column=0, sticky='w', padx=20, pady=2)

    radio_stat = tk.Radiobutton(main_frame, text='Statistical Normalization', 
                                variable=normalization_var, value='Stat')
    radio_stat.grid(row=6, column=0, sticky='w', padx=20, pady=2)

    # Button frame
    button_frame = tk.Frame(main_frame)
    button_frame.grid(row=7, column=0, pady=(15, 0))

    use_button = tk.Button(button_frame, text='Apply', width=10,
                          command=lambda: use_config_display(top, {
                              "fluo_filter": fluo_filter_var.get(),
                              "Filter": filter_var.get(),
                              "Normalization": normalization_var.get()
                          }))
    use_button.pack(side='left', padx=5)

    close_button = tk.Button(button_frame, text='Cancel', width=10, command=top.destroy)
    close_button.pack(side='left', padx=5)

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
            if not file:
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

def clear_list(file_list : list):
    new_list = []
    if isinstance(file_list, list):
        for file in file_list:
            # if file starts with #
            if file[0] == '#' or len(file) < 5 :
                continue
            if not file:
                continue
            if '=' in file:
                file = file.split('=')[0]
            if not os.path.isfile(file):
                filum = file.split()
                for fi in filum:
                    if '.txt' in fi:
                        file = fi
                        break
                file = os.path.join(USE_INDEXES["DB"], file)
            try:
                file = file.replace('\t', '')
                if file[-1] == ' ':
                    file = file[:-1]
                new_list.append(file)
            except:
                error_message(tk.Tk(), 'Error loading file: ' + file)
    return new_list


def display_subtraction():
    global WORKING_FILE, FILTER_FILE

    if not WORKING_FILE:
        error_message(tk.Tk(), 'No working file loaded')
        return
    
    if not FILTER_FILE:
        error_message(tk.Tk(), 'No filter file loaded')
        return

    # Load initial data
    x_work, y_work = load_data(WORKING_FILE)
    x_work, y_work = gui_norm(x_work, y_work)
    
    x_filt, y_filt = load_data(FILTER_FILE)
    x_filt, y_filt = gui_norm(x_filt, y_filt)

    # Store modified working data
    modified_data = {'x': x_work.copy() if isinstance(x_work, np.ndarray) else list(x_work), 
                     'y': y_work.copy() if isinstance(y_work, np.ndarray) else list(y_work)}
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 6))
    plt.subplots_adjust(bottom=0.25)
    
    # Track if plot has been initialized
    plot_state = {'initialized': False}
    
    # Window size parameter for smart subtraction
    whole_window_size = len(x_work) // 2
    window_size = {'value': whole_window_size}

    def update_plot():
        # Store current axis limits before clearing (only if already initialized)
        if plot_state['initialized']:
            xlim = ax.get_xlim()
            ylim = ax.get_ylim()
        
        ax.clear()
        ax.plot(x_work, y_work, label=os.path.basename(WORKING_FILE) + ' (Original)', alpha=0.5, linestyle='--')
        ax.plot(x_filt, y_filt, label=os.path.basename(FILTER_FILE), alpha=0.7)
        ax.plot(modified_data['x'], modified_data['y'], label='Modified', linewidth=2)
        ax.set_xlabel('Wavelength')
        ax.set_ylabel('Intensity')
        ax.grid(True, alpha=0.3)
        
        # Restore axis limits to maintain zoom (only if already initialized)
        if plot_state['initialized']:
            ax.set_xlim(xlim)
            ax.set_ylim(ylim)
        else:
            plot_state['initialized'] = True
        
        # Update legend without "Selected Peak" if not actively showing
        ax.legend()
        plt.draw()

    def simple_subtract(event):
        # Interpolate filter to match working file x-axis
        interp_func = scipy.interpolate.interp1d(x_filt, y_filt, kind='linear', 
                                                  bounds_error=False, fill_value=0)
        y_filt_interp = interp_func(modified_data['x'])
        
        # Subtract and don't go below 0
        modified_data['y'] = np.maximum(0, np.array(modified_data['y']) - np.array(y_filt_interp))
        update_plot()

    def smart_subtract(event):
        try:
            window = int(window_size['value'])
            if window < 1:
                window = 25
        except:
            window = 25
            
        # 1. Interpolate filter spectrum to match x-axis
        interp_func = scipy.interpolate.interp1d(
            x_filt, y_filt, kind='linear',
            bounds_error=False, fill_value=0
        )
        y_filt_interp = interp_func(modified_data['x'])

        y_work = np.array(modified_data['y'])
        y_filt_arr = np.array(y_filt_interp)
        n = len(y_work)

        # 2. Compute local scaling β(λ) via sliding-window LS
        beta = np.zeros(n)

        for i in range(n):
            lo = max(0, i - window)
            hi = min(n, i + window + 1)

            bW = y_filt_arr[lo:hi]
            sW = y_work[lo:hi]

            denom = np.dot(bW, bW)
            if denom > 1e-12:
                beta[i] = np.dot(sW, bW) / denom
            else:
                beta[i] = 0.0

        # Optional: smooth β(λ) a bit to avoid noise
        beta = scipy.signal.savgol_filter(beta, 51, 2, mode='mirror')

        # 3. Subtract with wavelength-dependent scaling
        corrected = y_work - beta * y_filt_arr

        # clip negative values
        modified_data['y'] = np.maximum(corrected, 0)

        update_plot()

    def manual_peaks(event):
        # Enable interactive peak modification
        peak_editor = {'selected_peak': None, 'peak_line': None, 'connection_ids': []}
        
        def find_peak_region(center_idx, y_data):
            """Find the extent of a peak around the center index"""
            y_arr = np.array(y_data)
            
            # Find local minima on both sides
            left_idx = center_idx
            right_idx = center_idx
            
            # Search left for minimum
            for i in range(center_idx - 1, max(0, center_idx - 50), -1):
                if y_arr[i] < y_arr[left_idx]:
                    left_idx = i
                elif y_arr[i] < y_arr[left_idx] * 1.1:  # Allow small increases
                    left_idx = i
                else:
                    break
            
            # Search right for minimum
            for i in range(center_idx + 1, min(len(y_arr), center_idx + 50)):
                if y_arr[i] < y_arr[right_idx]:
                    right_idx = i
                elif y_arr[i] < y_arr[right_idx] * 1.1:  # Allow small increases
                    right_idx = i
                else:
                    break
            
            return left_idx, right_idx
        
        def apply_smooth_scaling(indices, scale_factor, y_data):
            """Apply scaling to a peak region with smooth blending at edges"""
            left_idx, right_idx = indices
            y_arr = np.array(y_data)
            
            # Store original baseline values at both edges
            baseline_left = y_arr[left_idx]
            baseline_right = y_arr[right_idx]
            
            # Calculate the peak region relative to baseline
            peak_length = right_idx - left_idx + 1
            blend_width = min(5, peak_length // 4)  # Blend over 5 points or 25% of peak
            
            for i in range(left_idx, right_idx + 1):
                # Calculate distance from edges for blending
                dist_from_left = i - left_idx
                dist_from_right = right_idx - i
                
                # Calculate blend factor (1.0 in center, smoothly to 0 at edges)
                if dist_from_left < blend_width:
                    blend = dist_from_left / blend_width
                elif dist_from_right < blend_width:
                    blend = dist_from_right / blend_width
                else:
                    blend = 1.0
                
                # Interpolate baseline between left and right
                t = (i - left_idx) / max(1, peak_length - 1)  # Position ratio (0 to 1)
                baseline = baseline_left * (1 - t) + baseline_right * t
                
                # Apply scaling with blending
                # Subtract baseline, scale, add baseline back
                relative_height = y_arr[i] - baseline
                scaled_height = relative_height * (1 + (scale_factor - 1) * blend)
                modified_data['y'][i] = max(0, baseline + scaled_height)
            
        
        def update_peak_highlight():
            """Update the visual highlight of the selected peak"""
            if peak_editor['selected_peak'] is None:
                return
            
            left_idx, right_idx = peak_editor['selected_peak']['indices']
            
            # Remove old highlight
            if peak_editor['peak_line'] is not None:
                try:
                    peak_editor['peak_line'].remove()
                except:
                    pass
                peak_editor['peak_line'] = None
            
            # Draw new highlight
            peak_x = [modified_data['x'][i] for i in range(left_idx, right_idx + 1)]
            peak_y = [modified_data['y'][i] for i in range(left_idx, right_idx + 1)]
            peak_editor['peak_line'], = ax.plot(peak_x, peak_y, 'r-', linewidth=3, alpha=0.5, label='Selected Peak')
            ax.legend()
            plt.draw()
        
        def on_click(event_click):
            if event_click.inaxes != ax:
                return
            
            x_click = event_click.xdata
            if x_click is None:
                return
            
            # Remove old highlight if exists
            if peak_editor['peak_line'] is not None:
                try:
                    peak_editor['peak_line'].remove()
                except:
                    pass
                peak_editor['peak_line'] = None
            
            # Find nearest point
            x_arr = np.array(modified_data['x'])
            center_idx = np.argmin(np.abs(x_arr - x_click))
            
            # Find the peak region
            left_idx, right_idx = find_peak_region(center_idx, modified_data['y'])
            
            # Store selected peak
            peak_editor['selected_peak'] = {
                'indices': (left_idx, right_idx),
                'center': center_idx,
                'original_y': [modified_data['y'][i] for i in range(left_idx, right_idx + 1)]
            }
            
            update_peak_highlight()
            
            print(f"Peak selected at index {center_idx} (range: {left_idx}-{right_idx}).")
            print("  LEFT/RIGHT arrows: adjust peak boundaries")
            print("  UP/DOWN arrows: adjust peak intensity")
        
        def on_key(event_key):
            if peak_editor['selected_peak'] is None:
                return
            
            left_idx, right_idx = peak_editor['selected_peak']['indices']
            step = 0.02  # 2% adjustment per key press
            
            if event_key.key == 'left':
                # Expand peak region to the left
                new_left = max(0, left_idx - 1)
                if new_left < left_idx:
                    # Store current zoom
                    xlim = ax.get_xlim()
                    ylim = ax.get_ylim()
                    
                    peak_editor['selected_peak']['indices'] = (new_left, right_idx)
                    update_peak_highlight()
                    
                    # Restore zoom
                    ax.set_xlim(xlim)
                    ax.set_ylim(ylim)
                    print(f"Peak boundary adjusted: {new_left}-{right_idx}")
                    
            elif event_key.key == 'right':
                # Expand peak region to the right
                new_right = min(len(modified_data['y']) - 1, right_idx + 1)
                if new_right > right_idx:
                    # Store current zoom
                    xlim = ax.get_xlim()
                    ylim = ax.get_ylim()
                    
                    peak_editor['selected_peak']['indices'] = (left_idx, new_right)
                    update_peak_highlight()
                    
                    # Restore zoom
                    ax.set_xlim(xlim)
                    ax.set_ylim(ylim)
                    print(f"Peak boundary adjusted: {left_idx}-{new_right}")
                    
            elif event_key.key == 'shift+left':
                # Shrink peak region from the left
                new_left = min(right_idx - 1, left_idx + 1)
                if new_left > left_idx:
                    # Store current zoom
                    xlim = ax.get_xlim()
                    ylim = ax.get_ylim()
                    
                    peak_editor['selected_peak']['indices'] = (new_left, right_idx)
                    update_peak_highlight()
                    
                    # Restore zoom
                    ax.set_xlim(xlim)
                    ax.set_ylim(ylim)
                    print(f"Peak boundary adjusted: {new_left}-{right_idx}")
                    
            elif event_key.key == 'shift+right':
                # Shrink peak region from the right
                new_right = max(left_idx + 1, right_idx - 1)
                if new_right < right_idx:
                    # Store current zoom
                    xlim = ax.get_xlim()
                    ylim = ax.get_ylim()
                    
                    peak_editor['selected_peak']['indices'] = (left_idx, new_right)
                    update_peak_highlight()
                    
                    # Restore zoom
                    ax.set_xlim(xlim)
                    ax.set_ylim(ylim)
                    print(f"Peak boundary adjusted: {left_idx}-{new_right}")
            
            elif event_key.key == 'up':
                # Increase peak intensity with smooth blending
                apply_smooth_scaling(peak_editor['selected_peak']['indices'], 1 + step, modified_data['y'])
                
                # Store current zoom
                xlim = ax.get_xlim()
                ylim = ax.get_ylim()
                
                update_plot()
                update_peak_highlight()
                
                # Restore zoom
                ax.set_xlim(xlim)
                ax.set_ylim(ylim)
                
            elif event_key.key == 'down':
                # Decrease peak intensity with smooth blending
                apply_smooth_scaling(peak_editor['selected_peak']['indices'], 1 - step, modified_data['y'])
                
                # Store current zoom
                xlim = ax.get_xlim()
                ylim = ax.get_ylim()
                
                update_plot()
                update_peak_highlight()
                
                # Restore zoom
                ax.set_xlim(xlim)
                ax.set_ylim(ylim)
                
            elif event_key.key == 'escape':
                # Deselect peak
                if peak_editor['peak_line'] is not None:
                    try:
                        peak_editor['peak_line'].remove()
                    except:
                        pass
                    peak_editor['peak_line'] = None
                peak_editor['selected_peak'] = None
                ax.legend()
                plt.draw()
                print("Peak deselected.")
        
        # Connect events
        cid_click = fig.canvas.mpl_connect('button_press_event', on_click)
        cid_key = fig.canvas.mpl_connect('key_press_event', on_key)
        peak_editor['connection_ids'] = [cid_click, cid_key]
        # Open instruction window
        def show_instructions():
            inst_window = tk.Toplevel()
            inst_window.title('Manual Peak Editing Instructions')
            inst_window.geometry('500x300')
            inst_window.resizable(True, True)
            
            instructions = """
    Manual Peak Editing Instructions:

    SELECTING PEAKS:
    • Click on any peak to select it
    • Selected peak will be highlighted in red

    ADJUSTING PEAK BOUNDARIES:
    • LEFT arrow: Expand peak boundary to the left
    • RIGHT arrow: Expand peak boundary to the right
    • SHIFT+LEFT: Shrink peak boundary from the left
    • SHIFT+RIGHT: Shrink peak boundary from the right

    ADJUSTING PEAK INTENSITY:
    • UP arrow: Increase peak intensity (2% per press)
    • DOWN arrow: Decrease peak intensity (2% per press)

    OTHER CONTROLS:
    • ESC: Deselect current peak
    • Reset button: Restore original data
    • Save button: Save modified spectrum to file
            """
            
            text_widget = tk.Text(inst_window, wrap=tk.WORD, padx=10, pady=10)
            text_widget.pack(fill='both', expand=True)
            text_widget.insert('1.0', instructions)
            text_widget.config(state='disabled')
            
            close_btn = tk.Button(inst_window, text='Close', command=inst_window.destroy)
            close_btn.pack(pady=5)
        
        show_instructions()

    def reset_data(event):
        modified_data['x'] = x_work.copy() if isinstance(x_work, np.ndarray) else list(x_work)
        modified_data['y'] = y_work.copy() if isinstance(y_work, np.ndarray) else list(y_work)
        update_plot()

    def save_modified(event):
        # Open file dialog to save
        save_file = filedialog.asksaveasfilename(
            defaultextension='.txt',
            initialdir=os.path.dirname(WORKING_FILE),
            title='Save Modified File',
            filetypes=[('Text file', '*.txt'), ('All files', '*.*')]
        )
        
        if save_file:
            with open(save_file, 'w') as f:
                for i in range(len(modified_data['x'])):
                    f.write(f"{modified_data['x'][i]}\t{modified_data['y'][i]}\n")
            print(f"File saved: {save_file}")

    # Create buttons
    ax_simple = plt.axes([0.1, 0.05, 0.15, 0.04])
    ax_smart = plt.axes([0.26, 0.05, 0.15, 0.04])
    ax_manual = plt.axes([0.42, 0.05, 0.15, 0.04])
    ax_reset = plt.axes([0.58, 0.05, 0.15, 0.04])
    ax_save = plt.axes([0.74, 0.05, 0.15, 0.04])
    ax_zoom = plt.axes([0.9, 0.05, 0.08, 0.04])
    
    # Create window size input for smart subtract
    ax_window_label = plt.axes([0.1, 0.11, 0.08, 0.03])
    ax_window_input = plt.axes([0.19, 0.11, 0.06, 0.03])
    
    # Add label for window parameter
    ax_window_label.text(0.5, 0.5, 'Window:', ha='center', va='center', fontsize=9)
    ax_window_label.axis('off')
    
    # Create text box for window input
    from matplotlib.widgets import TextBox
    window_textbox = TextBox(ax_window_input, '', initial=str(window_size['value']))
    
    def update_window(text):
        try:
            val = int(text)
            if val > 0:
                window_size['value'] = val
        except:
            pass
    
    window_textbox.on_submit(update_window)

    btn_simple = Button(ax_simple, 'Simple Subtract')
    btn_smart = Button(ax_smart, 'Smart Subtract')
    btn_manual = Button(ax_manual, 'Manual Peaks')
    btn_reset = Button(ax_reset, 'Reset')
    btn_save = Button(ax_save, 'Save')
    btn_zoom = Button(ax_zoom, 'Zoom Out')

    btn_simple.on_clicked(simple_subtract)
    btn_smart.on_clicked(smart_subtract)
    btn_manual.on_clicked(manual_peaks)
    btn_reset.on_clicked(reset_data)
    btn_save.on_clicked(save_modified)
    btn_zoom.on_clicked(lambda event: ax.autoscale(enable=True, axis='both', tight=True) or plt.draw())

    # Initial plot
    update_plot()
    plt.show()

def display_files2(file_list, n=3, start_idx=0):
    if not WORKING_FILE:
        error_message(tk.Tk(), 'No working file loaded')
        return
    if not file_list or len(file_list) == 0:
        error_message(tk.Tk(), 'No files to display')
        return
    files = clear_list(file_list)
    global ax, fig
    
    fig, ax = plt.subplots()
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_xticks([])
    ax.set_yticks([])

    plot_canvas = fig.add_subplot(1, 1, 1)
    plot_canvas.autoscale(enable=True, axis='both', tight=True)



    axnext = plt.axes([0.85, 0.025, 0.1, 0.04])
    axprev = plt.axes([0.75, 0.025, 0.1, 0.04])
    axnextn = plt.axes([0.55, 0.025, 0.15, 0.04])
    axprevn = plt.axes([0.4, 0.025, 0.15, 0.04])
    bnext = Button(axnext, 'Next')
    bprev = Button(axprev, 'Prev')
    bnextn = Button(axnextn, 'Next {} Files'.format(n))
    bprevn = Button(axprevn, 'Prev {} Files'.format(n))
    bnext.on_clicked(lambda event: next_file(1))
    bprev.on_clicked(lambda event: prev_file(1))
    bnextn.on_clicked(lambda event: next_file(n))
    bprevn.on_clicked(lambda event: prev_file(n))

    def plot_files(files, start_idx, n):
        plot_canvas.clear()
        x, y = load_data(WORKING_FILE)
        x, y = gui_norm(x, y)
        name = os.path.basename(WORKING_FILE)
        plot_canvas.plot(x, y, label=name)
        if FILTER_FILE:
            x, y = load_data(FILTER_FILE)
            x, y = gui_norm(x, y)
            name = os.path.basename(FILTER_FILE)
            plot_canvas.plot(x, y, label=name)
        for i in range(n):
            idx = start_idx + i
            if idx < len(files):
                x, y = load_data(files[idx])
                x, y = gui_norm(x, y)
                name = os.path.basename(files[idx])
                plot_canvas.plot(x, y, label=name)
        plot_canvas.legend()
        plt.draw()
        plt.show()

    def next_file(num_files):
        nonlocal start_idx
        start_idx = min(start_idx + num_files, len(files) - n)
        plot_files(files, start_idx, n)

    def prev_file(num_files):
        nonlocal start_idx
        start_idx = max(start_idx - num_files, 0)
        plot_files(files, start_idx, n)

    plot_files(files, start_idx, n)
    #plt.show()




def display_filex(root):
    global WORKING_FILE, USE_INDEXES
    top = tk.Toplevel(root)
    top.title('Display Multiple Spectra - SpeComp')
    top.geometry('600x700')
    top.resizable(True, True)
    top.configure(bg='#f5f6fa')
    top.transient(root)
    top.grab_set()

    # Header
    header_frame = tk.Frame(top, bg='#f5f6fa', padx=15, pady=5)
    header_frame.pack(fill='x')
    
    tk.Label(header_frame, text='📊 Display Multiple Spectra', 
            font=('Segoe UI', 11, 'bold'), bg='#f5f6fa', fg='#2c3e50').pack(anchor='w')

    tk.Frame(top, height=1, bg='#bdc3c7').pack(fill='x', padx=15)

    # Main content
    content_frame = tk.Frame(top, bg='#f5f6fa', padx=15, pady=8)
    content_frame.pack(fill='both', expand=True)

    # Working file section
    work_frame = tk.LabelFrame(content_frame, text='Working File', font=('Segoe UI', 9, 'bold'),
                               bg='#f5f6fa', fg='#2c3e50', padx=10, pady=5)
    work_frame.pack(fill='x', pady=(0, 8))
    
    work_entry = tk.Entry(work_frame, font=('Segoe UI', 8), fg='#2c3e50')
    work_entry.pack(side='left', fill='x', expand=True, padx=(0, 5))
    work_entry.insert(0, WORKING_FILE if WORKING_FILE else '')
    
    def browse_working():
        global X, Y, WORKING_FILE, FILE_LOADED
        file = filedialog.askopenfilename(initialdir=os.path.dirname(WORKING_FILE) if WORKING_FILE else BASE_DIR,
                                         title='Select Working File', filetypes=[('Text files', '*.txt'), ('All files', '*.*')])
        if file:
            WORKING_FILE = file
            FILE_LOADED = True
            x, y = load_data(file)
            X, Y = x, y
            work_entry.delete(0, 'end')
            work_entry.insert(0, file)
    
    tk.Button(work_frame, text='📂', command=browse_working, font=('Segoe UI', 8),
             bg='#3498db', fg='white', relief='flat', padx=8, pady=2, cursor='hand2').pack(side='left')

    # Database section
    db_frame = tk.LabelFrame(content_frame, text='Database Folder', font=('Segoe UI', 9, 'bold'),
                            bg='#f5f6fa', fg='#2c3e50', padx=10, pady=5)
    db_frame.pack(fill='x', pady=(0, 8))
    
    db_entry = tk.Entry(db_frame, font=('Segoe UI', 8), fg='#2c3e50')
    db_entry.pack(side='left', fill='x', expand=True, padx=(0, 5))
    db_entry.insert(0, USE_INDEXES["DB"] if USE_INDEXES["DB"] else '')
    
    def browse_db():
        folder = filedialog.askdirectory(initialdir=USE_INDEXES["DB"] if USE_INDEXES["DB"] else BASE_DIR,
                                        title='Select Database Folder')
        if folder:
            USE_INDEXES["DB"] = folder
            db_entry.delete(0, 'end')
            db_entry.insert(0, folder)
    
    tk.Button(db_frame, text='📁', command=browse_db, font=('Segoe UI', 8),
             bg='#3498db', fg='white', relief='flat', padx=8, pady=2, cursor='hand2').pack(side='left')

    # Spectra list section
    spec_frame = tk.LabelFrame(content_frame, text='Spectra to Display', font=('Segoe UI', 9, 'bold'),
                               bg='#f5f6fa', fg='#2c3e50', padx=8, pady=5)
    spec_frame.pack(fill='both', expand=True, pady=(0, 5))

    tk.Label(spec_frame, text='💡 Paste paths, drag & drop files, or browse results',
            font=('Segoe UI', 8), bg='#f5f6fa', fg='#3498db').pack(anchor='w', pady=(0, 3))

    # Parse results file function
    def parse_results_file(filepath):
        paths = []
        try:
            if filepath.lower().endswith('.csv'):
                with open(filepath, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    next(reader)
                    for row in reader:
                        if len(row) >= 4:
                            full_path = os.path.join(row[2], row[3])
                            if os.path.exists(full_path):
                                paths.append(full_path)
            elif filepath.lower().endswith('.txt'):
                with open(filepath, 'r', encoding='utf-8') as f:
                    db_path = None
                    # First, try to find the database folder path
                    content = f.read()
                    f.seek(0)
                    
                    for line in content.split('\n'):
                        if line.strip().startswith('Database folder:'):
                            db_path = line.split('Database folder:', 1)[1].strip()
                            break
                    
                    # Parse spectrum lines
                    for line in content.split('\n'):
                        line_stripped = line.strip()
                        # Look for lines like "  1. filename.txt (Score: 28.0050)"
                        if '(Score:' in line_stripped and '. ' in line_stripped:
                            # Remove the rank number (e.g., "1. ")
                            parts = line_stripped.split('. ', 1)
                            if len(parts) >= 2:
                                # Extract filename (everything before " (Score:")
                                filename_part = parts[1].split(' (Score:')[0].strip()
                                
                                if db_path and filename_part:
                                    full_path = os.path.join(db_path, filename_part)
                                    if os.path.exists(full_path):
                                        paths.append(full_path)
        except Exception as e:
            error_message(top, f'Error parsing file: {str(e)}')
        return paths

    def browse_results():
        file = filedialog.askopenfilename(initialdir=BASE_DIR, title='Select Results File',
                                         filetypes=[('Results files', '*.txt *.csv'), ('All files', '*.*')])
        if file:
            paths = parse_results_file(file)
            if paths:
                txt.delete('1.0', 'end')
                txt.insert('1.0', '\n'.join(paths))
            else:
                error_message(top, 'No valid spectrum paths found in file')

    # Buttons row
    btn_frame = tk.Frame(spec_frame, bg='#f5f6fa')
    btn_frame.pack(fill='x', pady=(0, 5))
    
    tk.Button(btn_frame, text='📁 Load Results File', command=browse_results, font=('Segoe UI', 8),
             bg='#3498db', fg='white', relief='flat', padx=10, pady=3, cursor='hand2').pack(side='left', padx=(0, 5))

    conf_btn = tk.Button(btn_frame, text='⚙️ Config', command=lambda: configuration_display(top),
                        font=('Segoe UI', 8), bg='#95a5a6', fg='white', relief='flat', 
                        padx=10, pady=3, cursor='hand2')
    conf_btn.pack(side='left', padx=5)

    display_btn = tk.Button(btn_frame, text='📈 Display', 
                           command=lambda: display_files2(txt.get('1.0', 'end').splitlines()),
                           font=('Segoe UI', 8, 'bold'), bg='#3498db', fg='white', 
                           relief='flat', padx=15, pady=3, cursor='hand2')
    display_btn.pack(side='left', padx=5)

    # Hover effects
    conf_btn.bind("<Enter>", lambda e: conf_btn.config(bg='#7f8c8d'))
    conf_btn.bind("<Leave>", lambda e: conf_btn.config(bg='#95a5a6'))
    display_btn.bind("<Enter>", lambda e: display_btn.config(bg='#2980b9'))
    display_btn.bind("<Leave>", lambda e: display_btn.config(bg='#3498db'))

    # Text area
    txt_frm = tk.Frame(spec_frame, bg='#ffffff', relief='solid', bd=1)
    txt_frm.pack(fill='both', expand=True)
    txt_frm.grid_rowconfigure(0, weight=1)
    txt_frm.grid_columnconfigure(0, weight=1)

    txt = tk.Text(txt_frm, borderwidth=0, relief='flat', font=('Consolas', 8),
                 bg='#ffffff', fg='#2c3e50', wrap='none', padx=8, pady=8, height=6)
    txt.grid(row=0, column=0, sticky='nsew')

    scrollb = tk.Scrollbar(txt_frm, command=txt.yview)
    scrollb.grid(row=0, column=1, sticky='nsew')
    txt['yscrollcommand'] = scrollb.set

    # Drag and drop
    def on_drop(event):
        for file in top.tk.splitlist(event.data):
            file = file.strip('{}')
            if file.lower().endswith(('.txt', '.csv')):
                paths = parse_results_file(file)
                if paths:
                    if txt.get('1.0', 'end').strip():
                        txt.insert('end', '\n')
                    txt.insert('end', '\n'.join(paths))
            else:
                if txt.get('1.0', 'end').strip():
                    txt.insert('end', '\n')
                txt.insert('end', file)

    txt_frm.drop_target_register('DND_Files')
    txt_frm.dnd_bind('<<Drop>>', on_drop)
    txt.drop_target_register('DND_Files')
    txt.dnd_bind('<<Drop>>', on_drop)

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

def select_file(root, display = False, file_box = None,):        
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

def select_filter_file(root, file_box):
    global FILTER_FILE
    base_dir = os.getcwd()
    if FILTER_FILE:
        base_dir = os.path.dirname(FILTER_FILE)
    file = filedialog.askopenfilename(initialdir= base_dir, title='Select File',
                                        filetypes=(('txt files', '*.txt'), ('all files', '*.*')))
    FILTER_FILE = file
    #refresh the file box
    if file_box:
        file_box.delete(0, 'end')
        file_box.insert(0, os.path.basename(FILTER_FILE))

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


def filter_subtraction(root):
    global WORKING_FILE, FILTER_FILE
    # check if working file and filter file are loaded
    if WORKING_FILE is None or FILTER_FILE is None:
        error_message(root, "working file and filter missing")
        return
    display_subtraction()

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