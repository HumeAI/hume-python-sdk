from typing import Any, Dict, Optional

from hume._clients.common.configs.model_config_base import ModelConfigBase
from hume._clients.common.model_type import ModelType


class FaceConfig(ModelConfigBase["FaceConfig"]):

    def __init__(
        self,
        fps_pred: Optional[float] = None,
        prob_threshold: Optional[float] = None,
        identify_faces: Optional[bool] = None,
        min_face_size: Optional[float] = None,
    ):
        self.fps_pred = fps_pred
        self.prob_threshold = prob_threshold
        self.identify_faces = identify_faces
        self.min_face_size = min_face_size

    def get_model_type(cls) -> ModelType:
        return ModelType.FACE

    def serialize(self) -> Dict[str, Any]:
        return {
            "fps_pred": self.fps_pred,
            "prob_threshold": self.prob_threshold,
            "identify_faces": self.identify_faces,
            "min_face_size": self.min_face_size,
        }

    @classmethod
    def deserialize(cls, request_dict: Dict[str, Any]) -> "FaceConfig":
        return cls(
            fps_pred=request_dict["fps_pred"],
            prob_threshold=request_dict["prob_threshold"],
            identify_faces=request_dict["identify_faces"],
            min_face_size=request_dict["min_face_size"],
        )
