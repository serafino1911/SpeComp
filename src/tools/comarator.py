from modules.importer import *
from modules.basic_functions import *

BASE_DIR = 'data\\DB'

def convolution(y_1 : list,y_2 : list) -> float:
    """
    convolution of spectra

    Args:
        y_1 (list): spectrum 1 as list of floats
        y_2 (list): spectrum 2 as list of floats

    Returns:
        float: max of the convolution
    """
    conv = np.convolve(y_1, y_2, mode='same')
    return np.max(conv)

def compare_HQI(y_1 : list, y_2 : list) -> float:
    """ 
    HQI correlation of spectra

    Args:
        y_1 (list): spectrum 1 as list of floats
        y_2 (list): spectrum 2 as list of floats

    Returns:
        float: HQI
    """
    hqi = round((m.pow(np.dot(y_2,y_1),2))/(np.dot(y_2,y_2)*np.dot(y_1,y_1)),2)
    return hqi

def fft_convolution(y_1 : list, y_2 : list) -> float:
    """
    fft convolution of spectra (convolution through the fourier transform)

    Args:
        y_1 (list): spectrum 1 as list of floats
        y_2 (list): spectrum 2 as list of floats

    Returns:
        float: max of the convolution
    """
    # fast convolution
    conv = scipy.signal.fftconvolve(y_1, y_2[::-1], mode='same')
    return np.max(np.abs(conv))

def norm_correlation(y_1 : list, y_2 : list) -> float:
    """
    normalized correlation of spectra using the function np.corrcoef

    Args:
        y_1 (list): spectrum 1 as list of floats
        y_2 (list): spectrum 2 as list of floats

    Returns:
        float: normalized correlation
    """
    # standar deviation normalization
    return np.abs(np.corrcoef(y_1, y_2)[0, 1])

def discrete_correlation(y_1 : list, y_2 : list):
    """
    discrete correlation of spectra

    Args:
        y_1 (list): spectrum 1 as list of floats
        y_2 (list): spectrum 2 as list of floats

    Returns:
        float: discrete correlation
    """
    corr = np.corrcoef(y_1, y_2)[0,1]
    return np.abs(corr)

def correlate_correlation(y_1 : list, y_2 : list):
    """
    integral of the correlation of spectra

    Args:
        y_1 (list): spectrum 1 as list of floats
        y_2 (list): spectrum 2 as list of floats

    Returns:
        float: integral of the correlation
    """
    corr = np.correlate(y_1, y_2, mode='same')
    return np.trapz(corr)

def difference(y_1 : list, y_2 : list):
    """
    Calcultate the difference between two spectra normalized by the length of the spectra

    Args:
        y_1 (list): spectrum 1 as list of floats
        y_2 (list): spectrum 2 as list of floats

    Returns:
        float: difference
    """
    diff = np.sum(np.abs([x-y for x,y in zip(y_1, y_2)]))
    return(np.abs(diff)/len(y_1))


def compare(path1, file_list):
    result_norm = []
    result_discr = []
    result_conv = []
    result_HQI = []
    result_fftconv = []
    result_correlate = []
    result_diff = []

    x_u_i, y_u_i = load_data(path1)
    for file in file_list:
        x2, y2 = load_data(file)
        x_u, y_u, x2, y2 = pre_elaboration(x_u_i, y_u_i, x2, y2, 1)
        corr_norm = norm_correlation(y_u, y2) 
        corr_conv = convolution(y_u, y2) 
        corr_HQI = compare_HQI(y_u, y2)
        corr_discr = discrete_correlation(y_u, y2)
        corr_fftconv = fft_convolution(y_u, y2) #fft convolution
        corr_correlate = correlate_correlation(y_u, y2)
        corr_diff = difference(y_u, y2)
        result_norm.append((file, round(corr_norm,3)))
        result_conv.append((file, round(corr_conv,3)))
        result_HQI.append((file, round(corr_HQI,3)))
        result_discr.append((file, round(corr_discr,3)))
        result_fftconv.append((file, round(corr_fftconv,3)))
        result_correlate.append((file, round(corr_correlate,3)))
        result_diff.append((file, round(corr_diff,3)))
    #sort by correlation
    result_norm.sort(key=lambda x: x[1], reverse=True)
    result_conv.sort(key=lambda x: x[1], reverse=True)
    result_HQI.sort(key=lambda x: x[1], reverse=True)
    result_discr.sort(key=lambda x: x[1], reverse=True)
    result_fftconv.sort(key=lambda x: x[1], reverse=True)
    result_correlate.sort(key=lambda x: x[1], reverse=True)
    result_diff.sort(key = lambda x : x[1], reverse=False)
    return result_norm, result_conv, result_HQI, result_discr, result_fftconv, result_correlate, result_diff

