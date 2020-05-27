#imports
import numpy as np
import cv2
import pygame
import time

#Opencv video read on webcam
cap = cv2.VideoCapture(0)

#Inner rectangle (where strike is recorded) length and breadth
rectangle_dimensions = (100, 100)
#Outer rectangle (where speed of strike is recorded) length and breadth
extended_rectangle_dimensions = (150, 150)

#Images for drum-kit instruments
Hihat_image = cv2.resize(cv2.imread('../resources/HiHat.png'),rectangle_dimensions,interpolation=cv2.INTER_CUBIC) #HiHat.png
Snare_image = cv2.resize(cv2.imread('../resources/snare.png'),rectangle_dimensions,interpolation=cv2.INTER_CUBIC)
Tom5_image = cv2.resize(cv2.imread('../resources/snare.png'),rectangle_dimensions,interpolation=cv2.INTER_CUBIC)
Ride_image = cv2.resize(cv2.imread('../resources/HiHat.png'),rectangle_dimensions,interpolation=cv2.INTER_CUBIC)

#load music 
pygame.mixer.init()
HiHat_music = pygame.mixer.Sound("../resources/HiHat.wav")
Snare_music = pygame.mixer.Sound("../resources/Snare.wav")
Tom_music = pygame.mixer.Sound("../resources/Tom.wav")
Ride_music = pygame.mixer.Sound("../resources/Ride.wav")

#HiHat-left
#Snare Middle left
#Tom-5 Middle Right
#Ride Right
#Centers of the four drum instruments' rectangles
Hihat_centre = (550, 200)
Snare_centre = (250, 100)
Tom5_centre = (400, 100)
Ride_centre = (100, 200)

#To measure the speed of Strike
HiHat_speed_list = [(0,0)] * 10
Snare_speed_list = [(0,0)] * 10
Tom_speed_list = [(0,0)] * 10
Ride_speed_list = [(0,0)] * 10


#To measure strike for all 4 drum-kit instruments
HiHat_currently_struck = False
HiHat_music_played = False
Snare_currently_struck = False
Snare_music_played = False
Tom_currently_struck = False
Tom_music_played = False
Ride_currently_struck = False
Ride_music_played = False

#Calculate drum-kit rectangle edges from respective centers and inner retangle dimensions
Hihat_edges_pt1 = (int(Hihat_centre[0] - rectangle_dimensions[0]/2), int(Hihat_centre[1] - rectangle_dimensions[1]/2))
Hihat_edges_pt2 = (int(Hihat_centre[0] + rectangle_dimensions[0]/2), int(Hihat_centre[1] + rectangle_dimensions[1]/2))

Snare_edges_pt1 = (int(Snare_centre[0] - rectangle_dimensions[0]/2), int(Snare_centre[1] - rectangle_dimensions[1]/2))
Snare_edges_pt2 = (int(Snare_centre[0] + rectangle_dimensions[0]/2), int(Snare_centre[1] + rectangle_dimensions[1]/2))

Tom5_edges_pt1 = (int(Tom5_centre[0] - rectangle_dimensions[0]/2), int(Tom5_centre[1] - rectangle_dimensions[1]/2))
Tom5_edges_pt2 = (int(Tom5_centre[0] + rectangle_dimensions[0]/2), int(Tom5_centre[1] + rectangle_dimensions[1]/2))

Ride_edges_pt1 = (int(Ride_centre[0] - rectangle_dimensions[0]/2), int(Ride_centre[1] - rectangle_dimensions[1]/2))
Ride_edges_pt2 = (int(Ride_centre[0] + rectangle_dimensions[0]/2), int(Ride_centre[1] + rectangle_dimensions[1]/2))

