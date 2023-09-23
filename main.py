from utils.args import get_args
from utils.logging import get_logger
from utils.processing import *

import torch
import numpy as np
import cv2
import os
from tqdm import tqdm


def import_profiles(folder_path):
    """Imports profiles from a file."""
    profiles = {}
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        img = cv2.imread(file_path)

        img_tensor = torch.from_numpy(img).float()
        img_name = os.path.splitext(os.path.basename(filename))[0]
        profiles[img_name] = recognizer(detector(img_tensor).to(args.device))
    return profiles


def perform_recognition(frames, args):
    """Performs recognition on the given frame and returns its name (if recognized), or Unknown otherwise."""
    # Get face coordinates and crop them
    batch_boxes, _ = detector.detect(frames)
    faces = detector.extract(frames, batch_boxes, None)
    faces = torch.cat([tensor if tensor is not None else torch.zeros((1,3,160,160)) for tensor in faces])
    
    frames_embeddings = recognizer(faces.to(args.device))
    profile_embeddings = torch.cat(list(args.profiles.values()))
    names = list(args.profiles.keys())
    
    max_idxs = torch.argmax(torch.matmul(profile_embeddings, frames_embeddings.T), dim=0)
    recognitions = [names[max_idx] for max_idx in max_idxs]
    
    draw_boxes(frames, recognitions, batch_boxes)


def draw_boxes(frames, names, batch_boxes):
    """Draws bounding boxes around detected faces of each frame passed to it."""
    # Draw boxes and names
    for frame, boxes in zip(frames, batch_boxes):
        if boxes is not None:
            for box, name in zip(boxes, names):
                x, y, w, h = map(int, box)
                cv2.rectangle(frame, (x, y), (w, h), (0, 255, 0), 2)
                cv2.putText(frame, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        out.write(frame)


if __name__ == '__main__':
    try: 
        args = get_args()
        logger = get_logger()
        
        args.device = torch.device(f'cuda:{args.device_id}' if torch.cuda.is_available() else 'cpu')
        detector, recognizer = init_models(args)
        logger.info("Models initialized.")

        args.profiles = import_profiles(args.profiles)
        logger.info("Profiles loaded sucessfully.")
        
        # Use OpenCV to capture video/live feed
        try:
            args.input = int(args.input)
        except ValueError:
            pass
        cap = cv2.VideoCapture(args.input)

        # Determine number of frame splits to be sent for batched detection
        v_len = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        splits = v_len / args.batch_size if v_len >= args.batch_size else v_len
        counter = 1

        if not cap.isOpened():
            logger.error("Video source not found or cannot be opened.")
            exit()

        
        # Create output video
        # Define video properties
        output_path = 'output.mp4'
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        fps = 30.0
        frame_size = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        out = cv2.VideoWriter(output_path, fourcc, fps, frame_size)
        
        
        frames = []
        while True:
            ret, frame = cap.read()

            # Exit the loop if video file has ended or if the Q key is pressed
            if not ret or cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
            # Show live feed
            if isinstance(args.input, int):
                cv2.imshow('One-shot recognizer', frame)
                analysis = perform_recognition(frame, args)

            # Perform batched detection on pre-recorded video
            else:
                frames.append(frame)
                if len(frames) >= args.batch_size or counter > splits:
                    analysis = perform_recognition(frames, args)
                    frames.clear()
                    counter += 1

        cap.release()
        out.release()
        cv2.destroyAllWindows()

        logger.info("Process complete!")
    
    except Exception as e:
        logger.error(f"An exection occurred: {str(e)}")