#vivekyadavofficial
#import necessary libraries
import cv2
import argparse
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help="Path to input image", required=True)
ap.add_argument("-p", "--pivot-point", help="Pivot point coordinates x, y separated by comma (,)", required=True)
ap.add_argument("-s", "--scale", help="Scale to zoom", type=int, required=True)
args = vars(ap.parse_args())

image_path = args["image"]
x, y = map(int, args["pivot_point"].split(","))
scale = args["scale"]
image = cv2.imread(image_path)
image = image.tolist()

#calculate window for the final image
ul_x = int(x - (float(1)/float(scale) * float(1)/float(2) * len(image[0])))
ul_y = int(y - (float(1)/float(scale) * float(1)/float(2) * len(image)))

lr_x = int(ul_x + (float(1)/float(scale) * len(image[0])))
lr_y = int(ul_y + (float(1)/float(scale) * len(image)))

#checking and adjusting whether the window is negative
if (ul_x < 0):
		lr_x = lr_x - ul_x
		ul_x = 0
if (ul_y < 0):
		lr_y = lr_y - ul_y
		ul_y = 0

if (lr_x > len(image[0])):
		ul_x = ul_x - (lr_x - len(image[0]))
		lr_x = len(image[0])
if (lr_y > len(image)):
		ul_y = ul_y - (lr_y - len(image))
lr_y = len(image)

#allocating image list for storing 
new_image=[[[0,0,0] for m in range(1400*scale)] for m in range(1050)]

#column wise zooming
for i in range(len(image)):
	for j in range(len(image[0])):
		b_new = int(abs(image[i][j][0] - image[i][++j][0])/scale)
		g_new = int(abs(image[i][j][1] - image[i][++j][1])/scale)
		r_new = int(abs(image[i][j][2] - image[i][++j][2])/scale)
		#new_image.append([])
		#new_image.insert([i][j],image[i][j])
		j = j-3
		new_image[i][j*scale] = image[i][j]
		for k in range(scale-1):
			new_image[i][j*scale + k+1] = [new_image[i][j*scale + k][0] + b_new,new_image[i][j*scale + k][1] + g_new,new_image[i][j*scale + k][2] + r_new]

new_image2=[[[0,0,0] for n in range(1400*scale)] for n in range(1050*scale)]

#row wise zooming
for j in range(len(new_image[0])):
	for i in range(len(new_image)):
		r_new = int(abs(new_image[i][j][0] - new_image[++i][j][0])/scale)
		g_new = int(abs(new_image[i][j][1] - new_image[++i][j][1])/scale)
		b_new = int(abs(new_image[i][j][2] - new_image[++i][j][2])/scale)
		#new_image.append([])
		#new_image.insert([i][j],image[i][j])
		i = i-3
		new_image2[i*scale][j] = new_image[i][j]
		for k in range(scale-1):
			new_image2[i*scale + k+1][j] = [new_image2[i*scale +k][j][0] + r_new,new_image2[i*scale + k][j][1] + g_new,new_image2[i*scale + k][j][2] + b_new]

zoomed_image = new_image2[ul_x:lr_x+1][ul_y:lr_y+1]

cv2.imwrite("zoomed_image5.png", np.array(zoomed_image, dtype="uint8"))
