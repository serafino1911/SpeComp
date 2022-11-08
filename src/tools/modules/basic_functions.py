from modules.importer import *

def database_files(base_dir):
    file_list = []
    for root, dirs, files in os.walk(base_dir):
        file_list.extend(os.path.join(root, file) for file in files if file.endswith('.txt'))
    return file_list

def load_data(path):
    with open(path, 'r') as f:
        data = f.readlines()
        data = [line.split() for line in data]
        x = [float(line[0]) for line in data]
        y = [float(line[1]) for line in data]
    return x, y

def clear_y(y_test, guassian_filter : int = 0, normalization : str = 'MinMax'):
    if guassian_filter:
        y_test = scipy.ndimage.filters.gaussian_filter1d(y_test, guassian_filter) 
    if normalization == 'MinMax':
        minim = np.min(y_test)
        maxim = np.max(y_test)
        y_test = [y - minim for y in y_test] / maxim
    elif normalization == 'Stat':
        y_test = (y_test - np.mean(y_test)) / np.std(y_test)
    return y_test


def select_intervall(x_1, y_1, x_2, y_2):
    if len(x_1) != len(y_1) or len(x_2) != len(y_2):
        return 0
    # find same intervall
    x_min = max(x_1[0], x_2[0])
    x_max = min(x_1[-1], x_2[-1])
    i_min = next((i for i in range(len(x_1)) if x_1[i] >= x_min), 0)
    for i in range(len(x_2)):
        if x_2[i] >= x_min:
            i_min = i
            break
    i_max = next((i for i in range(len(x_1)) if x_1[i] >= x_max), 0)
    for i in range(len(x_2)):
        if x_2[i] >= x_max:
            i_max = i
            break
    # cut
    x_1 = x_1[i_min:i_max]
    y_1 = y_1[i_min:i_max]
    x_2 = x_2[i_min:i_max]
    y_2 = y_2[i_min:i_max]
    return x_1, y_1, x_2, y_2

def same_x_projection(x_1, y_1, x_2, y_2, deltaspace = 2):
    min_delta_x1 = min(x_1[i+1]-x_1[i] for i in range(len(x_1)-1))
    min_delta_x2 = min(x_2[i+1]-x_2[i] for i in range(len(x_2)-1))
    min_delta_x = min(min_delta_x1, min_delta_x2)
    new_x_1 = np.arange(x_1[0], x_1[-1], min_delta_x/deltaspace)
    new_x_2 = np.arange(x_2[0], x_2[-1], min_delta_x/deltaspace)
    y_1 = np.interp(new_x_2, x_1, y_1)
    y_2 = np.interp(new_x_2, x_2, y_2)
    return y_1, y_2, new_x_1, new_x_2

def pre_elaboration(x_1_i : list, y_1_i : list, x_2_i : list, y_2_i : list, divdelta : float = 1):
    x_1, y_1, x_2, y_2 = select_intervall(x_1_i, y_1_i, x_2_i, y_2_i)
    y_1 = clear_y(y_1, guassian_filter = 1, normalization = 'Stat')
    y_2 = clear_y(y_2, guassian_filter = 1, normalization = 'Stat')
    y_1, y_2, x_1, x_2 = same_x_projection(x_1, y_1, x_2, y_2, divdelta)
    return x_1, y_1, x_2, y_2