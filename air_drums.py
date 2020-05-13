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
Hihat_centre = (100, 200)
Snare_centre = (250, 100)
Tom5_centre = (400, 100)
Ride_centre = (550, 200)

rectangle_dimensions = (100, 100)
extended_rectangle_dimensions = (125, 125)

HiHat_currently_struck = False
HiHat_music_played = False
Snare_currently_struck = False
Snare_music_played = False
Tom_currently_struck = False
Tom_music_played = False
Ride_currently_struck = False
Ride_music_played = False

Hihat_edges_pt1 = (int(Hihat_centre[0] - rectangle_dimensions[0]/2), int(Hihat_centre[1] - rectangle_dimensions[1]/2))
Hihat_edges_pt2 = (int(Hihat_centre[0] + rectangle_dimensions[0]/2), int(Hihat_centre[1] + rectangle_dimensions[1]/2))

Snare_edges_pt1 = (int(Snare_centre[0] - rectangle_dimensions[0]/2), int(Snare_centre[1] - rectangle_dimensions[1]/2))
Snare_edges_pt2 = (int(Snare_centre[0] + rectangle_dimensions[0]/2), int(Snare_centre[1] + rectangle_dimensions[1]/2))

Tom5_edges_pt1 = (int(Tom5_centre[0] - rectangle_dimensions[0]/2), int(Tom5_centre[1] - rectangle_dimensions[1]/2))
Tom5_edges_pt2 = (int(Tom5_centre[0] + rectangle_dimensions[0]/2), int(Tom5_centre[1] + rectangle_dimensions[1]/2))

Ride_edges_pt1 = (int(Ride_centre[0] - rectangle_dimensions[0]/2), int(Ride_centre[1] - rectangle_dimensions[1]/2))
Ride_edges_pt2 = (int(Ride_centre[0] + rectangle_dimensions[0]/2), int(Ride_centre[1] + rectangle_dimensions[1]/2))

########################################################################################
extended_Hihat_edges_pt1 = (int(Hihat_centre[0] - extended_rectangle_dimensions[0]/2), int(Hihat_centre[1] - extended_rectangle_dimensions[1]/2))
extended_Hihat_edges_pt2 = (int(Hihat_centre[0] + extended_rectangle_dimensions[0]/2), int(Hihat_centre[1] + extended_rectangle_dimensions[1]/2))

extended_Snare_edges_pt1 = (int(Snare_centre[0] - extended_rectangle_dimensions[0]/2), int(Snare_centre[1] - extended_rectangle_dimensions[1]/2))
extended_Snare_edges_pt2 = (int(Snare_centre[0] + extended_rectangle_dimensions[0]/2), int(Snare_centre[1] + extended_rectangle_dimensions[1]/2))

extended_Tom5_edges_pt1 = (int(Tom5_centre[0] - extended_rectangle_dimensions[0]/2), int(Tom5_centre[1] - extended_rectangle_dimensions[1]/2))
extended_Tom5_edges_pt2 = (int(Tom5_centre[0] + extended_rectangle_dimensions[0]/2), int(Tom5_centre[1] + extended_rectangle_dimensions[1]/2))

extended_Ride_edges_pt1 = (int(Ride_centre[0] - extended_rectangle_dimensions[0]/2), int(Ride_centre[1] - extended_rectangle_dimensions[1]/2))
extended_Ride_edges_pt2 = (int(Ride_centre[0] + extended_rectangle_dimensions[0]/2), int(Ride_centre[1] + extended_rectangle_dimensions[1]/2))

def draw_rectangles(frame):
    cv2.rectangle(frame, Hihat_edges_pt1, Hihat_edges_pt2, (0,255,0), thickness=1, lineType=8, shift=0 )
    cv2.rectangle(frame, Snare_edges_pt1, Snare_edges_pt2, (0,255,0), thickness=1, lineType=8, shift=0 )
    cv2.rectangle(frame, Tom5_edges_pt1, Tom5_edges_pt2, (0,255,0), thickness=1, lineType=8, shift=0 )
    cv2.rectangle(frame, Ride_edges_pt1, Ride_edges_pt2, (0,255,0), thickness=1, lineType=8, shift=0 )    
    return frame

def draw_circles(frame, HiHat_pnt,  Snare_pnt, Tom_pnt, Ride_pnt ):
    cv2.circle(frame, HiHat_pnt, 10, (0, 255, 0),thickness=3, lineType=8, shift=0)
    cv2.circle(frame, Snare_pnt, 10, (0, 255, 0),thickness=3, lineType=8, shift=0)
    cv2.circle(frame, Tom_pnt, 10, (0, 255, 0),thickness=3, lineType=8, shift=0)
    cv2.circle(frame, Ride_pnt, 10, (0, 255, 0),thickness=3, lineType=8, shift=0)
    return frame

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

blueLower = (80,150,10)
blueUpper = (120,255,255)

def find_range(range_frame):
    hsv = cv2.cvtColor(range_frame, cv2.COLOR_BGR2HSV)
    
    mask = cv2.inRange(hsv, blueLower, blueUpper)

    return mask

