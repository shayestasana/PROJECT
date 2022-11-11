import cv2
import csv
cap = cv2.VideoCapture(2)
cap.set(3, 1280) # set Width
cap.set(4, 720) # set Height

class MCQ():
    def __init__(self, data):
        self.question = data[0]
        self.choice1 = data[1]
        self.choice2 = data[2]
        self.choice3 = data[3]
        self.choice4 = data[4]
        self.answer = int(data[5])

        self.userAns=None


pathCSV= "mcqs.csv"
with  open(pathCSV, newline='\n') as f:
    reader = csv.reader(f)
    dataAll = list(reader)[1:]

#create object for each question
mcqList = []   
for q in dataAll:
    mcqList.append(MCQ(q))

print(len)


qNo=0
qTotal=len(dataAll)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    cv2.imshow("Img", img)
    cv2.waitkey(1)
