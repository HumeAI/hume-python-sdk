"""Configuration for the facial expression model."""
from dataclasses import dataclass
from typing import Any, Dict, Optional

from hume.models import ModelType
from hume.models.config.model_config_base import ModelConfigBase


@dataclass
class FaceConfig(ModelConfigBase["FaceConfig"]):
    """Configuration for the facial expression model.

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
        save_faces (Optional[bool]): Whether to extract and save the detected faces to the artifacts
            directory included in the response.
            This configuration is only available for the batch API.
        descriptions (Optional[Dict[str, Any]]): Configuration for Descriptions predictions.
            Descriptions prediction can be enabled by setting "descriptions": {}.
            Currently, Descriptions prediction cannot be further configured with any parameters.
            If missing or null, no descriptions predictions will be generated.
        facs (Optional[Dict[str, Any]]): Configuration for FACS predictions.
            FACS prediction can be enabled by setting "facs": {}.
            Currently, FACS prediction cannot be further configured with any parameters.
            If missing or null, no facs predictions will be generated.
    """

    fps_pred: Optional[float] = None
    prob_threshold: Optional[float] = None
    identify_faces: Optional[bool] = None
    min_face_size: Optional[float] = None
    save_faces: Optional[bool] = None
    descriptions: Optional[Dict[str, Any]] = None
    facs: Optional[Dict[str, Any]] = None

    @classmethod
    def get_model_type(cls) -> ModelType:
        """Get the configuration model type.

        Returns:
            ModelType: Model type.
        """
        return ModelType.FACE
