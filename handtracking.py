from cvzone.HandTrackingModule import HandDetector
import cv2
from time import sleep
from pynput.keyboard import Controller

# Set up the video capture
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Width
cap.set(4, 720)   # Height

# Initialize the hand detector with higher detection confidence
detector = HandDetector(detectionCon=1)

# Define keys layout for the virtual keyboard
keys = [["Q","W","E","R","T","Y","U","I","O","P"],
        ["A","S","D","F","G","H","J","K","L",";"],
        ["Z","X","C","V","B","N","M",",",".","/"]]

finalText = ""

keyboard = Controller()


# Function to draw all buttons on the image with a thin green outline
def drawALL(img, buttonList):
    for button in buttonList: 
        x, y = button.pos
        w, h = button.size    

        # Draw the thin green outline (thickness=2)
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Green outline with thickness 2

        # Draw the filled rectangle inside the outline
        cv2.rectangle(img, (x + 2, y + 2), (x + w - 2, y + h - 2), (255, 0, 255), cv2.FILLED)  # Filled rectangle

        # Draw the text on top of the button
        cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4) 
    
    return img


# Button class to represent each key on the virtual keyboard
class Button():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text 

# Create a list of Button objects for each key
buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))

while True:
    success, img = cap.read()
    img = detector.findHands(img)

    # Get the position of landmarks and bounding box
    lmList, bboxInfo = detector.findPosition(img)

    # Draw all buttons on the image
    img = drawALL(img, buttonList)

    if lmList:
        for button in buttonList:
            x,y = button.pos
            w,h = button.size

            if x< lmList[8][0] <x+w and y<lmList[8][1] <y+h:
                cv2.rectangle(img, (x-10, y-10), (x + w+5, y + h+5), (175,0,175), cv2.FILLED)
                cv2.putText(img, button.text, (x + 20, y + 65),
                             cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4) 
                l, _, _ = detector.findDistance(8 ,12 ,img ,draw = False)
                print(l)
                
                #when clicked
                if l<30:
                    keyboard.press(button.text)
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0,255,0), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 65),
                               cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                    finalText += button.text
                    sleep(0.20)

    cv2.rectangle(img, (50, 350), (700, 450), (175,0,175), cv2.FILLED)
    cv2.putText(img, finalText, (60, 430),
                cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)
    
    # Show the image with virtual keyboard and hand detection
    cv2.imshow("Image", img)

    # Exit when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and destroy windows when done
cap.release()
cv2.destroyAllWindows()