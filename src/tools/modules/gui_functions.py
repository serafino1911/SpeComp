from modules.importer import *

OPEN_CONFIG = False

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
    


def display_graph(root, graph):
    graph = tk.Canvas(root, width=200, height=100)
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
    file.add_command(label='Open..', command=hello)
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

