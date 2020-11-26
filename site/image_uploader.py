import pydicom
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import pickle as pl

import os

from app import app, db
from app.models import User, Label, Image, Batch


def main():
    fig_handle = pl.load(open('..\images\TF_LOW_30RED_8221;-10;lesion;9.5;0.pickle','rb'))
    plt.imshow(fig_handle, cmap='gray', vmin=0, vmax=255)
    plt.show()

# Image upload needs to be in a random order so that index doesn't give away which is which
def upload_all(folder, batch_id):
    pass

def upload(image_file, batch_id):
    pass

def create_batch(batch_name, batch_description):
    b = Batch(name=batch_name, description=batch_description)
    db.session.add(b)
    db.session.commit()
    print(f"Created batch: {b.id}, {b.name}")

main()