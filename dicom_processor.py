import pydicom
import numpy as np
import matplotlib.pyplot as plt
import os
import random

# setup
radius = 15
lesion_locations = [(250, 390), (230, 355), (205, 305), (190, 270), (175, 245), 
                    (300, 365), (280, 330), (255, 280), (240, 245), (225, 220),
                    (350, 340), (330, 305), (305, 255), (290, 220), (275, 195)]
noise_center = (145, 260)

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

# get a 30x30 sample of noise, same dimension as lesion cut
cut_noise = scaled[noise_center[0]-15:noise_center[0]+15, noise_center[1]-15:noise_center[1]+15]
noise = np.full((120, 120), 1024)
# 4x4 grid of noise
for i in range(0, 91, 30):
    for j in range(0, 91, 30):
        noise[i:i+30, j:j+30] = cut_noise
# select random grid to replace with the lesion cut
lesion_x = random.randint(0, 3)
lesion_y = random.randint(0, 3)
lesion_selected = lesion_locations[lesion_index]
lesion = scaled[lesion_selected[0]-15:lesion_selected[0]+15, lesion_selected[1]-15:lesion_selected[1]+15]
noise[lesion_y*30:lesion_y*30+30, lesion_x*30:lesion_x*30+30] = lesion

plt.imshow(noise, cmap='gray', vmin=0, vmax=255)
plt.show()