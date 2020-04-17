import cv2
import os

def VideoMaker(image_folder,video_name):

    #create a video file by compiling a series of png images

    images=[img for img in os.listdir(image_folder) if img.endswith('.png')]
    images.sort()

    frame=cv2.imread(os.path.join(image_folder,images[0]))
    height,width,layers=frame.shape

    video=cv2.VideoWriter(video_name,0,30,(width,height))

    for image in images:
        video.write(cv2.imread(os.path.join(image_folder,image)))

    cv2.destroyAllWindows()
    video.release()

Uncovered_folder='Uncovered/Uncovered_figs'
Uncovered_name='SimulationUncovered.avi'
Uncovered_folder_cross='Uncovered/cross_section_figs'
Uncovered_name_cross='SimulationUncovered_cross_section.avi'

Torbjorn_folder='Example/fem_figs'
Torbjorn_name='fem_axon_tunnel.avi'

S4_folder='S4/S4_figs'
S4_name='SimulationS4.avi'
S4_folder_cross='S4/cross_section_figs'
S4_name_cross='SimulationS4_cross_section.avi'

S6_folder='S6/S6_figs'
S6_name='SimulationS6.avi'
S6_folder_cross='S6/cross_section_figs'
S6_name_cross='SimulationS6_cross_section.avi'

# VideoMaker(Uncovered_folder,Uncovered_name)
# VideoMaker(Uncovered_folder_cross,Uncovered_name_cross)

# VideoMaker(Torbjorn_folder,Torbjorn_name)

# VideoMaker(S4_folder,S4_name)
# VideoMaker(S4_folder_cross,S4_name_cross)

# VideoMaker(S6_folder,S6_name)
# VideoMaker(S6_folder_cross,S6_name_cross)

