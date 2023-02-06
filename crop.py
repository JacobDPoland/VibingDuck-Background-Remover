import cv2
import numpy as np

file_list = [
    "I_just_need_space.jpg",
    "keep_climbing.jpg",
    "mining_my_business.jpg",
    "smore_fun.jpg",
    "whale_of_a_time.jpg",
]

# This function was made from a script found from this Stack Overflow post:
# https://stackoverflow.com/questions/63001988/how-to-remove-background-of-images-in-python
def clearBackground(infile_dir, filename):
    # infile_dir = '../tshirts/'
    # filename = 'I_just_need_space_tshirt.jpg'

    # load image
    img = cv2.imread(infile_dir + filename)

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
    new_file_name = filename[:-4] + '_transp_bckgrnd.png'
    write_location = './output/' + infile_dir[3:] + "/" + new_file_name
    print("Write location: " + write_location)
    cv2.imwrite(write_location, result)

    # display result, though it won't show transparency
    # cv2.imshow("INPUT", img)
    # cv2.imshow("GRAY", gray)
    # cv2.imshow("MASK", mask)
    # cv2.imshow("RESULT", result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


dir_list = [
    "../tshirts/",
    "../hoodies/"
]
for dir in dir_list:
    for file in file_list:
        clearBackground(dir, file)
