from modules.importer import *
from modules.basic_functions import *

OPEN_CONFIG = False
X, Y = None, None
FILE_LOADED = False

def hello():
    print('hello!')

def clear_checks(data):
    for check in data:
        check.deselect()


def load_config(root, data):
    global OPEN_CONFIG
    check_box = data[0]
    if check_box.get():
        print('check_box is checked')
    else:
        print('check_box is not checked')
    root.destroy()
    OPEN_CONFIG = False
    #print the value of the checks

def configuration_window(root):
    global OPEN_CONFIG
    OPEN_CONFIG = True
    top = tk.Toplevel(root)
    top.title('Configuration')
    top.geometry('400x400')
    top.resizable(True, True)

    # check boxes
    check1_var = tk.BooleanVar()
    check1 = tk.Checkbutton(top, text='Check 1', variable=check1_var)
    check1.grid(row=0, column=0, sticky='w')

    check2_var = tk.BooleanVar()
    check2 = tk.Checkbutton(top, text='Check 2', variable=check2_var)
    check2.grid(row=1, column=0, sticky='w')

    check3_var = tk.BooleanVar()
    check3 = tk.Checkbutton(top, text='Check 3', variable=check3_var)
    check3.grid(row=2, column=0, sticky='w')


    # save the checks
    data = [check1_var, check2_var, check3_var]
    boxes = [check1, check2, check3]

    # clear button
    clear_button = tk.Button(top, text='Clear', command=lambda : clear_checks(boxes))
    clear_button.grid(row=3, column=1)


    #close button


    close_button = tk.Button(top, text='Load', command=lambda : load_config(top, data))
    close_button.grid(row=3, column=0)
    


def display_graph(root):
    if graph is not None:
        print('no graph')

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

def up_menu(root):
    menu = tk.Menu(root)
    root.config(menu=menu)

    #create the file object)
    file = tk.Menu(menu)

    #adds a command to the menu option, calling it exit, and the
    #command it runs on event is client_exit
    file.add_command(label='Open..', command=lambda : select_file(root))
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

def select_file(root):        
    global X, Y
    global FILE_LOADED
    file = filedialog.askopenfilename(initialdir='/', title='Select File',
                                        filetypes=(('csv files', '*.csv'), ('all files', '*.*')))
    x,y = load_data(file)
    X, Y = x, y
    FILE_LOADED = True
    


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



