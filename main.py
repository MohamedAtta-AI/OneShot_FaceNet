from utils.args import get_args
from utils.logging import get_logger

import torch
import numpy as np
import cv2


def perform_recognition(frame, args):
    pass


if __name__ == '__main__':
    args = get_args()
    logger = get_logger()

    # Use OpenCV to capture video/live feed
    try:
        args.input = int(args.input)
    except ValueError:
        pass
    cap = cv2.VideoCapture(args.input)

    if not cap.isOpened():
        logger.error("Video source not found or cannot be opened.")
        exit()
    
    while True:
        ret, frame = cap.read()

        # Exit the loop if video file has ended or if the Q key is pressed
        if not ret or cv2.waitKey(1) & 0xFF == ord('q'):
            break

        analysis = perform_recognition(frame, args)
        
        # Show live feed
        if isinstance(args.input, int):
            cv2.imshow('One-shot recognizer', frame)

    logger.info("Process complete!")
    
    # try:
    #     logger.error("Test #1")
    # except Exception as e:
    #     logger.error(f"An exection occurred: {str(e)}")