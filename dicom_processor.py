import pydicom
import numpy as np
import matplotlib.pyplot as plt

img = pydicom.read_file('./DICOM/ASIRV_0_30RED_8257/IM-0018-0001.dcm')
image = img.pixel_array
image2d = image.astype(float)

image2d_scaled = (np.maximum(image2d, 0) / image2d.max()) * 255.0
image2d_scaled = np.uint8(image2d_scaled)

print(image.dtype)
print(image.shape)
print(image)

print(image2d_scaled.dtype)
print(image2d_scaled.shape)
print(image2d_scaled)

drop_y = 50
drop_x = -25

white = np.full(image2d_scaled.shape, 1024)
dark_5 = image2d_scaled[235:265, 375:405]
dark_4 = image2d_scaled[215:245, 340:370]
dark_3 = image2d_scaled[190:220, 290:320]
dark_2 = image2d_scaled[175:205, 255:285]
dark_1 = image2d_scaled[160:190, 230:260]
white[235:265, 375:405] = dark_5
white[215:245, 340:370] = dark_4
white[190:220, 290:320] = dark_3
white[175:205, 255:285] = dark_2
white[160:190, 230:260] = dark_1

med_1 = image2d_scaled[285:315, 350:380]
med_2 = image2d_scaled[265:295, 315:345]
med_3 = image2d_scaled[240:270, 265:295]
med_4 = image2d_scaled[225:255, 230:260]
med_5 = image2d_scaled[210:240, 205:235]
white[285:315, 350:380] = med_1
white[265:295, 315:345] = med_2
white[240:270, 265:295] = med_3
white[225:255, 230:260] = med_4
white[210:240, 205:235] = med_5

light_1 = image2d_scaled[335:365, 325:355]
light_2 = image2d_scaled[315:345, 290:320]
light_3 = image2d_scaled[290:320, 240:270]
light_4 = image2d_scaled[275:305, 205:235]
light_5 = image2d_scaled[260:290, 180:210]
white[335:365, 325:355] = light_1
white[315:345, 290:320] = light_2
white[290:320, 240:270] = light_3
white[275:305, 205:235] = light_4
white[260:290, 180:210] = light_5


plt.imshow(white, cmap='gray', vmin=0, vmax=255)
#plt.imshow(image2d, cmap='gray', vmin=0, vmax=255)
#plt.imshow(image2d_scaled, cmap='gray', vmin=0, vmax=255)
plt.show()