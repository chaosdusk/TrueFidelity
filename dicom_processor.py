import pydicom
import numpy as np
import matplotlib.pyplot as plt
import os
import random
import pickle

# setup
radius = 15
lesion_locations = [(250, 390), (230, 355), (205, 305), (190, 270), (175, 245), 
                    (300, 365), (280, 330), (255, 280), (240, 245), (225, 220),
                    (350, 340), (330, 305), (305, 255), (290, 220), (275, 195)]
lesion_sizes = [10, 9.5, 6.3, 4.8, 4]
noise_centers = [(145, 260), (145, 270)]

# get random image to pull lesion and noise from
directories = [x[0] for x in os.walk('./DICOM/')]
image_index = random.randint(1, len(directories) - 1)
lesion_index = random.randint(0, 14)

# path and load image
image_path = directories[image_index]
(_, _, image_file) = next(os.walk(image_path))
image_full_path = '{}/{}'.format(image_path, image_file[0])
img = pydicom.read_file(image_full_path)

# process image
pixels = img.pixel_array.astype(float)
scaled = np.uint8((np.maximum(pixels, 0) / pixels.max()) * 255.0)
noise = np.full((160, 160), 1024)

# 4x4 grid of noise
for i in range(0, 121, 40):
    for j in range(0, 121, 40):
        center = noise_centers[random.randint(0, len(noise_centers) - 1)]
        rotate = random.randint(0, 3)
        x_offset = random.randint(-20, 20)
        y_offset = random.randint(-20, 20)
        cut_noise = scaled[center[0]-20+y_offset:center[0]+20+y_offset, center[1]-20+x_offset:center[1]+20+x_offset]
        np.rot90(cut_noise, rotate)
        if random.randint(0, 1) == 1:
            np.flip(cut_noise)
        noise[i:i+40, j:j+40] = cut_noise

# select random grid to replace with the lesion cut
lesion_x = random.randint(0, 3)
lesion_y = random.randint(0, 3)
lesion_selected = lesion_locations[lesion_index]
lesion = scaled[lesion_selected[0]-20:lesion_selected[0]+20, lesion_selected[1]-20:lesion_selected[1]+20]
noise[lesion_y*40:lesion_y*40+40, lesion_x*40:lesion_x*40+40] = lesion

plt.imshow(noise, cmap='gray', vmin=0, vmax=255)
plt.show()

hu = -15
if lesion_index > 4:
    if lesion_index > 9:
        hu = -10
    else:
        hu = -5
size = lesion_sizes[lesion_index % 5]

image_number = 0

'''with open('./images/{}_{}_{}_{}_{}.pickle'.format(directories[image_index][8:], hu, size, 'lesion', image_number), 'wb') as handle:
    pickle.dump(noise, handle)'''