def find_overlap(frame):
    HiHat_frame = np.copy(frame[extended_Hihat_edges_pt1[1]:extended_Hihat_edges_pt2[1],extended_Hihat_edges_pt1[0]:extended_Hihat_edges_pt2[0]])
    Snare_frame = np.copy(frame[extended_Snare_edges_pt1[1]:extended_Snare_edges_pt2[1],extended_Snare_edges_pt1[0]:extended_Snare_edges_pt2[0]])
    Tom_frame = np.copy(frame[extended_Tom5_edges_pt1[1]:extended_Tom5_edges_pt2[1],extended_Tom5_edges_pt1[0]:extended_Tom5_edges_pt2[0]])
    Ride_frame = np.copy(frame[extended_Ride_edges_pt1[1]:extended_Ride_edges_pt2[1],extended_Ride_edges_pt1[0]:extended_Ride_edges_pt2[0]])

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

def get_centre_point(mask, edges_pt1):
    contours = cv2.findContours(mask, 0, 2)

    c = contours[0]
    M = cv2.moments(c)
    if (M['m00'] != 0):
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        cx = cx + edges_pt1[0]
        cy = cy + edges_pt1[1]
        return cx, cy
'''
def check_strike(HiHat_mask, Snare_mask, Tom_mask, Ride_mask):
    global currently_struck
    if np.sum(HiHat_mask) > rectangle_dimensions[0] * rectangle_dimensions[1] * 0.7:
        if currently_struck == True:
            print("passing HiHat")
            pass
        else:
            play_HiHat(0.8)
            currently_struck = True
    else:
        currently_struck = False
    if np.sum(Snare_mask) > rectangle_dimensions[0] * rectangle_dimensions[1] * 0.7:
        play_Snare(0.8)
    if np.sum(Tom_mask) > rectangle_dimensions[0] * rectangle_dimensions[1] * 0.7:
        play_Tom(0.8)
    if np.sum(Ride_mask) > rectangle_dimensions[0] * rectangle_dimensions[1] * 0.7:
        play_Ride(0.8)'''

def check_inner_rectangle(Centre_pnt, edges_pt1, edges_pt2):
    if Centre_pnt[0] > edges_pt1[0] and Centre_pnt[0] < edges_pt2[0] \
        and Centre_pnt[1] > edges_pt1[1] and Centre_pnt[1] < edges_pt2[1]:
        return True 
    return False

def play_music(drum):
    if drum == "HiHat":
        play_HiHat(0.8)
    if drum == "Snare":
        play_Snare (0.8)
    if drum == "Tom":
        play_Tom(0.8)
    if drum == "Ride":
        play_Ride(0.8)



def check_strike_position(Centre_pnt, edges_pt1, edges_pt2, drum, music_played):
    if check_inner_rectangle(Centre_pnt, edges_pt1, edges_pt2):
        play_music(drum)
        music_played = True
    return music_played


while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    frame = cv2.flip( frame, 1 )
    
    
    HiHat_mask, Snare_mask, Tom_mask, Ride_mask = find_overlap(frame)
    #check_strike(HiHat_mask, Snare_mask, Tom_mask, Ride_mask)


    #########################
    HiHat_pnt = get_centre_point(HiHat_mask, Hihat_edges_pt1)
    Snare_pnt = get_centre_point(Snare_mask, Snare_edges_pt1)
    Tom_pnt = get_centre_point(Tom_mask, Tom5_edges_pt1)
    Ride_pnt = get_centre_point(Ride_mask, Ride_edges_pt1)

    

    if HiHat_pnt:
        if HiHat_currently_struck == True and HiHat_music_played == True:
            pass
        else:
            HiHat_music_played = check_strike_position(HiHat_pnt, Hihat_edges_pt1, Hihat_edges_pt2, "HiHat", HiHat_music_played )
            HiHat_currently_struck = True
    else:
        HiHat_currently_struck = False
        HiHat_music_played = False

    if Snare_pnt:
        if Snare_currently_struck == True and Snare_music_played == True:
            pass
        else:
            Snare_music_played = check_strike_position(Snare_pnt, Snare_edges_pt1, Snare_edges_pt2, "Snare", Snare_music_played )
            Snare_currently_struck = True
    else:
        Snare_currently_struck = False
        Snare_music_played = False

    if Tom_pnt:
        if Tom_currently_struck == True and Tom_music_played == True:
            pass
        else:
            Tom_music_played = check_strike_position(Tom_pnt, Tom5_edges_pt1, Tom5_edges_pt2, "Tom", Tom_music_played )
            Tom_currently_struck = True
    else:
        Tom_currently_struck = False
        Tom_music_played = False

    if Ride_pnt:
        if Ride_currently_struck == True and Ride_music_played == True:
            pass
        else:
            Ride_music_played = check_strike_position(Ride_pnt, Ride_edges_pt1, Ride_edges_pt2, "Ride", Ride_music_played )
            Ride_currently_struck = True
    else:
        Ride_currently_struck = False
        Ride_music_played = False




    #######################
    #frame = draw_rectangles(frame)
    frame = draw_circles(frame, HiHat_pnt,  Snare_pnt, Tom_pnt, Ride_pnt )
    frame = draw_instruments(frame)
    
    # Display the resulting frame
    cv2.imshow('air-drums',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()