import os
import pandas as pd


# DIR = "data/background"

# filenames = os.listdir(DIR)
# df = pd.read_csv(f"{DIR}/{filenames[0]}", sep="\t", names=["wavelength", "pixel_0"], skiprows=13, decimal=",")

# for i, filename in enumerate(filenames[1:]):

#     pixel = pd.read_csv(f"{DIR}/{filename}", sep="\t", names=["wavelength", "intensity"], skiprows=13, decimal=",")
#     df[f"pixel_{i+1}"] = pixel["intensity"]

# df.to_pickle("background.pkl")


df_non_scarifie = pd.read_pickle("data/pickle_dataframes/non_scarifie.pkl")
df_scarifie = pd.read_pickle("data/pickle_dataframes/scarifie.pkl")
df_background = pd.read_pickle("data/pickle_dataframes/background.pkl")