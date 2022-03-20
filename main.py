from _nmf import NMF
import numpy as np

from load_data import array_mixed
from plot_data import plot_array

def normalize_spectrum(array):
    return array / array.sum()

def normalize_array(A):
    """
    Discrete normalization of array A.
    Normalize array A so that every row sum to one (= 1).
    W: sum of weights == 1 for each measurement.
    H: sum of intensities == 1 for each endmember.
    Parameters
    ----------
    A: array-like to be normalized (W or H)
    Updates
    -------
    A: array-like normalized
    """
    m, n = A.shape
    for i in range(m):
        denom = sum(A[i])
        for j in range(n):
            A[i, j] /= denom
    return A

# spectrum_non_scarifie = normalize_spectrum(np.mean(array_non_scarifie[1:], axis=0))
# spectrum_scarifie = normalize_spectrum(np.mean(array_scarifie[1:], axis=0))
# spectrum_background = normalize_spectrum(np.mean(array_background[1:], axis=0))

# np.save("data/numpy_arrays/spectrum_non_scarifie.npy", spectrum_non_scarifie)
# np.save("data/numpy_arrays/spectrum_scarifie.npy", spectrum_scarifie)
# np.save("data/numpy_arrays/spectrum_background.npy", spectrum_background)

X = normalize_array(array_mixed)
X[X<0] = 0

spectrum_non_scarifie = np.load("data/numpy_arrays/spectrum_non_scarifie.npy")
spectrum_scarifie = np.load("data/numpy_arrays/spectrum_scarifie.npy")
spectrum_background = np.load("data/numpy_arrays/spectrum_background.npy")

# nmf custom init
Hp = np.vstack((spectrum_non_scarifie, spectrum_scarifie, spectrum_background))
Hp[Hp<0] = 0


# fig, ax = plt.subplots()

# ax.plot(np.arange(651), spectrum_non_scarifie)
# ax.plot(np.arange(651), spectrum_scarifie)
# ax.plot(np.arange(651), spectrum_background)

# plt.show()

fig_data = np.empty((4, 11))
table_data = np.empty((7, 4))

for i, beta in enumerate((0, 0.05, 0.1, 0.5, 1, 5, 10)):

    model = NMF(n_components=3, init='nndsvda', random_state=0, tol=1e-10, max_iter=1000000, beta=beta)
    W = model.fit_transform(X, Hp=Hp)
    H = model.components_

    if i % 2 == 0:
        plot_array(normalize_array(H))
        index = int(input("Index (0 or 1):"))
        fig_data[i//2] = [W[2, index], W[1, index], W[7, index], W[8, index], W[9, index], W[6, index],
                    W[0, index], W[3, index], W[5, index], W[4, index], W[10, index]] # reorder data from listdir
    table_data[i] = [beta, model.reconstruction_err_, model.divergence_err_, model.n_iter_]

np.save("data/figures/fig_data", fig_data)
np.save("data/figures/table_data", table_data)

# ['6_scarifie.txt', '1_scarifie.txt', '0_scarifie.txt', '7_scarifie.txt', '9_scarifie.txt', '8_scarifie.txt', '5_scarifie.txt', '2_scarifie.txt', '3_scarifie.txt', '4_scarifie.txt', '10_scarifie.txt']