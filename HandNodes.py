import cv2
import mediapipe as mp
import os
import json

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

file = open("hand_landmarks.json", "w")

with mp_hands.Hands(static_image_mode=True, max_num_hands=2, min_detection_confidence=0.5) as hands:
  data={}
  for idx, videoFile in enumerate(os.listdir('videos/')):
    if videoFile.endswith('.mp4'):
        video = os.path.join('videos/', videoFile)
        data[video.split(".")[0].split("/")[-1]] = []
        cap = cv2.VideoCapture(video)
        frame = 0
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                break
            image=cv2.resize(image,(640,480))
            results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            if results.multi_hand_landmarks:
                handCords = []
                for hand_landmarks in results.multi_hand_landmarks:
                    hand=hand_landmarks.landmark
                    if hand[mp_hands.HandLandmark.WRIST].x < hand[mp_hands.HandLandmark.THUMB_TIP].x:
                        handType = "Left"
                    else:
                        handType = "Right"
                    for joint_id, landmark in enumerate(hand):
                        x,y,z=landmark.x,landmark.y,landmark.z
                        handCords.append({"joint_id":joint_id,"x":x,"y":y,"z":z})
                    mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                data[video.split(".")[0].split("/")[-1]].append({
                    "Frame Number: ": frame,
                    "Left Hand Coordinates: ": handCords if handType == "Left" else[],
                    "Right Hand Coordinates: ": handCords if handType == "Right" else[]
                })
                frame += 1
                
                cv2.imshow('Hand Tracking', image)
                if cv2.waitKey(5) & 0xFF == ord('q'):
                    break
        cap.release()
    json.dump(data, file)
file.close()