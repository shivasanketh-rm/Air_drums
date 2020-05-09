import numpy as np
import cv2
import pygame

cap = cv2.VideoCapture(0)

rectangle_dimensions = (100, 100)
Hihat_image = cv2.resize(cv2.imread('../resources/HiHat.png'),rectangle_dimensions,interpolation=cv2.INTER_CUBIC) #HiHat.png
Snare_image = cv2.resize(cv2.imread('../resources/snare.png'),rectangle_dimensions,interpolation=cv2.INTER_CUBIC)
Tom5_image = cv2.resize(cv2.imread('../resources/snare.png'),rectangle_dimensions,interpolation=cv2.INTER_CUBIC)
Ride_image = cv2.resize(cv2.imread('../resources/HiHat.png'),rectangle_dimensions,interpolation=cv2.INTER_CUBIC)

pygame.mixer.init()
HiHat_music = pygame.mixer.Sound("../resources/HiHat.wav")
Snare_music = pygame.mixer.Sound("../resources/Snare.wav")
Tom_music = pygame.mixer.Sound("../resources/Tom.wav")
Ride_music = pygame.mixer.Sound("../resources/Ride.wav")

#HiHat-left
#Snare Middle left
#Tom-5 Middle Right
#Ride Right
Hihat_centre = (100, 300)
Snare_centre = (250, 400)
Tom5_centre = (400, 400)
Ride_centre = (550, 300)

rectangle_dimensions = (100, 100)
Hihat_edges_pt1 = (int(Hihat_centre[0] - rectangle_dimensions[0]/2), int(Hihat_centre[1] - rectangle_dimensions[1]/2))
Hihat_edges_pt2 = (int(Hihat_centre[0] + rectangle_dimensions[0]/2), int(Hihat_centre[1] + rectangle_dimensions[1]/2))

Snare_edges_pt1 = (int(Snare_centre[0] - rectangle_dimensions[0]/2), int(Snare_centre[1] - rectangle_dimensions[1]/2))
Snare_edges_pt2 = (int(Snare_centre[0] + rectangle_dimensions[0]/2), int(Snare_centre[1] + rectangle_dimensions[1]/2))

Tom5_edges_pt1 = (int(Tom5_centre[0] - rectangle_dimensions[0]/2), int(Tom5_centre[1] - rectangle_dimensions[1]/2))
Tom5_edges_pt2 = (int(Tom5_centre[0] + rectangle_dimensions[0]/2), int(Tom5_centre[1] + rectangle_dimensions[1]/2))

Ride_edges_pt1 = (int(Ride_centre[0] - rectangle_dimensions[0]/2), int(Ride_centre[1] - rectangle_dimensions[1]/2))
Ride_edges_pt2 = (int(Ride_centre[0] + rectangle_dimensions[0]/2), int(Ride_centre[1] + rectangle_dimensions[1]/2))

def draw_rectangles(frame):
    cv2.rectangle(frame, Hihat_edges_pt1, Hihat_edges_pt2, (0,255,0), thickness=1, lineType=8, shift=0 )
    cv2.rectangle(frame, Snare_edges_pt1, Snare_edges_pt2, (0,255,0), thickness=1, lineType=8, shift=0 )
    cv2.rectangle(frame, Tom5_edges_pt1, Tom5_edges_pt2, (0,255,0), thickness=1, lineType=8, shift=0 )
    cv2.rectangle(frame, Ride_edges_pt1, Ride_edges_pt2, (0,255,0), thickness=1, lineType=8, shift=0 )    

