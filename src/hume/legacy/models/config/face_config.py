"""Configuration for the facial expression model."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from hume.legacy.models import ModelType
from hume.legacy.models.config.model_config_base import ModelConfigBase


@dataclass
class FaceConfig(ModelConfigBase):
    """Configuration for the facial expression model.

    Args:
        fps_pred (float | None): Number of frames per second to process. Other frames will be omitted
            from the response.
        prob_threshold (float | None): Face detection probability threshold. Faces detected with a
            probability less than this threshold will be omitted from the response.
        identify_faces (bool | None): Whether to return identifiers for faces across frames.
            If true, unique identifiers will be assigned to face bounding boxes to differentiate different faces.
            If false, all faces will be tagged with an "unknown" ID.
        min_face_size (float | None): Minimum bounding box side length in pixels to treat as a face.
            Faces detected with a bounding box side length in pixels less than this threshold will be
            omitted from the response.
        save_faces (bool | None): Whether to extract and save the detected faces to the artifacts
            directory included in the response.
            This configuration is only available for the batch API.
        descriptions (dict[str, Any] | None): Configuration for Descriptions predictions.
            Descriptions prediction can be enabled by setting "descriptions": {}.
            Currently, Descriptions prediction cannot be further configured with any parameters.
            If missing or null, no descriptions predictions will be generated.
        facs (dict[str, Any] | None): Configuration for FACS predictions.
            FACS prediction can be enabled by setting "facs": {}.
            Currently, FACS prediction cannot be further configured with any parameters.
            If missing or null, no facs predictions will be generated.
    """

    fps_pred: float | None = None
    prob_threshold: float | None = None
    identify_faces: bool | None = None
    min_face_size: float | None = None
    save_faces: bool | None = None
    descriptions: dict[str, Any] | None = None
    facs: dict[str, Any] | None = None

    @classmethod
    def get_model_type(cls) -> ModelType:
        """Get the configuration model type.

        Returns:
            ModelType: Model type.
        """
        return ModelType.FACE