########################################################################################
#Calculate outer speed measuring rectangle edges from respective centers and inner retangle dimensions
extended_Hihat_edges_pt1 = (int(Hihat_centre[0] - extended_rectangle_dimensions[0]/2), int(Hihat_centre[1] - extended_rectangle_dimensions[1]/2))
extended_Hihat_edges_pt2 = (int(Hihat_centre[0] + extended_rectangle_dimensions[0]/2), int(Hihat_centre[1] + extended_rectangle_dimensions[1]/2))

extended_Snare_edges_pt1 = (int(Snare_centre[0] - extended_rectangle_dimensions[0]/2), int(Snare_centre[1] - extended_rectangle_dimensions[1]/2))
extended_Snare_edges_pt2 = (int(Snare_centre[0] + extended_rectangle_dimensions[0]/2), int(Snare_centre[1] + extended_rectangle_dimensions[1]/2))

extended_Tom5_edges_pt1 = (int(Tom5_centre[0] - extended_rectangle_dimensions[0]/2), int(Tom5_centre[1] - extended_rectangle_dimensions[1]/2))
extended_Tom5_edges_pt2 = (int(Tom5_centre[0] + extended_rectangle_dimensions[0]/2), int(Tom5_centre[1] + extended_rectangle_dimensions[1]/2))

extended_Ride_edges_pt1 = (int(Ride_centre[0] - extended_rectangle_dimensions[0]/2), int(Ride_centre[1] - extended_rectangle_dimensions[1]/2))
extended_Ride_edges_pt2 = (int(Ride_centre[0] + extended_rectangle_dimensions[0]/2), int(Ride_centre[1] + extended_rectangle_dimensions[1]/2))



#Lower and Upper bounds for measuring blue color
lower_blue = np.array([110,50,50])
upper_blue = np.array([130,255,255])

blueLower = (80,150,10)
blueUpper = (120,255,255)

def play_HiHat(volume):
    '''
    Function to play HiHat music

    param:
    ----------
    volume: float between 0 and 1 indicating volume

    return:
    None
    '''
    HiHat_music.set_volume(volume)
    HiHat_music.play()

def play_Snare(volume):
    '''
    Function to play Snare music

    param:
    ----------
    volume: float between 0 and 1 indicating volume

    return:
    None
    '''
    Snare_music.set_volume(volume)
    Snare_music.play()

def play_Tom(volume):
    '''
    Function to play Tom music

    param:
    ----------
    volume: float between 0 and 1 indicating volume

    return:
    None
    '''
    Tom_music.set_volume(volume)
    Tom_music.play()

def play_Ride(volume):
    '''
    Function to play Ride music

    param:
    ----------
    volume: float between 0 and 1 indicating volume

    return:
    None
    '''
    Ride_music.set_volume(volume)
    Ride_music.play()


def draw_rectangles(frame):
    '''
    Function to draw the 4 drum-kit rectangles in the frame

    Param
    ----------
    frame: current frame

    return
    ----------
    frame: current frame with 4 drum-kit rectangles drawn

    '''
    cv2.rectangle(frame, Hihat_edges_pt1, Hihat_edges_pt2, (0,255,0), thickness=1, lineType=8, shift=0 )
    cv2.rectangle(frame, Snare_edges_pt1, Snare_edges_pt2, (0,255,0), thickness=1, lineType=8, shift=0 )
    cv2.rectangle(frame, Tom5_edges_pt1, Tom5_edges_pt2, (0,255,0), thickness=1, lineType=8, shift=0 )
    cv2.rectangle(frame, Ride_edges_pt1, Ride_edges_pt2, (0,255,0), thickness=1, lineType=8, shift=0 )    
    return frame

