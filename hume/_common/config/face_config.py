"""Configuration for the facial expression model."""
from typing import Any, Dict, Optional

from hume._common.config.job_config_base import JobConfigBase
from hume._common.model_type import ModelType


class FaceConfig(JobConfigBase["FaceConfig"]):
    """Configuration for the facial expression model."""

    def __init__(
        self,
        *,
        fps_pred: Optional[float] = None,
        prob_threshold: Optional[float] = None,
        identify_faces: Optional[bool] = None,
        min_face_size: Optional[float] = None,
    ):
        """Construct a `FaceConfig`.

        Args:
            fps_pred (Optional[float]): Number of frames per second to process. Other frames will be omitted
                from the response.
            prob_threshold (Optional[float]): Face detection probability threshold. Faces detected with a
                probability less than this threshold will be omitted from the response.
            identify_faces (Optional[bool]): Whether to return identifiers for faces across frames.
                If true, unique identifiers will be assigned to face bounding boxes to differentiate different faces.
                If false, all faces will be tagged with an "unknown" ID.
            min_face_size (Optional[float]): Minimum bounding box side length in pixels to treat as a face.
                Faces detected with a bounding box side length in pixels less than this threshold will be
                omitted from the response.
        """
        self.fps_pred = fps_pred
        self.prob_threshold = prob_threshold
        self.identify_faces = identify_faces
        self.min_face_size = min_face_size

    @classmethod
    def get_model_type(cls) -> ModelType:
        """Get the configuration model type.

        Returns:
            ModelType: Model type.
        """
        return ModelType.FACE

    def serialize(self) -> Dict[str, Any]:
        """Serialize `FaceConfig` to dictionary.

        Returns:
            Dict[str, Any]: Serialized `FaceConfig` object.
        """
        return {
            "fps_pred": self.fps_pred,
            "prob_threshold": self.prob_threshold,
            "identify_faces": self.identify_faces,
            "min_face_size": self.min_face_size,
        }

    @classmethod
    def deserialize(cls, request_dict: Dict[str, Any]) -> "FaceConfig":
        """Deserialize `FaceConfig` from request JSON.

        Args:
            request_dict (Dict[str, Any]): Request JSON data.

        Returns:
            FaceConfig: Deserialized `FaceConfig` object.
        """
        return cls(
            fps_pred=request_dict.get("fps_pred"),
            prob_threshold=request_dict.get("prob_threshold"),
            identify_faces=request_dict.get("identify_faces"),
            min_face_size=request_dict.get("min_face_size"),
        )
