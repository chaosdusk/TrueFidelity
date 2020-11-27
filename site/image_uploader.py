import pydicom
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import pickle as pl

import os
from shutil import copyfile

from app import app, db
from app.models import User, Label, Image, Batch

from flask import url_for


def main():
    fig_handle = pl.load(open('..\images\TF_LOW_30RED_8221;-10;lesion;9.5;0.pickle','rb'))
    plt.imshow(fig_handle, cmap='gray', vmin=0, vmax=255)
    plt.show()

# Image upload needs to be in a random order so that index doesn't give away which is which
def upload_all(folder, batch_id):
    b = Batch.query.get(batch_id)
    if b is None:
        raise Exception(f"Batch_id '{batch_id}'' does not exist! Create this batch first or select a different one")

    files = [os.path.join(folder, f) for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    for f in files:
        __upload_helper(f, batch_id)

def upload(image_file, batch_id):
    b = Batch.query.get(batch_id)
    if b is None:
        raise Exception(f"Batch_id '{batch_id}'' does not exist! Create this batch first or select a different one")
    __upload_helper(image_file, batch_id)

def __upload_helper(image_file, batch_id):
    folder_dest = os.path.join(app.root_path, 'static', 'images', str(batch_id))
    folder_dest_fake = os.path.join(folder_dest, 'fake')
    if not os.path.exists(folder_dest_fake):
        print("Making new folders:", folder_dest_fake)
        os.makedirs(folder_dest_fake)

    base = os.path.basename(image_file)

    # TODO: if imageOf noise, then don't add to database, but save to correct location
    dest_file = os.path.join(folder_dest, base)
    copyfile(image_file, dest_file)

    # TODO: See above, this is strictly for actual images to go into database
    attributes = os.path.splitext(base)[0].split(";")

    splitName = attributes[0].split("_")
    reconstruction = splitName[0] + "_" + splitName[1]
    dose = splitName[2]

    hu = attributes[1]
    imageOf = attributes[2]
    lesion_size_mm = attributes[3]

    # TODO: figure out size of grid to do lesion_size_mm / grid_size * 100
    size_measurement = 0

    i = Image(  batch_id=batch_id,
                reconstruction=reconstruction,
                dose=dose,
                hu=hu,
                lesion_size_mm=lesion_size_mm,
                size_measurement=size_measurement,
                filename=base
            )

    db.session.add(i)
    db.session.commit()

    print("Uploaded image:", i)


def create_batch(batch_name, batch_description):
    b = Batch(name=batch_name, description=batch_description)
    db.session.add(b)
    db.session.commit()
    print(f"Created batch: {b.id}, {b.name}")

if __name__ == "__main__":
    upload('..\images\TF_LOW_30RED_8221;-10;lesion;9.5;0.pickle', 1)