def main(unknown : str):    
    file_list = database_files(BASE_DIR)
    result_norm, result_conv, result_HQI, result_discr, result_fftconv, result_correlate, result_diff  = compare(unknown,file_list)
    print('NORM: ', result_norm[:5])
    print('CONV: ', result_conv[:5])
    print('HQI: ', result_HQI[:5])
    print('DISCR: ', result_discr[:5])
    print('FFT CONV: ', result_fftconv[:5])
    print('CORRELATE: ', result_correlate[:5])
    print('DIFF: ', result_diff[:5])

    file_name = unknown.split('\\')[-1]
    #save results
    with open(f'reports\\results_{file_name}', 'w') as f:
        f.write('NORM: \n\t' + '\n\t'.join( [ str(val[0]) + ' = ' + str(val[1]) for val in result_norm[:5]] ) + ' \n\n')
        f.write('CONV: \n\t' + '\n\t'.join( [ str(val[0]) + ' = ' + str(val[1]) for val in result_conv[:5]] ) + ' \n\n')
        f.write('HQI: \n\t' + '\n\t'.join( [ str(val[0]) + ' = ' + str(val[1]) for val in result_HQI[:5]] ) + ' \n\n')
        f.write('DISCR: \n\t' + '\n\t'.join( [ str(val[0]) + ' = ' + str(val[1]) for val in result_discr[:5]] ) + ' \n\n')
        f.write('FFT CONV: \n\t' + '\n\t'.join( [ str(val[0]) + ' = ' + str(val[1]) for val in result_fftconv[:5]] ) + ' \n\n')
        f.write('CORRELATE: \n\t' + '\n\t'.join( [ str(val[0]) + ' = ' + str(val[1]) for val in result_correlate[:5]] ) + ' \n\n')
        f.write('DIFF: \n\t' + '\n\t'.join( [ str(val[0]) + ' = ' + str(val[1]) for val in result_diff[:5]] ) + ' \n\n')


    #take first and plot it
    
    x_u, y_u = load_data(unknown)
    x_norm, y_norm = load_data(result_norm[0][0])
    x_conv, y_conv = load_data(result_conv[0][0])
    x_HQI, y_HQI = load_data(result_HQI[0][0])
    x_discr, y_discr = load_data(result_discr[0][0])
    x_fftconv, y_fftconv = load_data(result_fftconv[0][0])
    x_correlate, y_correlate = load_data(result_correlate[0][0])
    x_diff, y_diff = load_data(result_diff[0][0])
    name_norm = result_norm[0][0].split('\\')[-1].replace('.txt', '').replace(' ', '')
    name_conv = result_conv[0][0].split('\\')[-1].replace('.txt', '').replace(' ', '')
    name_HQI = result_HQI[0][0].split('\\')[-1].replace('.txt', '').replace(' ', '')
    name_discr = result_discr[0][0].split('\\')[-1].replace('.txt', '').replace(' ', '')
    name_fftconv = result_fftconv[0][0].split('\\')[-1].replace('.txt', '').replace(' ', '')
    name_correlate = result_correlate[0][0].split('\\')[-1].replace('.txt', '').replace(' ', '')
    name_diff = result_diff[0][0].split('\\')[-1].replace('.txt', '').replace(' ', '')

    # normalize data
    u = np.min(y_u)
    y_u = [y-u for y in y_u]
    y_u /= np.max(y_u)

    u = np.min(y_norm)
    y_norm = [y-u for y in y_norm]
    y_norm /= np.max(y_norm)

    u = np.min(y_conv)
    y_conv = [y-u for y in y_conv]
    y_conv /= np.max(y_conv)

    u = np.min(y_HQI)
    y_HQI = [y-u for y in y_HQI]
    y_HQI /= np.max(y_HQI)

    u = np.min(y_discr)
    y_discr = [y-u for y in y_discr]
    y_discr /= np.max(y_discr)

    u = np.min(y_fftconv)
    y_fftconv = [y-u for y in y_fftconv]
    y_fftconv /= np.max(y_fftconv)

    u = np.min(y_correlate)
    y_correlate = [y-u for y in y_correlate]
    y_correlate /= np.max(y_correlate)

    u = np.min(y_diff)
    y_diff = [y-u for y in y_diff]
    y_diff /= np.max(y_diff)

    # plot as subplots
    fig, axs = plt.subplots(4, 2, figsize=(15, 15))
    axs[0,0].plot(x_u, y_u, label='unknown')
    axs[0,0].plot(x_norm, y_norm, label=name_norm)
    axs[0,0].set_title('norm')
    axs[0,0].legend()
    axs[0,1].plot(x_u, y_u, label='unknown')
    axs[0,1].plot(x_conv, y_conv, label=name_conv)
    axs[0,1].set_title('conv')
    axs[0,1].legend()
    axs[1,0].plot(x_u, y_u, label='unknown')
    axs[1,0].plot(x_HQI, y_HQI, label=name_HQI)
    axs[1,0].set_title('HQI')
    axs[1,0].legend()
    axs[1,1].plot(x_u, y_u, label='unknown')
    axs[1,1].plot(x_discr, y_discr, label=name_discr)
    axs[1,1].set_title('discr')
    axs[1,1].legend()
    axs[2,0].plot(x_u, y_u, label='unknown')
    axs[2,0].plot(x_fftconv, y_fftconv, label=name_fftconv)
    axs[2,0].set_title('fftconv')
    axs[2,0].legend()
    axs[2,1].plot(x_u, y_u, label='unknown')
    axs[2,1].plot(x_correlate, y_correlate, label=name_correlate)
    axs[2,1].set_title('correlate')
    axs[2,1].legend()
    axs[3,0].plot(x_u, y_u, label='unknown')
    axs[3,0].plot(x_diff, y_diff, label=name_diff)
    axs[3,0].set_title('diff')
    axs[3,0].legend()
    plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
    name_file = unknown.split('\\')[-1].replace('.txt', '').replace(' ', '')
    plt.savefig(f'reports\\figures\\result_delta1_{name_file}.png', dpi=300)
    #plt.show()
    #close
    plt.close()

if __name__ == '__main__':
    import glob
    unknown_list = glob.glob('data\\unknown\\*.txt')
    #unknown = 'data\\Unknown\\EXE.txt'
    for unknown in unknown_list:
        main(unknown)
