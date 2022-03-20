from cProfile import label
import matplotlib.pyplot as plt
import numpy as np


def plot_array(array):

    fig, ax = plt.subplots()

    for sample in array:
        ax.plot(np.arange(array.shape[1]), sample)
    
    plt.show()


if __name__ == '__main__':

    spectrum_non_scarifie = np.load("data/numpy_arrays/spectrum_non_scarifie.npy")
    spectrum_scarifie = np.load("data/numpy_arrays/spectrum_scarifie.npy")
    spectrum_background = np.load("data/numpy_arrays/spectrum_background.npy")

    # nmf custom init
    Hp = np.vstack((spectrum_non_scarifie, spectrum_scarifie, spectrum_background))
    Hp[Hp<0] = 0

    # Hp figure
    fig, ax = plt.subplots()

    ax.set_xlabel('wavelength [nm]')
    ax.set_ylabel('intensity [arb.u.]')

    ax.plot(np.arange(350, 1001), spectrum_scarifie, label="scarified")
    ax.plot(np.arange(350, 1001), spectrum_non_scarifie, label="non-scarified")
    ax.plot(np.arange(350, 1001), spectrum_background, label="background")

    ax.tick_params(direction='in')

    plt.legend()
    plt.show()

    fig_data = np.load("data/figures/fig_data.npy")
    table_data = np.load("data/figures/table_data.npy")

    print(table_data)

    # scarified fraction figure
    fig, ax = plt.subplots()

    ax.set_xlabel('n_scarified out of 10 [-]')
    ax.set_ylabel('weight_scarified [-]')

    for w, beta in zip(fig_data, (0, 0.1, 1, 10)):
        ax.plot(np.arange(11), w, label=r'$\beta$ = '+str(beta))
    ax.tick_params(direction='in')

    plt.legend()
    plt.show()

    # metrics figures
    fig, ax1 = plt.subplots()

    betas = [0.01, 0.05, 0.1, 0.5, 1, 5, 10]

    color = 'tab:blue'
    ax1.set_xlabel(r'$\beta$ [-]')
    ax1.set_ylabel('reconstruction_error [-]', color=color)
    ax1.plot(betas, table_data[:,1], color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:red'
    ax2.set_ylabel('divergence_error [-]', color=color)  # we already handled the x-label with ax1
    ax2.plot(betas, table_data[:,2], color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    ax1.set_xscale('log')
    ax1.set_xticks([0.01, 0.1, 1, 10])
    ax1.set_xticklabels([0, 0.1, 1, 10])

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()

    fig, ax = plt.subplots()

    ax.set_xlabel(r'$\beta$ [-]')
    ax.set_ylabel('sum_errors [-]')
    ax.plot(betas, 10*table_data[:,1] + table_data[:,2], color='k')

    ax.set_xscale('log')
    ax.set_xticks([0.01, 0.1, 1, 10])
    ax.set_xticklabels([0, 0.1, 1, 10])

    plt.show()