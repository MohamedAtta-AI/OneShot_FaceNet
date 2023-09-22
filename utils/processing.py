from facenet_pytorch import MTCNN, InceptionResnetV1
import torch

def init_models(args):
    """Initialize the models."""
    mtcnn = MTCNN(
        min_face_size = args.min_face_size,
        thresholds=args.thresholds, 
        factor=args.factor, 
        post_process=True,
        device=args.device
    ).eval()

    resnet = InceptionResnetV1(
        pretrained='vggface2', 
        device=args.device
    ).eval()

    return mtcnn, resnet