import cv2
import csv
import cvzone
from cvzone.HandTrackingModule import HandDetector
from time import sleep

class Quiz():
    def __init__(self, data):
        self.question = data[0]
        self.choice1 = data[1]
        self.choice2 = data[2]
        self.choice3 = data[3]
        self.choice4 = data[4]
        self.answer = int(data[5])
        self.userAnswer = None
    #method to check if user click an answer
    def update(self,cursor,bboxs):
        for index, bbox in enumerate(bboxs):
            x1, y1, x2, y2 = bbox
            if x1<cursor[0]<x2 and y1<cursor[1]<y2:
                self.userAnswer = index+1
                cv2.rectangle(img,(x1,y1),(x2,y2),(255,140,102),cv2.FILLED)
                
#open Camera
cap = cv2.VideoCapture(0)
cap.set((cv2.CAP_PROP_BUFFERSIZE), 1)
cap.set(3, 1320)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.8)

# read the csv file
csvPath = "Quiz.csv"
with open(csvPath,newline='\n')as f:
    reader = csv.reader(f)
    questions_data = list(reader)[1:]

# --------------------------------Create a class object---------------------------------------------------
testList = []
for question in questions_data:
    testList.append(Quiz(question))

question_no = 0
question_total = len(questions_data)

start = 0
# loops to capture frames from web cam
while True:
    sucess, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)
    
    if start == 0:
        img, bboxWelcome = cvzone.putTextRect(img, "Welcome to IQ Test!!!", (250,250), 2, 3,(0,0,0), (208,224,64),cv2.FONT_HERSHEY_TRIPLEX,offset=150, border=10,colorB=(89,89,89))
        img, bboxStart = cvzone.putTextRect(img, "Start", (1050,530), 1, 2,(0,0,0), (208,224,64),cv2.FONT_HERSHEY_SIMPLEX,offset=55, border=5,colorB=(89,89,89))
        if hands:
                lmList = hands[0]['lmList']
                cursor = lmList[8]
                length, info = detector.findDistance(lmList[8], lmList[12])
                
                if length < 60:
                    x1, y1, x2, y2 = bboxStart
                    if x1<cursor[0]<x2 and y1<cursor[1]<y2:
                        cv2.rectangle(img,(x1,y1),(x2,y2),(255,140,102),cv2.FILLED)
                        start += 1
    else:
        if question_no < question_total:    
            ques = testList[question_no]    
        #------------------------------Displaying the Questions and Answer choices---------------------------------
            # Draws rectangle and text
            img, bbox = cvzone.putTextRect(img,ques.question,(100,100), 1, 2,(0,0,0), (208,224,64),cv2.FONT_HERSHEY_SIMPLEX, offset=50,border=5,colorB=(89,89,89))
            img, bbox1 = cvzone.putTextRect(img,ques.choice1,(100,250), 1, 2,(0,0,0), (208,224,64),cv2.FONT_HERSHEY_SIMPLEX, offset=50,border=5,colorB=(89,89,89))
            img, bbox2 = cvzone.putTextRect(img,ques.choice2,(400,250), 1, 2,(0,0,0), (208,224,64),cv2.FONT_HERSHEY_SIMPLEX, offset=50,border=5,colorB=(89,89,89))
            img, bbox3 = cvzone.putTextRect(img,ques.choice3,(100,400), 1, 2,(0,0,0), (208,224,64),cv2.FONT_HERSHEY_SIMPLEX, offset=50,border=5,colorB=(89,89,89))
            img, bbox4 = cvzone.putTextRect(img,ques.choice4,(400,400), 1, 2,(0,0,0), (208,224,64),cv2.FONT_HERSHEY_SIMPLEX, offset=50,border=5,colorB=(89,89,89))

        #----------------------------Checked if user click the answer--------------------------------------------
            if hands:
                lmList = hands[0]['lmList']
                cursor = lmList[8]
                length, info = detector.findDistance(lmList[8], lmList[12])
            
                if length < 50:
                    ques.update(cursor,[bbox1, bbox2, bbox3, bbox4])
                    if ques.userAnswer is not None:
                        sleep(1)
                        question_no += 1
        else:
            score = 0
            for test in testList:
                if test.answer == test.userAnswer:
                    score +=1
            score = round((score/question_total)*100, 2)
            # Draws rectangles with text
            img, _ = cvzone.putTextRect(img, 'Quiz Completed', [300, 400], 1, 2,(0,0,0), (208,224,64),cv2.FONT_HERSHEY_SIMPLEX, offset=40, border=5,colorB=(89,89,89))
            img, _ = cvzone.putTextRect(img, f'Youre Score:{score}%', [710, 400], 1, 2,(0,0,0), (208,224,64),cv2.FONT_HERSHEY_SIMPLEX, offset=40, border=5,colorB=(89,89,89))
            img, bboxQuit = cvzone.putTextRect(img, 'End', [1150, 530], 1, 2,(0,0,0), (208,224,64),cv2.FONT_HERSHEY_SIMPLEX, offset=40, border=5,colorB=(89,89,89))
            if hands:
                lmList = hands[0]['lmList']
                cursor = lmList[8]
                length, info = detector.findDistance(lmList[8], lmList[12])
                # condition to end program
                if length < 50:
                    x1, y1, x2, y2 = bboxQuit
                    if x1<cursor[0]<x2 and y1<cursor[1]<y2:
                        cv2.rectangle(img,(x1,y1),(x2,y2),(255,140,102),cv2.FILLED)
                        break
            # conditons to print what iq status the user has
            if score == 100:
                img, bboxIQlvl_high = cvzone.putTextRect(img, 'Wow! You are a Genius', [450, 150], 1, 2,(255,255,255), (255,0,128),cv2.FONT_HERSHEY_TRIPLEX, offset=100, border=5,colorB=(89,89,89)) 
            if score < 100 and score >= 80:
                img, bboxIQlvl_high = cvzone.putTextRect(img, 'You\'re IQ Level is High', [400, 150], 1, 2,(0,0,0), (0,215,255),cv2.FONT_HERSHEY_TRIPLEX, offset=100, border=5,colorB=(89,89,89))
            if score < 80 and score >= 50:
                img, bboxIQlvl_high = cvzone.putTextRect(img, 'You\'re IQ Level is Low', [450, 150], 1, 2,(0,0,0), (192,192,192),cv2.FONT_HERSHEY_TRIPLEX, offset=100, border=5,colorB=(89,89,89))
            if score < 49 and score >=0:
                img, bboxIQlvl_high = cvzone.putTextRect(img, 'You\'re IQ Level is Unidentified', [400, 150], 1, 2,(255,255,255),(57,115,172),cv2.FONT_HERSHEY_TRIPLEX, offset=100, border=5,colorB=(89,89,89))
    # create progress bar
    barValue = 100 + (1000//question_total)*question_no
    cv2.rectangle(img, (100,600),(barValue, 650),(208, 224, 64), cv2.FILLED)
    cv2.rectangle(img, (100,600),(1100, 650),(0, 255, 0), 5)
    img, _ = cvzone.putTextRect(img, f'{round((question_no/question_total)*100)}%', [1130, 635], 1, 2,(0,0,0), (208,224,64),cv2.FONT_HERSHEY_SIMPLEX, offset=16,border=1)
    # Show frames captured
    cv2.imshow("IQ test",img)
    cv2.waitKey(1)
# close camera
cap.release()
cv2.destroyAllWindows()    