def draw_outer_rectangles(frame):
    '''
    Function to draw the 4 speed measuring rectangles in the frame

    Param
    ----------
    frame: current frame

    return
    ----------
    frame: current frame with 4 speed measuring rectangles drawn

    '''
    cv2.rectangle(frame, extended_Hihat_edges_pt1, extended_Hihat_edges_pt2, (255,255,0), thickness=1, lineType=8, shift=0 )
    cv2.rectangle(frame, extended_Snare_edges_pt1, extended_Snare_edges_pt2, (255,255,0), thickness=1, lineType=8, shift=0 )
    cv2.rectangle(frame, extended_Tom5_edges_pt1, extended_Tom5_edges_pt2, (255,255,0), thickness=1, lineType=8, shift=0 )
    cv2.rectangle(frame, extended_Ride_edges_pt1, extended_Ride_edges_pt2, (255,255,0), thickness=1, lineType=8, shift=0 )    
    return frame

def draw_circles(frame, HiHat_pnt,  Snare_pnt, Tom_pnt, Ride_pnt ):
    '''
    Function to draw circles corresponding to drum stick points if present inside 4 rectangles in the frame

    Param
    ----------
    frame: current frame
    HiHat_pnt: HitHat centre point 
    Snare_pnt: Snare centre point 
    Tom_pnt: Tom centre point 
    Ride_pnt: Ride centre point 

    return
    ----------
    frame: current frame with circles

    '''
    cv2.circle(frame, HiHat_pnt, 10, (0, 255, 0),thickness=3, lineType=8, shift=0)
    cv2.circle(frame, Snare_pnt, 10, (0, 255, 0),thickness=3, lineType=8, shift=0)
    cv2.circle(frame, Tom_pnt, 10, (0, 255, 0),thickness=3, lineType=8, shift=0)
    cv2.circle(frame, Ride_pnt, 10, (0, 255, 0),thickness=3, lineType=8, shift=0)
    return frame


def overlay_image_alpha(img, img_overlay, pos, alpha_mask):
    """Overlay img_overlay on top of img at the position specified by
    pos and blend using alpha_mask.

    Alpha mask must contain values within the range [0, 1] and be the
    same size as img_overlay.
    """

    x, y = pos

    # Image ranges
    y1, y2 = max(0, y), min(img.shape[0], y + img_overlay.shape[0])
    x1, x2 = max(0, x), min(img.shape[1], x + img_overlay.shape[1])

    # Overlay ranges
    y1o, y2o = max(0, -y), min(img_overlay.shape[0], img.shape[0] - y)
    x1o, x2o = max(0, -x), min(img_overlay.shape[1], img.shape[1] - x)

    # Exit if nothing to do
    if y1 >= y2 or x1 >= x2 or y1o >= y2o or x1o >= x2o:
        return

    channels = img.shape[2]

    alpha = alpha_mask[y1o:y2o, x1o:x2o]
    alpha_inv = 1.0 - alpha

    for c in range(channels):
        img[y1:y2, x1:x2, c] = (alpha * img_overlay[y1o:y2o, x1o:x2o, c] +
                                alpha_inv * img[y1:y2, x1:x2, c])


def draw_instruments(frame):
    '''
    Function to draw the 4 drum-kit instruments in the frame

    Param
    ----------
    frame: current frame

    return
    ----------
    frame: current frame with drum-kit instruments drawn

    '''
    
    frame[Hihat_edges_pt1[1]:Hihat_edges_pt2[1],Hihat_edges_pt1[0]:Hihat_edges_pt2[0]] = \
        cv2.addWeighted(Hihat_image, 0.2, frame[Hihat_edges_pt1[1]:Hihat_edges_pt2[1],Hihat_edges_pt1[0]:Hihat_edges_pt2[0]], 1, 0)

    frame[Snare_edges_pt1[1]:Snare_edges_pt2[1],Snare_edges_pt1[0]:Snare_edges_pt2[0]] = \
        cv2.addWeighted(Snare_image, 0.2, frame[Snare_edges_pt1[1]:Snare_edges_pt2[1],Snare_edges_pt1[0]:Snare_edges_pt2[0]], 1, 0)

    frame[Tom5_edges_pt1[1]:Tom5_edges_pt2[1],Tom5_edges_pt1[0]:Tom5_edges_pt2[0]] = \
        cv2.addWeighted(Tom5_image, 0.2, frame[Tom5_edges_pt1[1]:Tom5_edges_pt2[1],Tom5_edges_pt1[0]:Tom5_edges_pt2[0]], 1, 0)

    frame[Ride_edges_pt1[1]:Ride_edges_pt2[1],Ride_edges_pt1[0]:Ride_edges_pt2[0]] = \
        cv2.addWeighted(Ride_image, 0.2, frame[Ride_edges_pt1[1]:Ride_edges_pt2[1],Ride_edges_pt1[0]:Ride_edges_pt2[0]], 1, 0)
    
    return frame




