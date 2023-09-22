import argparse

def get_args():
    parser = argparse.ArgumentParser(description="One-shot face recognition with FaceNet-PyTorch")

    parser.add_argument(
        "--input", 
        type=str, 
        default='0',
        help="Input video source. You can either write specify video file path or a device id for live camera feed (default: 0)."
    )
    parser.add_argument(
        "--profiles",
        type=str,
        default='./profiles',
        help="Path to profile pictures (default: './profiles')."
    )
    parser.add_argument(
        "--output", 
        type=str,
        default=None, 
        help="Path to save the output video. If not specified, it does not get saved."
    )
    parser.add_argument(
        "--device_id", 
        default=0, 
        type=int, 
        help='GPU device id to use (default: 0). Uses the cpu if the specified gpu was not available.'
    )
    parser.add_argument(
        "--batch_size",
        default=1,
        type=int,
        help="Perform batched recognition for better perfomance (default: 1). This works for pre-recorded video files only."
    )
    parser.add_argument(
        "--similarity-threshold", 
        type=float, 
        default=0.5,
        help="Threshold for face recognition similarity score (default: 0.5)."
    )
    parser.add_argument(
        "--thresholds",
        type=float,
        nargs='+',
        default=[0.6, 0.7, 0.7],
        help="MTCNN face detection thresholds (default: {[0.6, 0.7, 0.7]}).",
    )
    parser.add_argument(
        "--factor",
        type=float,
        default=0.709,
        help="Factor used to create a scaling pyramid of face sizes. (default: 0.709)"
    )
    parser.add_argument(
        "--min-face-size",
        type=int,
        default=20,
        help="Minimum face size for detection in pixels (default: 20).",
    )

    args = parser.parse_args()
    return args