def draw_instruments(frame):

    frame[Hihat_edges_pt1[1]:Hihat_edges_pt2[1],Hihat_edges_pt1[0]:Hihat_edges_pt2[0]] = \
        cv2.addWeighted(Hihat_image, 1, frame[Hihat_edges_pt1[1]:Hihat_edges_pt2[1],Hihat_edges_pt1[0]:Hihat_edges_pt2[0]], 1, 0)

    frame[Snare_edges_pt1[1]:Snare_edges_pt2[1],Snare_edges_pt1[0]:Snare_edges_pt2[0]] = \
        cv2.addWeighted(Snare_image, 1, frame[Snare_edges_pt1[1]:Snare_edges_pt2[1],Snare_edges_pt1[0]:Snare_edges_pt2[0]], 1, 0)

    frame[Tom5_edges_pt1[1]:Tom5_edges_pt2[1],Tom5_edges_pt1[0]:Tom5_edges_pt2[0]] = \
        cv2.addWeighted(Tom5_image, 1, frame[Tom5_edges_pt1[1]:Tom5_edges_pt2[1],Tom5_edges_pt1[0]:Tom5_edges_pt2[0]], 1, 0)

    frame[Ride_edges_pt1[1]:Ride_edges_pt2[1],Ride_edges_pt1[0]:Ride_edges_pt2[0]] = \
        cv2.addWeighted(Ride_image, 1, frame[Ride_edges_pt1[1]:Ride_edges_pt2[1],Ride_edges_pt1[0]:Ride_edges_pt2[0]], 1, 0)        
    return frame

lower_blue = np.array([110,50,50])
upper_blue = np.array([130,255,255])

def find_range(range_frame):
    hsv = cv2.cvtColor(range_frame, cv2.COLOR_BGR2HSV)
    
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    return mask

def find_overlap(frame):
    HiHat_frame = np.copy(frame[Hihat_edges_pt1[1]:Hihat_edges_pt2[1],Hihat_edges_pt1[0]:Hihat_edges_pt2[0]])
    Snare_frame = np.copy(frame[Snare_edges_pt1[1]:Snare_edges_pt2[1],Snare_edges_pt1[0]:Snare_edges_pt2[0]])
    Tom_frame = np.copy(frame[Tom5_edges_pt1[1]:Tom5_edges_pt2[1],Tom5_edges_pt1[0]:Tom5_edges_pt2[0]])
    Ride_frame = np.copy(frame[Ride_edges_pt1[1]:Ride_edges_pt2[1],Ride_edges_pt1[0]:Ride_edges_pt2[0]])

    HiHat_mask = find_range(HiHat_frame)
    Snare_mask = find_range(Snare_frame)
    Tom_mask = find_range(Tom_frame)
    Ride_mask = find_range(Ride_frame)

    return HiHat_mask, Snare_mask, Tom_mask, Ride_mask

def play_HiHat(volume):
    HiHat_music.set_volume(volume)
    HiHat_music.play()

def play_Snare(volume):
    Snare_music.set_volume(volume)
    Snare_music.play()

def play_Tom(volume):
    Tom_music.set_volume(volume)
    Tom_music.play()

def play_Ride(volume):
    Ride_music.set_volume(volume)
    Ride_music.play()




def check_strike(HiHat_mask, Snare_mask, Tom_mask, Ride_mask):
    if np.sum(HiHat_mask) > rectangle_dimensions[0] * rectangle_dimensions[1] * 0.7:
        play_HiHat(0.8)
    if np.sum(Snare_mask) > rectangle_dimensions[0] * rectangle_dimensions[1] * 0.7:
        play_Snare(0.8)
    if np.sum(Tom_mask) > rectangle_dimensions[0] * rectangle_dimensions[1] * 0.7:
        play_Tom(0.8)
    if np.sum(Ride_mask) > rectangle_dimensions[0] * rectangle_dimensions[1] * 0.7:
        play_Ride(0.8)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    #draw_rectangles(frame)
    frame = draw_instruments(frame)
    
    HiHat_mask, Snare_mask, Tom_mask, Ride_mask = find_overlap(frame)
    check_strike(HiHat_mask, Snare_mask, Tom_mask, Ride_mask)


    # Display the resulting frame
    cv2.imshow('air-drums',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()