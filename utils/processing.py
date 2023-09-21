from facenet_pytorch import MTCNN, InceptionResnetV1
import torch

def init_models(**kwargs):
    """Initialize the models."""
    mtcnn = MTCNN(
        image_size=160, margin=0, min_face_size=20,
        thresholds=[0.6, 0.7, 0.7], factor=0.709, post_process=True,
        device=device
    )
    resnet = InceptionResnetV1(pretrained='vggface2', device=device).eval()