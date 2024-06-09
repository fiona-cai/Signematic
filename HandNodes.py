import cv2
import mediapipe as mp
import os
import json

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

file = open("hand_landmarks.json", "w")

with mp_hands.Hands(
    static_image_mode=True, max_num_hands=2, min_detection_confidence=0.5
) as hands:
    data = {}
    for idx, videoFile in enumerate(os.listdir("videos/")):
        if videoFile.endswith(".mp4"):
            video = os.path.join("videos/", videoFile)
            data[video.split(".")[0].split("/")[-1]] = []
            cap = cv2.VideoCapture(video)
            frame = 0
            while cap.isOpened():
                success, image = cap.read()
                if not success:
                    break
                image = cv2.resize(image, (1000, 800))
                results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
                if results.multi_hand_landmarks:
                    handCords = {}
                    for hand_landmarks in results.multi_hand_landmarks:
                        hand = hand_landmarks.landmark
                        if (
                            hand[mp_hands.HandLandmark.WRIST].x
                            < hand[mp_hands.HandLandmark.THUMB_TIP].x
                        ):
                            handType = "Left"
                        else:
                            handType = "Right"
                        for joint_id, landmark in enumerate(hand):
                            x, y, z = landmark.x, landmark.y, landmark.z
                            handCords[joint_id] = [x, y, z]
                        mp_drawing.draw_landmarks(
                            image, hand_landmarks, mp_hands.HAND_CONNECTIONS
                        )
                    data[video.split(".")[0].split("/")[-1]].append(
                        {
                            "Frame Number": frame,
                            "Left Hand Coordinates": (
                                handCords if handType == "Left" else []
                            ),
                            "Right Hand Coordinates": (
                                handCords if handType == "Right" else []
                            ),
                        }
                    )
                    frame += 1
                    cv2.imshow("Hand Tracking", image)
                    if cv2.waitKey(5) & 0xFF == ord("q"):
                        break
            cap.release()
            print(
                "Hand Landmarks for video: ",
                video.split("/")[-1],
                " extracted successfully with ",
                str(frame),
                " frames",
            )
    json.dump(data, file)
file.close()

# Interpolate gaps between frames
for word in data:
    frames = data[word]
    num_frames = len(frames)
    if num_frames > 1:
        interpolated_frames = []
        for i in range(num_frames - 1):
            currentFrame = frames[i]
            nextFrame = frames[i + 1]
            if nextFrame["Frame Number"] - currentFrame["Frame Number"] > 1:
                gap = nextFrame["Frame Number"] - currentFrame["Frame Number"]
                for j in range(1, gap):
                    ratio = j / gap
                    coordinates = []
                    for joint_id in range(21):
                        currentCords = currentFrame["Left Hand Coordinates"][joint_id]
                        nextCords = nextFrame["Left Hand Coordinates"][joint_id]
                        coordinates.append(
                            {
                                "x": currentCords[0]
                                + (nextCords[0] - currentCords[0]) * ratio,
                                "y": currentCords[1]
                                + (nextCords[1] - currentCords[1]) * ratio,
                                "z": currentCords[2]
                                + (nextCords[2] - currentCords[2]) * ratio,
                            }
                        )
                    interpolated_frames.append(
                        {
                            "Frame Number": currentFrame["Frame Number"] + j,
                            "Left Hand Coordinates": coordinates,
                            "Right Hand Coordinates": coordinates,
                        }
                    )
        frames.extend(interpolated_frames)

file = open("hand_landmarks.json", "w")
json.dump(data, file)
file.close()