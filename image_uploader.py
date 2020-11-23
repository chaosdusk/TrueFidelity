import pydicom
import numpy as np
import matplotlib.pyplot as plt

import pickle as pl


def main():
    fig_handle = pl.load(open('images\TF_LOW_30RED_8221;-10;lesion;9.5;0.pickle','rb'))
    plt.imshow(fig_handle, cmap='gray', vmin=0, vmax=255)
    plt.show()
    print("hey there")

main()