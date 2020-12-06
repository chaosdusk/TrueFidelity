import pydicom
import numpy as np
import matplotlib.pyplot as plt
import os
import random
import pickle

def location_mod(image, index):
    offset_y = 0
    offset_x = 0
    lesion = lesion_locations[index]
    off_30 = [1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 16, 17, 19, 20, 21, 22, 23, 24, 25]
    if image in off_30:
        offset_y = 30
    elif image == 14:
        offset_y = -35
    elif image == 18:
        offset_y = -15
    return (lesion[0]+offset_y, lesion[1]+offset_x)

def noise_mod(image, index):
    offset_y = 0
    offset_x = 0
    noise = noise_centers[index]
    if image == 14:
        offset_y = -60
    elif image == 18:
        offset_y = -50
    return (noise[0]+offset_y, noise[1]+offset_x)

def generate(image_index, image_full_path, lesion_index, is_noise=False):
    img = pydicom.read_file(image_full_path)

    # process image
    pixels = img.pixel_array.astype(float)
    scaled = np.uint8((np.maximum(pixels, 0) / pixels.max()) * 255.0)
    noise = np.full((radius*2*grid_dim, radius*2*grid_dim), 1024)

    # 4x4 grid of noise
    for i in range(0, radius*2*(grid_dim-1)+1, radius*2):
        for j in range(0, radius*2*(grid_dim-1)+1, radius*2):
            center = noise_mod(image_index, random.randint(0, len(noise_centers) - 1))
            rotate = random.randint(0, grid_dim-1)
            x_offset = random.randint(-offset, offset)
            y_offset = random.randint(-offset, offset)
            cut_noise = scaled[center[0]-radius+y_offset:center[0]+radius+y_offset, center[1]-radius+x_offset:center[1]+radius+x_offset]
            np.rot90(cut_noise, rotate)
            if random.randint(0, 1) == 1:
                np.flip(cut_noise)
            noise[i:i+radius*2, j:j+radius*2] = cut_noise
    if not is_noise:
        # select random grid to replace with the lesion cut
        lesion_x = random.randint(0, grid_dim - 1)
        lesion_y = random.randint(0, grid_dim - 1)
        lesion_selected = location_mod(image_index, 0)
        lesion = scaled[lesion_selected[0]-radius:lesion_selected[0]+radius, lesion_selected[1]-radius:lesion_selected[1]+radius]
        noise[lesion_y*radius*2:lesion_y*radius*2+radius*2, lesion_x*radius*2:lesion_x*radius*2+radius*2] = lesion
        #plt.imshow(noise, cmap='gray', vmin=0, vmax=255)
        #plt.show()

    hu = -15
    if lesion_index > 4:
        if lesion_index > 9:
            hu = -10
        else:
            hu = -5
    size = lesion_sizes[lesion_index % 5]

    image_number = 0
    save_file = './images_5x5/{};{};{};{};{}.pickle'.format(directories[image_index][8:], hu, 'lesion', size, image_number) if not is_noise else './noise_5x5/{};{}.pickle'.format(directories[image_index][8:], 'noise')

    if not os.path.exists('noise_5x5'):
        os.makedirs('noise_5x5')
    with open(save_file, 'wb') as handle:
        pickle.dump(noise, handle)


# setup
radius = 15
grid_dim = 5
lesion_locations = [(250, 390), (230, 355), (205, 305), (190, 270), (175, 245), 
                    (300, 365), (280, 330), (255, 280), (240, 245), (225, 220),
                    (350, 340), (330, 305), (305, 255), (290, 220), (275, 195)]
lesion_sizes = [10, 9.5, 6.3, 4.8, 4]
noise_centers = [(145, 260)]#, (145, 270)]
offset = 20
# get random image to pull lesion and noise from
directories = [x[0] for x in os.walk('./DICOM/')]
for image_index in range(1, len(directories)):
    for lesion_index in range(0, 1):
        image_path = directories[image_index]
        (_, _, image_file) = next(os.walk(image_path))
        image_full_path = '{}/{}'.format(image_path, image_file[0])
        generate(image_index, image_full_path, lesion_index, True)
