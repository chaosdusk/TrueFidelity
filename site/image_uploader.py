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
    b = Batch.query.get(batch_id)
    if b is None:
        raise Exception(f"Batch_id '{batch_id}'' does not exist! Create this batch first or select a different one")
    print(f"Uploading image to batch {batch_id}: {b.name}")
    __upload_helper(image_file, batch_id)

def __upload_helper(image_file, batch_id):
    base = os.path.basename(image_file)
    attributes = os.path.splitext(base)[0].split(";")
    print("Attributes:", attributes)
TF_LOW_30RED_8221;-10;lesion;9.5;0.pickle
    i = Image(  batch_id=batch_id,
                reconstruction=attributes[0],
                attenuation=attributes[1],
                )

def create_batch(batch_name, batch_description):
    b = Batch(name=batch_name, description=batch_description)
    db.session.add(b)
    db.session.commit()
    print(f"Created batch: {b.id}, {b.name}")

if __name__ == "__main__":
    main()