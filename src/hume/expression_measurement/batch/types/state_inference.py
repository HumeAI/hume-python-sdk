# This file was auto-generated by Fern from our API Definition.

import typing
from .state_inference_queued import StateInferenceQueued
from .state_inference_in_progress import StateInferenceInProgress
from .state_inference_completed_inference import StateInferenceCompletedInference
from .state_inference_failed import StateInferenceFailed

StateInference = typing.Union[
    StateInferenceQueued, StateInferenceInProgress, StateInferenceCompletedInference, StateInferenceFailed
]
