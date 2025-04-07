# This file was auto-generated by Fern from our API Definition.

from hume import HumeClient
from hume import AsyncHumeClient
import typing
from hume.tts import PostedUtterance
from hume.tts import PostedContextWithUtterances
from hume.tts import FormatMp3
from ..utilities import validate_response


async def test_synthesize_json(client: HumeClient, async_client: AsyncHumeClient) -> None:
    expected_response: typing.Any = {
        "generations": [
            {
                "generation_id": "795c949a-1510-4a80-9646-7d0863b023ab",
                "duration": 7.44225,
                "file_size": 120192,
                "encoding": {"format": "mp3", "sample_rate": 48000},
                "audio": "//PExAA0DDYRvkpNfhv3JI5JZ...etc.",
                "snippets": [
                    [
                        {
                            "audio": "//PExAA0DDYRvkpNfhv3JI5JZ...etc.",
                            "generation_id": "795c949a-1510-4a80-9646-7d0863b023ab",
                            "id": "37b1b1b1-1b1b-1b1b-1b1b-1b1b1b1b1b1b",
                            "text": "Beauty is no quality in things themselves: It exists merely in the mind which contemplates them.",
                            "utterance_index": 0,
                        }
                    ]
                ],
            }
        ],
        "request_id": "66e01f90-4501-4aa0-bbaf-74f45dc15aa725906",
    }
    expected_types: typing.Any = {
        "generations": (
            "list",
            {
                0: {
                    "generation_id": None,
                    "duration": None,
                    "file_size": "integer",
                    "encoding": {"format": None, "sample_rate": "integer"},
                    "audio": None,
                    "snippets": (
                        "list",
                        {
                            0: (
                                "list",
                                {
                                    0: {
                                        "audio": None,
                                        "generation_id": None,
                                        "id": None,
                                        "text": None,
                                        "utterance_index": "integer",
                                    }
                                },
                            )
                        },
                    ),
                }
            },
        ),
        "request_id": None,
    }
    response = client.tts.synthesize_json(
        utterances=[
            PostedUtterance(
                text="Beauty is no quality in things themselves: It exists merely in the mind which contemplates them.",
                description="Middle-aged masculine voice with a clear, rhythmic Scots lilt, rounded vowels, and a warm,  steady tone with an articulate, academic quality.",
            )
        ],
        context=PostedContextWithUtterances(
            utterances=[
                PostedUtterance(
                    text="How can people see beauty so differently?",
                    description="A curious student with a clear and respectful tone, seeking clarification on Hume's  ideas with a straightforward question.",
                )
            ]
        ),
        format=FormatMp3(),
        num_generations=1,
    )
    validate_response(response, expected_response, expected_types)

    async_response = await async_client.tts.synthesize_json(
        utterances=[
            PostedUtterance(
                text="Beauty is no quality in things themselves: It exists merely in the mind which contemplates them.",
                description="Middle-aged masculine voice with a clear, rhythmic Scots lilt, rounded vowels, and a warm,  steady tone with an articulate, academic quality.",
            )
        ],
        context=PostedContextWithUtterances(
            utterances=[
                PostedUtterance(
                    text="How can people see beauty so differently?",
                    description="A curious student with a clear and respectful tone, seeking clarification on Hume's  ideas with a straightforward question.",
                )
            ]
        ),
        format=FormatMp3(),
        num_generations=1,
    )
    validate_response(async_response, expected_response, expected_types)
