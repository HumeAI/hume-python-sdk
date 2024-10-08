from pathlib import Path
from unittest.mock import MagicMock

import pytest
from pytest import MonkeyPatch, TempPathFactory

from hume.legacy import BatchJob, HumeBatchClient
from hume.legacy.models.config import BurstConfig, FaceConfig, LanguageConfig, ProsodyConfig


@pytest.fixture(name="batch_client", scope="function")
def batch_client_fixture(monkeypatch: MonkeyPatch) -> HumeBatchClient:
    mock_submit_request = MagicMock(return_value="temp-job-value")
    monkeypatch.setattr(HumeBatchClient, "_submit_job", mock_submit_request)
    client = HumeBatchClient("0000-0000-0000-0000", timeout=15)
    mock_submit_request.return_value = BatchJob(client, "mock-job-id")
    return client


@pytest.mark.batch
class TestHumeBatchClient:

    def test_face(self, batch_client: HumeBatchClient) -> None:
        mock_url = "mock-url"
        config = FaceConfig(fps_pred=5, prob_threshold=0.24, identify_faces=True, min_face_size=78)
        job = batch_client.submit_job([mock_url], [config])
        assert isinstance(job, BatchJob)
        assert job.id == "mock-job-id"
        batch_client._submit_job.assert_called_once_with(  # type: ignore
            {
                "models": {
                    "face": {
                        "fps_pred": 5,
                        "prob_threshold": 0.24,
                        "identify_faces": True,
                        "min_face_size": 78,
                    },
                },
                "urls": [mock_url],
            },
            None,
            None,
        )

    def test_burst(self, batch_client: HumeBatchClient) -> None:
        mock_url = "mock-url"
        config = BurstConfig()
        job = batch_client.submit_job([mock_url], [config])
        assert isinstance(job, BatchJob)
        assert job.id == "mock-job-id"
        batch_client._submit_job.assert_called_once_with(  # type: ignore
            {
                "models": {
                    "burst": {},
                },
                "urls": [mock_url],
            },
            None,
            None,
        )

    def test_prosody(self, batch_client: HumeBatchClient) -> None:
        mock_url = "mock-url"
        config = ProsodyConfig(identify_speakers=True)
        job = batch_client.submit_job([mock_url], [config])
        assert isinstance(job, BatchJob)
        assert job.id == "mock-job-id"
        batch_client._submit_job.assert_called_once_with(  # type: ignore
            {
                "models": {
                    "prosody": {
                        "identify_speakers": True,
                    },
                },
                "urls": [mock_url],
            },
            None,
            None,
        )

    def test_language(self, batch_client: HumeBatchClient) -> None:
        mock_url = "mock-url"
        config = LanguageConfig(granularity="word", identify_speakers=True)
        job = batch_client.submit_job([mock_url], [config])
        assert isinstance(job, BatchJob)
        assert job.id == "mock-job-id"
        batch_client._submit_job.assert_called_once_with(  # type: ignore
            {
                "models": {
                    "language": {
                        "granularity": "word",
                        "identify_speakers": True,
                    },
                },
                "urls": [mock_url],
            },
            None,
            None,
        )

    def test_language_with_raw_text(self, batch_client: HumeBatchClient) -> None:
        mock_text = "Test!"
        config = LanguageConfig(granularity="word", identify_speakers=True)
        job = batch_client.submit_job([], [config], text=[mock_text])
        assert isinstance(job, BatchJob)
        assert job.id == "mock-job-id"
        batch_client._submit_job.assert_called_once_with(  # type: ignore
            {
                "urls": [],
                "models": {
                    "language": {
                        "granularity": "word",
                        "identify_speakers": True,
                    },
                },
                "text": [mock_text],
            },
            None,
            None,
        )

    def test_get_job(self, batch_client: HumeBatchClient) -> None:
        job = batch_client.get_job("mock-job-id")
        assert job.id == "mock-job-id"

    def test_files(self, batch_client: HumeBatchClient) -> None:
        mock_filepath = "my-audio.mp3"
        config = ProsodyConfig(identify_speakers=True)
        job = batch_client.submit_job([], [config], files=[mock_filepath])
        assert isinstance(job, BatchJob)
        assert job.id == "mock-job-id"
        batch_client._submit_job.assert_called_once_with(  # type: ignore
            {
                "urls": [],
                "models": {
                    "prosody": {
                        "identify_speakers": True,
                    },
                },
            },
            ["my-audio.mp3"],
            None,
        )

    def test_get_multipart_form_data(self, batch_client: HumeBatchClient, tmp_path_factory: TempPathFactory) -> None:
        dirpath = tmp_path_factory.mktemp("multipart")
        filepath = dirpath / "my-audio.mp3"
        with filepath.open("w") as f:
            f.write("I can't believe this test passed!")

        request_body = {"mock": "body"}
        filepaths: list[Path] = [filepath]
        filebytes: list[tuple[str, bytes]] = []
        result = batch_client._get_multipart_form_data(request_body, filepaths, filebytes)

        assert result == [
            ("file", ("my-audio.mp3", b"I can't believe this test passed!")),
            ("json", b'{"mock": "body"}'),
        ]
