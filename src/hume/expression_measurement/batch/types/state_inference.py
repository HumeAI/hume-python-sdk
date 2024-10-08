# This file was auto-generated by Fern from our API Definition.

import typing
from .queued_state import QueuedState
from .in_progress_state import InProgressState
from .completed_state import CompletedState
from .failed_state import FailedState

StateInference = typing.Union[QueuedState, InProgressState, CompletedState, FailedState]
