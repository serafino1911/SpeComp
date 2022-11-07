from .modules.importer import *
from .modules.basic_functions import *

BASE_DIR = 'data\\DB'

def find_peaks(y_1 : list, y_2 : list):
    peaks_1 = scipy.signal.find_peaks(y_1, height=0.5, distance=10)
    peaks_2 = scipy.signal.find_peaks(y_2, height=0.5, distance=10)
    #indexis peaks
    peaks_1_indexs = peaks_1[0]
    peaks_2_indexs = peaks_2[0]
    #valori peaks
    peaks_1_val = [y_1[i] for i in peaks_1]
    peaks_2_val = [y_2[i] for i in peaks_2]
    #distanze tra i picchi
    peaks_1_dist = [peaks_1[i+1]-peaks_1[i] for i in range(len(peaks_1)-1)]
    peaks_2_dist = [peaks_2[i+1]-peaks_2[i] for i in range(len(peaks_2)-1)]
    #picchi più vicini tra i due
    peaks_b = [peaks_1[i] for i in range(len(peaks_1)) if peaks_1[i] in peaks_2]

def compare(path1, file_list):
    result = []

    x_u_i, y_u_i = load_data(path1)
    for file in file_list:
        x2, y2 = load_data(file)
        x_u, y_u, x2, y2 = pre_elaboration(x_u_i, y_u_i, x2, y2, 2)
        corr = find_peaks(y_u, y2) 
        result.append((file, round(corr,3)))
    return result

def main(unknown : str):    
    file_list = database_files(BASE_DIR)
    result  = compare(unknown,file_list)
    print('TEST: ', result[:5])
    #take first and plot it
    
    x_u, y_u = load_data(unknown)
    x_test, y_test = load_data(result[0][0])
    name = result[0][0].split('\\')[-1].replace('.txt', '').replace(' ', '')

    # normalize data
    u = np.min(y_u)
    y_u = [y-u for y in y_u]
    y_u /= np.max(y_u)

    u = np.min(y_test)
    y_test = [y-u for y in y_test]
    y_test /= np.max(y_test)

    # plot
    plt.plot(x_u, y_u, label='unknown')
    plt.plot(x_test, y_test, label=name)
    plt.legend()
    plt.show()

if __name__ == '__main__':
    import glob
    unknown_list = glob.glob('data\\unknown\\*.txt')
    #unknown = 'data\\Unknown\\EXE.txt'
    for unknown in unknown_list:
        main(unknown)