import cv2
import numpy as np
import subprocess

file_list = [
    "I_just_need_space.jpg",
    "keep_climbing.jpg",
    "mining_my_business.jpg",
    "smore_fun.jpg",
    "whale_of_a_time.jpg",
]

def getFileNames(dir):
    proc = subprocess.Popen('ls ' + dir + "/*", stdout=subprocess.PIPE)
    output = proc.stdout.read()
    names_list = output[:-1].split(b"\n")
    for i, name in enumerate(names_list):
        names_list[i] = str(name, "utf-8")
    return(names_list)  # empty output at the end

# This function was made from a script found from this Stack Overflow post:
# https://stackoverflow.com/questions/63001988/how-to-remove-background-of-images-in-python
def clearBackground(filename):
    # infile_dir = '../tshirts/'
    # filename = 'I_just_need_space_tshirt.jpg'

    # load image
    img = cv2.imread(filename)

    # convert to graky
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # threshold input image as mask
    mask = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY)[1]

    # negate mask
    mask = 255 - mask

    # apply morphology to remove isolated extraneous noise
    # use borderconstant of black since foreground touches the edges
    kernel = np.ones((3,3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # anti-alias the mask -- blur then stretch
    # blur alpha channel
    mask = cv2.GaussianBlur(mask, (0,0), sigmaX=2, sigmaY=2, borderType = cv2.BORDER_DEFAULT)

    # linear stretch so that 127.5 goes to 0, but 255 stays 255
    mask = (2*(mask.astype(np.float32))-255.0).clip(0,255).astype(np.uint8)

    # put mask into alpha channel
    result = img.copy()
    result = cv2.cvtColor(result, cv2.COLOR_BGR2BGRA)
    result[:, :, 3] = mask

    # save resulting masked image
    new_file_name = filename[:-4] + '_transp_bckgrnd.png'  # change suffix
    new_file_name = new_file_name[3:]
    write_location = './output/' + new_file_name
    print("Write location: " + write_location)
    if not cv2.imwrite(write_location, result):
        print("Error writing file") 

    # display result, though it won't show transparency
    # cv2.imshow("INPUT", img)
    # cv2.imshow("GRAY", gray)
    # cv2.imshow("MASK", mask)
    # cv2.imshow("RESULT", result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


tshirt_names = getFileNames("../tshirts")
hoodie_names = getFileNames("../hoodies")
hat_names = getFileNames("../hats")

for this_file in tshirt_names:
    clearBackground(this_file)

for this_file in hoodie_names:
    clearBackground(this_file)

for this_file in hat_names:
    clearBackground(this_file)

