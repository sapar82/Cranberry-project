import matplotlib.pyplot as plt

from load_data import df_background, df_non_scarifie, df_scarifie


df_background.plot(x="wavelength")
df_non_scarifie.plot(x="wavelength")
df_scarifie.plot(x="wavelength")

plt.show()