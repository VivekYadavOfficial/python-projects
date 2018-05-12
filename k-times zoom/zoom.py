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

new_x = x*scale
new_y = y*scale

ul_x = new_x - x
ul_y = new_y - y

lr_x = new_x + (len(image) - x)
lr_y = new_y + (len(image[0]) - y)

#allocating image list for storing 
new_image=[[[0,0,0] for m in range(len(image[0])*scale)] for m in range(len(image))]

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
			new_image[i][j*scale + k+1] = [min(new_image[i][j*scale + k][0],new_image[i][(j+1)*scale][0]) + b_new,min(new_image[i][j*scale + k][1],new_image[i][(j+1)*scale][1]) + g_new,min(new_image[i][j*scale + k][2],new_image[i][(j+1)*scale][2]) + r_new]

new_image2=[[[0,0,0] for n in range(len(image[0])*scale)] for n in range(len(image)*scale)]

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
			new_image2[i*scale + k+1][j] = [min(new_image2[i*scale +k][j][0],new_image2[(i+1)*scale][j][0]) + r_new,min(new_image2[i*scale + k][j][1],new_image2[(i+1)*scale][j][1]) + g_new,min(new_image2[i*scale + k][j][2],new_image2[(i+1)*scale][j][2]) + b_new]

zoomed_image = [[[0,0,0] for n in range(len(image[0]))] for n in range(len(image))]
zoomed_image = [new_image2[i][ul_y:lr_y] for i in range(ul_x,lr_x)]

cv2.imwrite("zoomed_image.png", np.array(zoomed_image, dtype="uint8"))
