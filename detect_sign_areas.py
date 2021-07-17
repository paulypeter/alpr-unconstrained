import cv2
import numpy as np

SIMILAR_DIST = 50
MAIN_COLOUR_RATIO = 0.7


def scan_image(imgobj):
    img_size = imgobj.shape[1::-1] # return (width, height)
    averages = []
    percent = []
    for x in range(img_size[0]):    # iterate over width
        averages.append(np.average(imgobj[:,x]))
        np.mean(imgobj[:,x], axis=(0, 1)) #?
        colour_amount = {}
        for y in range(int(img_size[1])):
            current_value = imgobj[y, x]
            b, g, r = current_value
            similar = colour_in_list(colour_amount, current_value)
            if similar:
                colour_amount[similar] += 1/img_size[1]
            else:
                colour_amount[str([b, g, r])] = 1/img_size[1]
        # print("different colours counted:", len(colour_amount))
        # https://stackoverflow.com/a/14350013 ?
        percent.append(colour_amount)
    return averages, percent


        # for y in range(int(img_size[1]/5)):    # iterate over height, use every 5th pixel
        #     point = imgobj[y * 5, x]
        #     #print(x, y * 5, point)

def get_main_colour(column_colour_perc):
    for colour in column_colour_perc.keys():
        if column_colour_perc[colour] > MAIN_COLOUR_RATIO:
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

def colour_distance(colour_1, colour_2):
    dist = colour_2 - colour_1
    return cv2.norm(dist)

def get_colour_percent_for_column(column_colour_perc, colour):
    # https://stackoverflow.com/a/62675780 -> colour distance
    if str(colour) in column_colour_perc.keys():
        return column_colour_perc[colour.tobytes()]
    return 0

def get_boundaries(imgobj):
    width, height = imgobj.shape[1::-1]
    borders = []
    current_colour = np.array([128, 128, 128])
    last_colour = np.array([128, 128, 128])
    for i in range(width):
        current = get_main_colour(percents[i])
        last = get_main_colour(percents[i - 1])
        if current is not None:
            current = eval(current)
            current_colour = np.array(current)
        if last is not None:
            last = eval(last)
            last_colour = np.array(last)
        if colour_distance(current_colour, last_colour) > SIMILAR_DIST and not (current is None and last is None):# and i > borders[-1] + width/6:
            borders.append(i)
    borders = borders + [width]
    return borders

def colour_in_list(column_colour_perc, colour):
    if column_colour_perc:
        for item in column_colour_perc:
            item_colour = np.array(eval(item))
            if colour_distance(colour, item_colour) < SIMILAR_DIST:
                return item
    return False

# TODO:
# convert crops to greyscale
# test OCR on greyscale img
# test on inverted img -> no improvement?
if __name__ == "__main__":
    imgpath = "samples/test/0002_lp.png"
    # imgpath = "samples/test/011.jpg"
    img = cv2.imread(imgpath)
    width, height = img.shape[1::-1]
    avs, percents = scan_image(img)
    #detect_edge(avs)
    black = np.array([0, 0, 0])
    borders = get_boundaries(img)
    for i in range(len(borders) - 1):
        # print(borders[i], borders[i + 1])
        crop = img[0:height, borders[i]:borders[i + 1]]
        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
        gray_inv = cv2.bitwise_not(gray)
        cv2.imwrite(f"crop_{i}.png", crop)
        cv2.imwrite(f"crop_{i}_gray.png", gray)
        cv2.imwrite(f"crop_{i}_gray_inv.png", gray_inv)
    print(len(borders))
