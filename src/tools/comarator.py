import numpy as np
import os
import scipy.signal
import scipy.interpolate
import math as m

def load_data(path):
    with open(path, 'r') as f:
        data = f.readlines()
        data = [line.split() for line in data]
        x = [float(line[0]) for line in data]
        y = [float(line[1]) for line in data]
    return x, y

def clear_y(y_test):
    k = np.min(y_test)
    y_test = [y-k for y in y_test]
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
    y_1 = np.interp(new_x_1, x_1, y_1)
    y_2 = np.interp(new_x_2, x_2, y_2)
    f = scipy.interpolate.interp1d(new_x_1, y_1, fill_value="extrapolate")
    y_1 = f(new_x_2)
    return y_1, y_2, new_x_1, new_x_2

def pre_elaboration(x_1_i : list, y_1_i : list, x_2_i : list, y_2_i : list, divdelta : float = 1):
    x_1, y_1, x_2, y_2 = select_intervall(x_1_i, y_1_i, x_2_i, y_2_i)
    y_1 = clear_y(y_1)
    y_2 = clear_y(y_2)
    y_1, y_2, x_1, x_2 = same_x_projection(x_1, y_1, x_2, y_2, divdelta)
    return x_1, y_1, x_2, y_2

def convolution(y_1 : list,y_2 : list):
    #corr = np.correlate(y_1, y_2, mode='same')
    conv = np.convolve(y_1, y_2, mode='same')
    return np.max(conv) #np.trapz(corr)

def compare_HQI(y_1 : list, y_2 : list):
    # x_1, y_1, x_2, y_2 = select_intervall(x_1, y_1, x_2, y_2)
    # y_1 = clear_y(y_1)
    # y_2 = clear_y(y_2)
    # y_1, y_2, x_1, x_2  = same_x_projection(x_1, y_1, x_2, y_2, 4)
    hqi = round((m.pow(np.dot(y_2,y_1),2))/(np.dot(y_2,y_2)*np.dot(y_1,y_1)),2)
    return hqi

def compare_timeseries_correlation(y_1 : list, y_2 : list):
    # fast convolution
    conv = scipy.signal.fftconvolve(y_1, y_2[::-1], mode='same')
    return np.max(np.abs(conv))

def norm_correlation(y_1 : list, y_2 : list):
    # x_1, y_1, x_2, y_2 = select_intervall(x_1, y_1, x_2, y_2)
    # #resample to same length
    # y_1 = clear_y(y_1)
    # y_2 = clear_y(y_2)
    # y_1, y_2, x_1, x_2  = same_x_projection(x_1, y_1, x_2, y_2, 4)    
    #normalize
    y_1 = y_1/np.max(y_1)
    y_2 = y_2/np.max(y_2)
    return np.corrcoef(y_1, y_2)[0, 1]

def discrete_correlation(y_1 : list, y_2 : list):
    # x_1, y_1, x_2, y_2 = select_intervall(x_1, y_1, x_2, y_2)
    # y_1 = clear_y(y_1)
    # y_2 = clear_y(y_2)
    # y_1, y_2, x_1, x_2  = same_x_projection(x_1, y_1, x_2, y_2, 4)
    corr = np.corrcoef(y_1, y_2)[0,1]
    return np.abs(corr)

def compare(path1, file_list):
    result_norm = []
    result_discr = []
    result_conv = []
    result_HQI = []
    result_timese = []

    x_u_i, y_u_i = load_data(path1)
    for file in file_list:
        x2, y2 = load_data(file)
        x_u, y_u, x2, y2 = pre_elaboration(x_u_i, y_u_i, x2, y2, 2)
        corr_norm = norm_correlation(y_u, y2) 
        corr_conv = convolution(y_u, y2) 
        corr_HQI = compare_HQI(y_u, y2)
        corr_discr = discrete_correlation(y_u, y2)
        corr_timese = compare_timeseries_correlation(y_u, y2) #fft convolution
        result_norm.append((file, corr_norm))
        result_conv.append((file, corr_conv))
        result_HQI.append((file, corr_HQI))
        result_discr.append((file, corr_discr))
        result_timese.append((file, corr_timese))
    #sort by correlation
    result_norm.sort(key=lambda x: x[1], reverse=True)
    result_conv.sort(key=lambda x: x[1], reverse=True)
    result_HQI.sort(key=lambda x: x[1], reverse=True)
    result_discr.sort(key=lambda x: x[1], reverse=True)
    result_timese.sort(key=lambda x: x[1], reverse=True)
    return result_norm, result_conv, result_HQI, result_discr, result_timese


BASE_DIR = 'data\\DB'
unknown = 'data\\Unknown\\EXE.txt'
file_list = []
for root, dirs, files in os.walk(BASE_DIR):
    file_list.extend(os.path.join(root, file) for file in files if file.endswith('.txt'))

result_norm, result_conv, result_HQI, result_discr, result_timese = compare(unknown,file_list)
print('NORM: ', result_norm[:5])
print('CONV: ', result_conv[:5])
print('HQI: ', result_HQI[:5])
print('DISCR: ', result_discr[:5])
print('FFT CONV: ', result_timese[:5])

#take first and plot it
import matplotlib.pyplot as plt
x_u, y_u = load_data(unknown)
x_ultra, y_ultra = load_data(result_norm[0][0])
x_conv, y_conv = load_data(result_conv[0][0])
x_HQI, y_HQI = load_data(result_HQI[0][0])
x_discr, y_discr = load_data(result_discr[0][0])
x_timese, y_timese = load_data(result_timese[0][0])
name_ultra = result_norm[0][0].split('\\')[-1].replace('.txt', '').replace(' ', '')
name_conv = result_conv[0][0].split('\\')[-1].replace('.txt', '').replace(' ', '')
name_HQI = result_HQI[0][0].split('\\')[-1].replace('.txt', '').replace(' ', '')
name_discr = result_discr[0][0].split('\\')[-1].replace('.txt', '').replace(' ', '')
name_timese = result_timese[0][0].split('\\')[-1].replace('.txt', '').replace(' ', '')

# normalize data
u = np.min(y_u)
y_u = [y-u for y in y_u]
y_u = y_u/np.max(y_u)

u = np.min(y_ultra)
y_ultra = [y-u for y in y_ultra]
y_ultra = y_ultra/np.max(y_ultra)

u = np.min(y_conv)
y_conv = [y-u for y in y_conv]
y_conv = y_conv/np.max(y_conv)

u = np.min(y_HQI)
y_HQI = [y-u for y in y_HQI]
y_HQI = y_HQI/np.max(y_HQI)

u = np.min(y_discr)
y_discr = [y-u for y in y_discr]
y_discr = y_discr/np.max(y_discr)

u = np.min(y_timese)
y_timese = [y-u for y in y_timese]
y_timese = y_timese/np.max(y_timese)

plt.plot(x_u, y_u, label='unknown')
plt.plot(x_ultra, y_ultra, label=f'ultra {name_ultra}')
plt.plot(x_conv, y_conv, label=f'conv {name_conv}')
plt.plot(x_HQI, y_HQI, label=f'HQI {name_HQI}')
plt.plot(x_discr, y_discr, label=f'discr {name_discr}')
plt.plot(x_timese, y_timese, label=f'timese {name_timese}')

plt.legend()
plt.show()




