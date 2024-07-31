# This file was auto-generated by Fern from our API Definition.

import typing

from .state_tl_inference_completed_tl_inference import StateTlInferenceCompletedTlInference
from .state_tl_inference_failed import StateTlInferenceFailed
from .state_tl_inference_in_progress import StateTlInferenceInProgress
from .state_tl_inference_queued import StateTlInferenceQueued

StateTlInference = typing.Union[
    StateTlInferenceQueued, StateTlInferenceInProgress, StateTlInferenceCompletedTlInference, StateTlInferenceFailed
]
