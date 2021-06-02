import cv2
import numpy as np

def scan_image(imgobj):
    img_size = imgobj.shape[1::-1] # return (width, height)
    averages = []
    percent = []
    for x in range(img_size[0]):    # iterate over width
        averages.append(np.average(imgobj[:,x]))
        np.mean(imgobj[:,x], axis=(0, 1)) #?
        colour_amount = {}
        for y in range(int(img_size[1])):
            current_value = str(imgobj[y, x])
            if current_value in list(colour_amount.keys()):
                colour_amount[current_value] += 1/img_size[1]
            else:
                colour_amount[current_value] = 1/img_size[1]
        # https://stackoverflow.com/a/14350013 ?
        percent.append(colour_amount)
    return averages, percent


        # for y in range(int(img_size[1]/5)):    # iterate over height, use every 5th pixel
        #     point = imgobj[y * 5, x]
        #     #print(x, y * 5, point)

def get_main_colour(column_colour_perc):
    for colour in column_colour_perc.keys():
        if column_colour_perc[colour] > 0.4:
            return colour
    return None

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

def get_colour_percent_for_column(column_colour_perc, colour):
    # https://stackoverflow.com/a/62675780 -> colour distance
    if str(colour) in column_colour_perc.keys():
        return column_colour_perc[str(colour)]
    return 0

if __name__ == "__main__":
    imgpath = "samples/test/0002_lp.png"
    img = cv2.imread(imgpath)
    avs, percents = scan_image(img)
    #detect_edge(avs)
    black = np.array([0, 0, 0])
    for i in range(240):
        print(get_colour_percent_for_column(percents[i], black))
