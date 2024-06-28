# This file was auto-generated by Fern from our API Definition.

import typing

from .state_training_completed_training import StateTrainingCompletedTraining
from .state_training_failed import StateTrainingFailed
from .state_training_in_progress import StateTrainingInProgress
from .state_training_queued import StateTrainingQueued

StateTraining = typing.Union[
    StateTrainingQueued, StateTrainingInProgress, StateTrainingCompletedTraining, StateTrainingFailed
]