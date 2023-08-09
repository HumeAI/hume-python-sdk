# Example Notebooks

## About

Each example notebook showcases the use of one API with one or more models. Some examples also demonstrate additional functionality that you might care about like downloading batch results as CSVs.

## Requirements

Some notebooks have requirements beyond the Hume Python SDK. To install these run `pip install hume[examples]` before running the notebook.

## Notebooks

| API                                              | Models                                                                                                                | Extras                                                  | Link                                                                                              |
| ------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| [batch](https://dev.hume.ai/reference/start_job) | [`face`](https://dev.hume.ai/docs/facial-expression), [`facs`](https://dev.hume.ai/docs/facial-expression)            | Download results as CSV file                            | [Notebook](./batch-facial-action-coding-system/batch-facial-action-coding-system.ipynb)           |
| [batch](https://dev.hume.ai/reference/start_job) | [`language`](https://dev.hume.ai/docs/emotional-language), [`sentiment`](https://dev.hume.ai/docs/emotional-language) | Download results as JSON file                           | [Notebook](./batch-text-sentiment-analysis/batch-text-sentiment-analysis.ipynb)                   |
| [batch](https://dev.hume.ai/reference/start_job) | [`burst`](https://dev.hume.ai/docs/vocal-burst), [`prosody`](https://dev.hume.ai/docs/speech-prosody)                 | Webhook callback                                        | [Notebook](./batch-voice-expression/batch-voice-expression.ipynb)                                 |
| [batch](https://dev.hume.ai/reference/start_job) | [`language`,](https://dev.hume.ai/docs/emotional-language) [`toxicity`](https://dev.hume.ai/docs/emotional-language)  | Enable email notification                               | [Notebook](./batch-text-toxicity-detection/batch-text-toxicity-detection.ipynb)                   |
| [batch](https://dev.hume.ai/reference/start_job) | [`language`,](https://dev.hume.ai/docs/emotional-language) [`ner`](https://dev.hume.ai/docs/emotional-language)       | Submit a file from your local disk                      | [Notebook](./batch-text-entity-recognition/batch-text-entity-recognition.ipynb)                   |
| [batch](https://dev.hume.ai/reference/start_job) | [`prosody`](https://dev.hume.ai/docs/speech-prosody)                                                                  | Specified language support                              | [Notebook](./batch-specified-language-transcription/batch-specified-language-transcription.ipynb) |
| [stream](https://dev.hume.ai/docs/streaming-api) | [`facemesh`](https://dev.hume.ai/docs/facial-expression)                                                              |                                                         | [Notebook](./stream-anonymized-facemesh/stream-anonymized-facemesh.ipynb)                         |
| [stream](https://dev.hume.ai/docs/streaming-api) | [`face`](https://dev.hume.ai/docs/facial-expression)                                                                  | Face identification                                     | [Notebook](./stream-face-expression/stream-face-expression.ipynb)                                 |
| [stream](https://dev.hume.ai/docs/streaming-api) | [`language`](https://dev.hume.ai/docs/emotional-language)                                                             | Send raw text over WebSocket                            | [Notebook](./stream-text-emotion/stream-text-emotion.ipynb)                                       |
| [stream](https://dev.hume.ai/docs/streaming-api) | [`burst`](https://dev.hume.ai/docs/vocal-burst), [`prosody`](https://dev.hume.ai/docs/speech-prosody)                 | Stream media from in memory bytes, reset stream context | [Notebook](./stream-voice-expression/stream-voice-expression.ipynb)                               |
