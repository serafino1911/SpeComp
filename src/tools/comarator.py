import numpy as np
import os
import scipy
import scipy.interpolate

def load_data(path):
    with open(path, 'r') as f:
        data = f.readlines()
        data = [line.split() for line in data]
        x = [float(line[0]) for line in data]
        y = [float(line[1]) for line in data]
    return x, y


def compare_timeseries_correlation(x_1 : list, y_1 : list, x_2 : list, y_2 : list):
    # differnte lenght
    if len(x_1) != len(y_1) or len(x_2) != len(y_2):
        return 0
    # find same intervall
    x_min = max(x_1[0], x_2[0])
    x_max = min(x_1[-1], x_2[-1])
    # find index
    i_min = 0
    i_max = 0
    for i in range(len(x_1)):
        if x_1[i] >= x_min:
            i_min = i
            break
    for i in range(len(x_2)):
        if x_2[i] >= x_min:
            i_min = i
            break
    for i in range(len(x_1)):
        if x_1[i] >= x_max:
            i_max = i
            break
    for i in range(len(x_2)):
        if x_2[i] >= x_max:
            i_max = i
            break
    # cut
    x_1 = x_1[i_min:i_max]
    y_1 = y_1[i_min:i_max]
    x_2 = x_2[i_min:i_max]
    y_2 = y_2[i_min:i_max]
    #resample to same length
    y_1 = np.linspace(y_1[0], y_1[-1], len(y_2))


    corr = np.corrcoef(y_1, y_2)[0, 1]
    return corr


def discrete_correlation(x_1 : list, y_1 : list, x_2 : list, y_2 : list):
    # differnte lenght
    if len(x_1) != len(y_1) or len(x_2) != len(y_2):
        return 0
    # find same intervall
    x_min = max(x_1[0], x_2[0])
    x_max = min(x_1[-1], x_2[-1])
    # find index
    i_min = 0
    i_max = 0
    for i in range(len(x_1)):
        if x_1[i] >= x_min:
            i_min = i
            break
    for i in range(len(x_2)):
        if x_2[i] >= x_min:
            i_min = i
            break
    for i in range(len(x_1)):
        if x_1[i] >= x_max:
            i_max = i
            break
    for i in range(len(x_2)):
        if x_2[i] >= x_max:
            i_max = i
            break
    # cut
    x_1 = x_1[i_min:i_max]
    y_1 = y_1[i_min:i_max]
    x_2 = x_2[i_min:i_max]
    y_2 = y_2[i_min:i_max]
    #interpolate to same x values
    #y_1 = np.interp(x_2, x_1, y_1)
    #scipy interpolation
    f = scipy.interpolate.interp1d(x_1, y_1, fill_value="extrapolate")
    y_1 = f(x_2)

    #y_2 = np.interp(x_1, x_2, y_2)
    #resample to same length
    #y_1 = np.linspace(y_1[0], y_1[-1], len(y_2))
    #calculate correlation
    corr = np.corrcoef(y_1, y_2)[0,1]
    return np.abs(corr)


def compare(path1, file_list):
    file_results = []
    x_u, y_u = load_data(path1)
    for file in file_list:
        x2, y2 = load_data(file)

        corr = discrete_correlation(x_u, y_u, x2, y2)
        file_results.append((file, corr))
    #sort by correlation
    file_results.sort(key=lambda x: x[1], reverse=True)
    return file_results


BASE_DIR = 'data\\DB'
unknown = 'data\\Unknown\\EXE.txt'
file_list = []
for root, dirs, files in os.walk(BASE_DIR):
    file_list.extend(os.path.join(root, file) for file in files if file.endswith('.txt'))

results = compare(unknown,file_list)
print(results)
#take first and plot it
import matplotlib.pyplot as plt
x_u, y_u = load_data(unknown)
x2, y2 = load_data(results[0][0])
plt.plot(x_u, y_u, label='unknown')
plt.plot(x2, y2, label='known')
plt.legend()
plt.show()




