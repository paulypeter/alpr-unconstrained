import cv2
import numpy as np

def scan_image(imgobj):
    img_size = imgobj.shape[1::-1] # return (width, height)
    averages = []
    for x in range(img_size[0]):    # iterate over width
        averages.append(np.average(imgobj[:,x]))
        np.mean(imgobj[:,x], axis=(0, 1)) #?
        # https://stackoverflow.com/a/14350013 ?
    return averages

        # for y in range(int(img_size[1]/5)):    # iterate over height, use every 5th pixel
        #     point = imgobj[y * 5, x]
        #     #print(x, y * 5, point)

def detect_edge_by_avg(avg_array):
    delta_arr = []
    delta_dict = {}
    for i in range(1, len(avg_array)):
        delta = int(avg_array[i] - avg_array[i - 1])
        delta_arr.append(delta)
        if abs(delta) > 30:
            delta_dict[str(i)] = delta
    print(delta_dict)

def detect_edge_by_percent(percent_dict):
    return 0
        

if __name__ == "__main__":
    imgpath = "samples/test/0002_lp.png"
    img = cv2.imread(imgpath)
    avs = scan_image(img)
    detect_edge(avs)