def find_range(range_frame):
    '''
    Function to return the mask of the pixels where drum-stick is present 

    param:
    ----------
    range_frame: part of frame which contains instruments

    return:
    ----------
    mask: drum-stick mask
    '''
    
    hsv = cv2.cvtColor(range_frame, cv2.COLOR_BGR2HSV)
    #check if clue color is present in the coundary
    mask = cv2.inRange(hsv, blueLower, blueUpper)

    return mask

def find_overlap(frame):
    '''
    Function to return the mask of all 4 drum instrument area where drum-stick is present 

    param:
    ----------
    frame: current frame

    return:
    ----------
    mask: drum-stick mask of all 4 instruments
    '''
    #Extract instrument sized blocks of frame
    HiHat_frame = np.copy(frame[extended_Hihat_edges_pt1[1]:extended_Hihat_edges_pt2[1],extended_Hihat_edges_pt1[0]:extended_Hihat_edges_pt2[0]])
    Snare_frame = np.copy(frame[extended_Snare_edges_pt1[1]:extended_Snare_edges_pt2[1],extended_Snare_edges_pt1[0]:extended_Snare_edges_pt2[0]])
    Tom_frame = np.copy(frame[extended_Tom5_edges_pt1[1]:extended_Tom5_edges_pt2[1],extended_Tom5_edges_pt1[0]:extended_Tom5_edges_pt2[0]])
    Ride_frame = np.copy(frame[extended_Ride_edges_pt1[1]:extended_Ride_edges_pt2[1],extended_Ride_edges_pt1[0]:extended_Ride_edges_pt2[0]])

    #Find masks
    HiHat_mask = find_range(HiHat_frame)
    Snare_mask = find_range(Snare_frame)
    Tom_mask = find_range(Tom_frame)
    Ride_mask = find_range(Ride_frame)

    return HiHat_mask, Snare_mask, Tom_mask, Ride_mask



def get_centre_point(mask, edges_pt1):
    '''
    Function to calculate the centre of the mask

    param:
    ----------
    mask: drum-stick mask
    edges_pt1: Top-left corner of the drum-instrument rectangle

    return:
    ----------
    cx: center point's x-coordinate
    cy: center point's y-coordinate
    '''
    contours = cv2.findContours(mask, 0, 2)

    c = contours[0]
    M = cv2.moments(c)
    if (M['m00'] != 0):
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        cx = cx + edges_pt1[0]
        cy = cy + edges_pt1[1]
        return cx, cy
    #else:
    #    return 0, 0


def check_inner_rectangle(Centre_pnt, edges_pt1, edges_pt2):
    '''
    Function to check if drum stick is present inside the drum-kit rectangle

    param:
    ----------
    Centre_pnt: Centre point of the drum-kit rectangle
    edges_pt1: Top left corner of the drum-kit rectangle 
    edges_pt2: Bottom right corner of the drum-kit rectangle

    return:
    ----------
    True if drum stick is present inside the drum-kit rectangle
    False otherwise

    '''
    if Centre_pnt[0] > edges_pt1[0] and Centre_pnt[0] < edges_pt2[0] \
        and Centre_pnt[1] > edges_pt1[1] and Centre_pnt[1] < edges_pt2[1]:
        return True 
    return False

