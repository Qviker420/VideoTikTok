import cv2 
from ffpyplayer.player import MediaPlayer
import numpy as np
import os
import random
from pydub import AudioSegment
from moviepy.editor import VideoFileClip, AudioFileClip
import uuid
import download

#Add URL s in urls list, it will creat number_of_outputs duplicates for each url in this list
#For example you have 1 url and number_of_outputs = 5, it will make 5 duplicates of video from url, if you have 5 url it will make in total 25 videos 5 of each 
urls = ["https://www.tiktok.com/@daisybloomssexy/video/7302025509955702022?q=daisyblooms&t=1700329672068"]

#Change this Variable to how many duplicates you want for each url
number_of_output_videos = 1

def rotate_image(image, angle):
    image_center = tuple(np.array(image.shape[1::-1])/ 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result

def zoom(img, zoom_factor):
      return cv2.resize(img, None, fx=zoom_factor, fy=zoom_factor)

def crop_video_duration(input_path, output_path, crop_percentage):
    cap = cv2.VideoCapture(input_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    # Calculate the number of frames to keep
    num_frames_to_keep = int(total_frames * crop_percentage)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (int(cap.get(3)), int(cap.get(4))))
    # Generate a list of frame indices to keep
    frame_indices_to_keep = random.sample(range(total_frames), num_frames_to_keep)

def create_triangle_mask(size):
    mask = np.zeros(size, dtype=np.uint8)
    triangle_pts = np.array([[0, 0], [size[1], 0], [0, size[0]]], dtype=np.int32)
    cv2.fillPoly(mask, [triangle_pts], 255)
    return mask

def triangular_blur(image, mask, kernel_size):
    blurred = cv2.GaussianBlur(image, kernel_size, 0)
    result = np.where(mask[:, :, None] / 255, blurred, image)
    return result

def picture_edit(image, angle, scale):
    image = zoom(comment_image, scale)
    image = rotate_image(image, angle)
    return image


i = 0
for url in urls:
  download.download_video(url)
  #Sources
  source= 'InputVideos\\Downloaded_from_TikTok.mp4'

  #This is Main Loop
  while i < number_of_output_videos:
    cap = cv2.VideoCapture(source)
    frame_count = 0


    #Change  random_image_name = random.randint(0, change this) with number of pictures that you will have, name pictures for example 0.jpg, 1.jpg, 2.jpg etc
    random_image_name = random.randint(0, 0)
    image_path = f"CommentPictures\\{random_image_name}.JPG"
    comment_image = cv2.imread(image_path)
    comment_image = picture_edit(comment_image, random.uniform(-3.0, 3.0), random.uniform(0.3,0.5))

    print("Shape Of Image: " + str(zoom(comment_image, 0.5).shape))



    #Random Variables
    random_degree = random.uniform(-3.0, 3.0)
    scale_size = random.uniform(0.9, 0.92)
    random_brightness= random.uniform(0.8, 1.3)
    random_contrast = random.uniform(0.01, 0.05)
    random_flip = random.choice([0, 1])
    random_crop = random.randint(20, 25)
    random_blur = random.randint(55, 100)
    random_pixel_coordinate_x = np.random.randint(0, 400, 30)
    random_pixel_coordinate_y = np.random.randint(0, 400, 30)
    random_sound = random.uniform(0.2, 2.0)
    blur_triangle = 75
    random_blur_median = random.randint(1, 4)

    #Shape
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))



    #RandomFileName
    name ="OutPutVideos\\TikTok_"+str(uuid.uuid4())+".mp4"
    name_with_sound ="OutPutsWithSound\\TikTok_"+str(uuid.uuid4())+".mp4"

    #writing Video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(name, fourcc, fps, (width,  height))

    mask_size = (height, width)
    triangle_mask = create_triangle_mask(mask_size)
    
    
    random_x =random.randint(30, height-comment_image.shape[0])
    random_y =random.randint(30, width-comment_image.shape[1])

    #This Function is blurring Corners
    def blurer(frame):
        top_left_corner = triangular_blur(frame[:random_crop, :random_crop], triangle_mask[:random_crop, :random_crop], (blur_triangle, blur_triangle))
        top_right_corner = triangular_blur(frame[:random_crop, -random_crop:], triangle_mask[:random_crop, -random_crop:], (blur_triangle, blur_triangle))
        bottom_left_corner = triangular_blur(frame[-random_crop:, :random_crop], triangle_mask[-random_crop:, :random_crop], (blur_triangle, blur_triangle))
        bottom_right_corner = triangular_blur(frame[-random_crop:, -random_crop:], triangle_mask[-random_crop:, -random_crop:], (blur_triangle, blur_triangle))
        frame[:random_crop, :random_crop] = top_left_corner
        frame[:random_crop, -random_crop:] = top_right_corner
        frame[-random_crop:, :random_crop] = bottom_left_corner
        frame[-random_crop:, -random_crop:] = bottom_right_corner

    #This Loop iterates for each frame in video
    while(cap.isOpened()==True):
        ret, frame = cap.read()

        if ret == True :
    
            #Comment This if you want to disable Rotation
            frame = rotate_image(frame, random_degree) 

            #Comment This if you want to disable zoom
            frame = zoom(frame, scale_size)

            #Comment This if you want to disable brightness
            frame =cv2.convertScaleAbs(frame,random_contrast, random_brightness)

            frame_height = frame[0]
            frame_width = frame[1]
            print(width, height)
            #Comment This if you want to disable flip
            if random_flip == 0:
                frame = cv2.flip(frame, 1)
            
            #Comment This if you want to disable white pixels
            for coordinate in random_pixel_coordinate_x:
              frame[random_pixel_coordinate_x, random_pixel_coordinate_y] = (255, 255, 255)

            #Comment This if you want to disable cropping image
            frame = frame[random_crop:-random_crop, random_crop:-random_crop]
            
            #Comment This if you want to disable blurring corners
            blurer(frame)

            #DONT DISABLE THIS
            frame = cv2.resize(frame, (width, height), interpolation = cv2.INTER_AREA)  

            print("comment image _ -0 = "+ str(comment_image.shape[0]))

           
            print(random_x, random_y)
            frame[random_x:random_x+comment_image.shape[0], random_y:random_y+comment_image.shape[1], :] = comment_image
            #Comment This if you want to disable Full video blurring
            #frame = cv2.medianBlur(frame,random_blur_median)
            out.write(frame)
            # cv2.imshow('Frame', frame)
            frame_count+=1
            
            if cv2.waitKey(28) & 0xFF == ord("q"):
                break
        else:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    #Leave This Part As it is Don't experiment
    video_clip = VideoFileClip(name)
    audio_clip = AudioFileClip(source)

    temp_audio_file = "temp_audio.wav"
    audio_clip.write_audiofile(temp_audio_file, codec="pcm_s16le")

    audio_clip_modified = audio_clip.volumex(random_sound)
    final_clip = video_clip.set_audio(audio_clip_modified)
    final_clip.write_videofile(name_with_sound, codec="libx264", audio_codec="aac")
    os.remove(name)
    crop_video_duration(name_with_sound, "cropped.mp4", 0.9)
    i+=1