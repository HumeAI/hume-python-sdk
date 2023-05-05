# Example Notebooks

## About

Each example notebook showcases the use of one API with one or more models. Some examples also demonstrate additional functionality that you might care about like downloading batch results as CSVs.

## Requirements

Some notebooks have requirements beyond the Hume Python SDK. To install these run `pip install hume[examples]` before running the notebook.

## Notebooks

| API                                              | Models                 | Extras                          | Link                                                                                          |
| ------------------------------------------------ | ---------------------- | ------------------------------- | --------------------------------------------------------------------------------------------- |
| [batch](https://docs.hume.ai/doc/batch-api)      | `face`, `facs`         | Download results as CSV file    | [Notebook](./batch-facial-action-coding-system/batch-facial-action-coding-system.ipynb)       |
| [batch](https://docs.hume.ai/doc/batch-api)      | `language`             | Download results as JSON file   | [Notebook](./batch-text-sentiment-analysis/batch-text-sentiment-analysis.ipynb)               |
| [batch](https://docs.hume.ai/doc/batch-api)      | `burst`, `prosody`     |                                 | [Notebook](./batch-voice-expression/batch-voice-expression.ipynb)                             |
| [batch](https://docs.hume.ai/doc/batch-api)      | `language`, `toxicity` |                                 | [Notebook](./batch-text-toxicity-detection/batch-text-toxicity-detection.ipynb)               |
| [batch](https://docs.hume.ai/doc/batch-api)      | `language`, `ner`      |                                 | [Notebook](./batch-text-entity-recognition/batch-text-entity-recognition.ipynb)               |
| [batch](https://docs.hume.ai/doc/batch-api)      | `prosody`              | Foreign language support        | [Notebook](./batch-foreign-language-transcription/batch-foreign-language-transcription.ipynb) |
| [stream](https://docs.hume.ai/doc/streaming-api) | `facemesh`             |                                 | [Notebook](./stream-anonymized-facemesh/stream-anonymized-facemesh.ipynb)                     |
| [stream](https://docs.hume.ai/doc/streaming-api) | `face`                 | Face identification             | [Notebook](./stream-face-expression/stream-face-expression.ipynb)                             |
| [stream](https://docs.hume.ai/doc/streaming-api) | `language`             | Sending raw text over websocket | [Notebook](./stream-text-emotion/stream-text-emotion.ipynb)                                   |
| [stream](https://docs.hume.ai/doc/streaming-api) | `burst`, `prosody`     | Reset audio context             | [Notebook](./stream-voice-expression/stream-voice-expression.ipynb)                           |
