from utils.args import get_args
from utils.logging import get_logger
from utils.processing import *

import torch
import numpy as np
import cv2
import os


def import_profiles(folder_path):
    """Imports profiles from a file."""
    profiles = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(('.jpg', '.png', '.jpeg')): # Add more extensions if needed
            file_path = os.path.join(folder_path, filename)
            img = cv2.imread(file_path)

            img_tensor = torch.from_numpy(img).float()
            img_name = os.path.splitext(os.path.basename(filename))[0]
            profiles[img_name] = detector(img_tensor)
    return profiles


def perform_recognition(frame, args):
    c = 1
    if c >= args.batch_size:
        pass


if __name__ == '__main__':
    args = get_args()
    logger = get_logger()
    
    args.device = torch.device(f'cuda:{args.device_id}' if torch.cuda.is_available() else 'cpu')
    detector, recognizer = init_models(args)
    profiles = import_profiles(args.profiles)
    exit()
    # Use OpenCV to capture video/live feed
    try:
        args.input = int(args.input)
    except ValueError:
        pass
    cap = cv2.VideoCapture(args.input)

    if not cap.isOpened():
        logger.error("Video source not found or cannot be opened.")
        exit()
    
    
    frames = []
    while True:
        ret, frame = cap.read()

        # Exit the loop if video file has ended or if the Q key is pressed
        if not ret or cv2.waitKey(1) & 0xFF == ord('q'):
            break

        RGB_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Show live feed
        if isinstance(args.input, int):
            cv2.imshow('One-shot recognizer', frame)
            analysis = perform_recognition(RGB_frame, args)

        else:
            frames.append(RGB_frame)
            if len(frames) >= args.batch_size:
                analysis = perform_recognition(frames, args)
                frames.clear()
    
    # try:
    #     logger.error("Test #1")
    # except Exception as e:
    #     logger.error(f"An exection occurred: {str(e)}")

    cap.release()
    cap.destroyAllWindows()

    logger.info("Process complete!")