ride_continuous = 0
def play_music(drum,speed_list ):
    '''
    Function to play sound as according to the instrument rectangle struck 

    param:
    ----------
    drum: String to denote the instrument being struck
    speed_list: List consisting of recent 10 points of drum stick

    return:
    ----------
    None
    '''
    volume = 0.3
    
    #Calculation of Volume
    x_mean_speed = 0
    y_mean_speed = 0
    for i in range(len(speed_list)):
        x_mean_speed += speed_list[i][0]
        y_mean_speed += speed_list[i][1]
    x_mean_speed = x_mean_speed/len(speed_list)
    y_mean_speed = y_mean_speed/len(speed_list)
    x_speed = speed_list[len(speed_list)-1][0] - speed_list[0][0]
    y_speed = speed_list[len(speed_list)-1][1] - speed_list[0][1]
    if (abs(x_speed) > 40 or abs(y_speed) > 40):  
        volume = 1
    elif (abs(x_speed) > 10 or abs(y_speed) > 10):  
        volume = 0.4

    print(volume)

    
    if drum == "HiHat":
        play_HiHat(volume)
    if drum == "Snare":
        play_Snare (volume)
    if drum == "Tom":
        play_Tom(volume)
    if drum == "Ride":
        play_Ride(volume)

def ride_constant_music(speed_list ):
    '''
    Function to play Ride rhythm as according to the instrument rectangle struck continuously 

    param:
    ----------
    speed_list: List consisting of recent 10 points of drum stick

    return:
    ----------
    None
    '''
    global ride_continuous
    #Check for movement
    if speed_list[len(speed_list)-1][0] != speed_list[len(speed_list)-2][0]\
        or speed_list[len(speed_list)-1][1] != speed_list[len(speed_list)-2][1]:    
              
        if ride_continuous % 10 == 0:
            play_Ride(0.4)
            ride_continuous = 0
    ride_continuous = ride_continuous + 1

def check_strike_position(Centre_pnt, edges_pt1, edges_pt2, drum, music_played, speed_list, ride_constant):
    '''
    Function to measure stike position

    param:
    ----------
    Centre_pnt: Centre point of the drum-kit rectangle
    edges_pt1: Top left corner of the drum-kit rectangle 
    edges_pt2: Bottom right corner of the drum-kit rectangle
    drum: String to denote the instrument being struck
    music_played: indicates if music was played for that strike
    speed_list: List consisting of recent 10 points of drum stick

    return:
    ----------
    music_played: bool: if music was played
    '''
    if check_inner_rectangle(Centre_pnt, edges_pt1, edges_pt2):
        if ride_constant == False:
            play_music(drum, speed_list)
            music_played = True
        else:
            ride_constant_music(speed_list )
    return music_played




def calc_speed(speed_list, centre_pnt):
    '''
    Function to calculate speed of strike

    param:
    ----------
    speed_list: List to append drum stick points
    centre_pnt: Centre point of the drum-kit rectangle

    return:
    ----------
    speed_list: List consisting of recent 10 points of drum stick
    '''
    speed_list.append(centre_pnt)
    speed_list = speed_list[1:]
    return speed_list

    
start_time = time.time()
frame_count = 0

