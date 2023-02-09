from testingHelper import *

folder_path = '/Users/mightymanh/Desktop/experiment/'
accuracy = getAccuracyOfTextDetection(folder_path, 500, 20)

# img_path = folder_path + 'img_000_tar_014_L.jpg'
# img = cv2.imread(img_path)
# imgScaled = scaleImg(img, 500)

# results = readImgPathDetectLetter(img_path, 500, 20)

# imgStack = stackHorizontal('img_000_tar_014_L.jpg', imgScaled, results)
# imgStackPil = Image.fromarray(imgStack)
# imgStackPil.save('experiment.pdf')