import pydicom
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import pickle as pl
import random

import os
from shutil import copyfile

from app import app, db
from app.models import User, Label, Image, Batch

from flask import url_for


def main():
    fig_handle = pl.load(open('..\images\TF_LOW_30RED_8221;-10;lesion;9.5;0.pickle','rb'))
    plt.imshow(fig_handle, cmap='gray', vmin=0, vmax=255)
    plt.show()

def upload_all(folder, batch_id, NUM_GRIDS):
    b = Batch.query.get(batch_id)
    if b is None:
        raise Exception(f"Batch_id '{batch_id}'' does not exist! Create this batch first or select a different one")

    files = [os.path.join(folder, f) for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    # Shuffle the files so the order of the images in the questions is random
    random.shuffle(files)
    for f in files:
        __upload_helper(f, batch_id, NUM_GRIDS)


def upload_all_fake(folder, batch_id):
    b = Batch.query.get(batch_id)
    if b is None:
        raise Exception(f"Batch_id '{batch_id}' does not exist! Create this batch or select a different one")

    files = [os.path.join(folder, f) for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    for f in files:
        __upload_fake_helper(f, batch_id)

def upload_fake(image_file, batch_id):
    b = Batch.query.get(batch_id)
    if b is None:
        raise Exception(f"Batch_id '{batch_id}'' does not exist! Create this batch first or select a different one")
    __upload_fake_helper(image_file, batch_id)

def __upload_fake_helper(image_file, batch_id):
    folder_dest_fake = os.path.join(app.root_path, 'static', 'images', str(batch_id), 'fake')
    if not os.path.exists(folder_dest_fake):
        print("Making new folders:", folder_dest_fake)
        os.makedirs(folder_dest_fake)

    base = os.path.basename(image_file)
    attributes = os.path.splitext(base)[0].split(";")

    splitName = attributes[0].split("_")
    reconstruction = splitName[0] + "_" + splitName[1]
    dose = splitName[2]

    save_name = f'{reconstruction}_{dose}.pickle'
    dest_file = os.path.join(folder_dest_fake, save_name)
    copyfile(image_file, dest_file)

    print("Uploaded fake: ", save_name)

def upload(image_file, batch_id, NUM_GRIDS):
    b = Batch.query.get(batch_id)
    if b is None:
        raise Exception(f"Batch_id '{batch_id}'' does not exist! Create this batch first or select a different one")
    __upload_helper(image_file, batch_id, NUM_GRIDS)

def __upload_helper(image_file, batch_id, NUM_GRIDS):
    folder_dest = os.path.join(app.root_path, 'static', 'images', str(batch_id))
    folder_dest_fake = os.path.join(folder_dest, 'fake')
    if not os.path.exists(folder_dest_fake):
        print("Making new folders:", folder_dest_fake)
        os.makedirs(folder_dest_fake)

    base = os.path.basename(image_file)
    dest_file = os.path.join(folder_dest, base)
    copyfile(image_file, dest_file)

    attributes = os.path.splitext(base)[0].split(";")

    splitName = attributes[0].split("_")
    reconstruction = splitName[0] + "_" + splitName[1]
    dose = splitName[2]

    hu = attributes[1]
    imageOf = attributes[2]
    lesion_size_mm = attributes[3]

    GRID_SIZE = 15 * NUM_GRIDS
    # This 500 is the script size
    size_measurement = int(float(lesion_size_mm) * 500 / GRID_SIZE)

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
    print('Call upload_all with folder of images to upload.')