while(True):
    # Capture frame-by-frame
    frame_count += 1
    ret, frame = cap.read()
    
    frame = cv2.flip( frame, 1 )
    
    #Find masks
    
    HiHat_mask, Snare_mask, Tom_mask, Ride_mask = find_overlap(frame)
    


    #########################
    #Get centre points of masks in instrument region
    HiHat_pnt = get_centre_point(HiHat_mask, Hihat_edges_pt1)
    Snare_pnt = get_centre_point(Snare_mask, Snare_edges_pt1)
    Tom_pnt = get_centre_point(Tom_mask, Tom5_edges_pt1)
    Ride_pnt = get_centre_point(Ride_mask, Ride_edges_pt1)
       

    
    #If mask in HiHat region
    if HiHat_pnt:
        #Get strike speed_list
        HiHat_speed_list = calc_speed(HiHat_speed_list, HiHat_pnt )
        #If music not played for this strike
        if HiHat_currently_struck == True and HiHat_music_played == True:
            pass
        else:
            #Check the strike position
            #HiHat_music_played = check_strike_position(HiHat_pnt, Hihat_edges_pt1, Hihat_edges_pt2, "HiHat", HiHat_music_played, HiHat_speed_list, ride_constant = False )
            HiHat_music_played = check_strike_position(HiHat_pnt, extended_Hihat_edges_pt1, extended_Hihat_edges_pt2, "HiHat", HiHat_music_played, HiHat_speed_list, ride_constant = False )
            HiHat_currently_struck = True
    else:
        HiHat_currently_struck = False
        HiHat_music_played = False

    #If mask in Snare region
    if Snare_pnt:
        #Get strike speed_list
        Snare_speed_list = calc_speed(Snare_speed_list, Snare_pnt )
        #If music not played for this strike
        if Snare_currently_struck == True and Snare_music_played == True:
            pass
        else:
            Snare_music_played = check_strike_position(Snare_pnt, extended_Snare_edges_pt1, extended_Snare_edges_pt2, "Snare", Snare_music_played, Snare_speed_list, ride_constant = False )
            Snare_currently_struck = True
    else:
        Snare_currently_struck = False
        Snare_music_played = False

    #If mask in Tom region
    if Tom_pnt:
        #Get strike speed_list
        Tom_speed_list = calc_speed(Tom_speed_list, Tom_pnt )
        #If music not played for this strike
        if Tom_currently_struck == True and Tom_music_played == True:
            pass
        else:
            Tom_music_played = check_strike_position(Tom_pnt, extended_Tom5_edges_pt1, extended_Tom5_edges_pt2, "Tom", Tom_music_played, Tom_speed_list, ride_constant = False )
            Tom_currently_struck = True
    else:
        Tom_currently_struck = False
        Tom_music_played = False

    #If mask in Ride region
    if Ride_pnt:
        #Get strike speed_list
        Ride_speed_list = calc_speed(Ride_speed_list, Ride_pnt )
        #If music not played for this strike
        if Ride_currently_struck == True and Ride_music_played == True:
            Ride_music_played = check_strike_position(Ride_pnt, extended_Ride_edges_pt1, extended_Ride_edges_pt2, "Ride", Ride_music_played, Ride_speed_list, ride_constant = True )
        else:
            Ride_music_played = check_strike_position(Ride_pnt, extended_Ride_edges_pt1, extended_Ride_edges_pt2, "Ride", Ride_music_played, Ride_speed_list, ride_constant = False )
            Ride_currently_struck = True
    else:
        Ride_currently_struck = False
        Ride_music_played = False


    #######################
    #frame = draw_rectangles(frame)
    #frame = draw_outer_rectangles(frame)
    #frame = draw_circles(frame, HiHat_pnt,  Snare_pnt, Tom_pnt, Ride_pnt )
    frame = draw_instruments(frame)
    
    current_time = time.time() - start_time
    #print("Time taken : {0} seconds".format(current_time))
    
    fps  = frame_count / current_time
    #print("Estimated frames per second : {0}".format(fps))

    cv2.putText(frame,"Ride", (60, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255))
    cv2.putText(frame,"Snare", (200, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255))
    cv2.putText(frame,"Tom", (350, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255))
    cv2.putText(frame,"Hihat", (500, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255))
    # Display the resulting frame
    cv2.imshow('Virtual-drums',frame)
    #if cv2.waitKey(1) == ord('m'):  
    #    play_HiHat(1)
    #if cv2.waitKey(1) == ord('n'):  
    #    play_Snare(1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()