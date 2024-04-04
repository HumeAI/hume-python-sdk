import json
import logging
import re
import zipfile
from dataclasses import fields
from datetime import datetime
from pathlib import Path
from typing import Optional, Type, Union
from urllib.request import urlretrieve

import pytest
from pytest import TempPathFactory

from hume import BatchJob, BatchJobDetails, HumeBatchClient, HumeClientException, TranscriptionConfig
from hume.models.config import BurstConfig, FaceConfig, FacemeshConfig, LanguageConfig, NerConfig, ProsodyConfig
from hume.models.config.model_config_base import ModelConfigBase
from utilities.eval_data import EvalData

logger = logging.getLogger(__name__)


@pytest.fixture(name="batch_client", scope="module")
def batch_client_fixture(hume_api_key: str) -> HumeBatchClient:
    return HumeBatchClient(hume_api_key)


@pytest.mark.batch
@pytest.mark.service
class TestServiceHumeBatchClient:

    def test_face(self, eval_data: EvalData, batch_client: HumeBatchClient, tmp_path_factory: TempPathFactory) -> None:
        data_url = eval_data["image-obama-face"]
        config = FaceConfig(
            fps_pred=5,
            prob_threshold=0.24,
            identify_faces=True,
            min_face_size=78,
            facs={},
            descriptions={},
            save_faces=False,
        )
        job_files_dirpath = tmp_path_factory.mktemp("job-files")
        job = batch_client.submit_job([data_url], [config])
        self.check_job(job, config, FaceConfig, job_files_dirpath)

    def test_burst(self, eval_data: EvalData, batch_client: HumeBatchClient, tmp_path_factory: TempPathFactory) -> None:
        data_url = eval_data["burst-amusement-009"]
        config = BurstConfig()
        job_files_dirpath = tmp_path_factory.mktemp("job-files")
        job = batch_client.submit_job([data_url], [config])
        self.check_job(job, config, BurstConfig, job_files_dirpath)

    def test_prosody(
        self, eval_data: EvalData, batch_client: HumeBatchClient, tmp_path_factory: TempPathFactory
    ) -> None:
        data_url = eval_data["prosody-horror-1051"]
        config = ProsodyConfig(
            identify_speakers=True,
            granularity="word",
            window={"length": 4.0, "step": 1.0},
        )
        job_files_dirpath = tmp_path_factory.mktemp("job-files")
        job = batch_client.submit_job([data_url], [config])
        self.check_job(job, config, ProsodyConfig, job_files_dirpath)

    def test_language(
        self, eval_data: EvalData, batch_client: HumeBatchClient, tmp_path_factory: TempPathFactory
    ) -> None:
        data_url = eval_data["text-happy-place"]
        config = LanguageConfig(
            granularity="word",
            identify_speakers=True,
            sentiment={},
            toxicity={},
        )
        job_files_dirpath = tmp_path_factory.mktemp("job-files")
        job = batch_client.submit_job([data_url], [config])
        self.check_job(job, config, LanguageConfig, job_files_dirpath)

    def test_ner(self, eval_data: EvalData, batch_client: HumeBatchClient, tmp_path_factory: TempPathFactory) -> None:
        data_url = eval_data["text-obama-news"]
        config = NerConfig(identify_speakers=True)
        job_files_dirpath = tmp_path_factory.mktemp("job-files")
        job = batch_client.submit_job([data_url], [config])
        self.check_job(job, config, NerConfig, job_files_dirpath)

    def test_facemesh(
        self, eval_data: EvalData, batch_client: HumeBatchClient, tmp_path_factory: TempPathFactory
    ) -> None:
        data_url = eval_data["three-faces-mediapipe"]
        config = FacemeshConfig()
        job_files_dirpath = tmp_path_factory.mktemp("job-files")
        job = batch_client.submit_job([data_url], [config])
        self.check_job(job, config, FacemeshConfig, job_files_dirpath)

    def test_transcription(
        self, eval_data: EvalData, batch_client: HumeBatchClient, tmp_path_factory: TempPathFactory
    ) -> None:
        data_url = eval_data["prosody-noticias"]
        config = LanguageConfig()
        transcription_config = TranscriptionConfig(language="es")
        self.check_complete_config(transcription_config, TranscriptionConfig)
        job = batch_client.submit_job([data_url], [config], transcription_config=transcription_config)
        assert isinstance(job, BatchJob)
        assert len(job.id) == 36
        logger.info(f"Running test job {job.id}")
        details = job.await_complete()
        job_files_dirpath = tmp_path_factory.mktemp("job-files")
        self.check_details(job, details, job_files_dirpath)

    def test_client_invalid_api_key(self, eval_data: EvalData) -> None:
        invalid_client = HumeBatchClient("invalid-api-key")
        data_url = eval_data["image-obama-face"]
        message = "HumeBatchClient initialized with invalid API key."
        with pytest.raises(HumeClientException, match=re.escape(message)):
            invalid_client.submit_job([data_url], [FaceConfig()])

    def test_job_invalid_api_key(self, eval_data: EvalData, batch_client: HumeBatchClient) -> None:
        data_url = eval_data["image-obama-face"]
        job = batch_client.submit_job([data_url], [FaceConfig()])
        invalid_client = HumeBatchClient("invalid-api-key")
        message = "HumeBatchClient initialized with invalid API key."
        with pytest.raises(HumeClientException, match=re.escape(message)):
            rehydrated_job = BatchJob(invalid_client, job.id)
            rehydrated_job.await_complete(10)

    def test_local_file_upload_simple(
        self, eval_data: EvalData, batch_client: HumeBatchClient, tmp_path_factory: TempPathFactory
    ) -> None:
        data_url = eval_data["image-obama-face"]
        data_filepath = tmp_path_factory.mktemp("data-dir") / "obama.png"
        urlretrieve(data_url, data_filepath)
        config = FaceConfig()
        job_files_dirpath = tmp_path_factory.mktemp("job-files")
        job = batch_client.submit_job([], [config], files=[data_filepath])
        self.check_job(job, config, FaceConfig, job_files_dirpath, complete_config=False)

        predictions = job.get_predictions()
        assert predictions[0]["source"]["filename"] == "obama.png"

    def test_data_as_raw_text(self, batch_client: HumeBatchClient, tmp_path_factory: TempPathFactory) -> None:
        data_raw_text = "Test!"
        config = LanguageConfig()
        job_files_dirpath = tmp_path_factory.mktemp("job-files")
        job = batch_client.submit_job([], [config], text=[data_raw_text])
        self.check_job(job, config, LanguageConfig, job_files_dirpath, complete_config=False)

        predictions = job.get_predictions()
        language_predictions = predictions[0]["results"]["predictions"][0]["models"]["language"]
        assert predictions[0]["source"]["type"] == "text"
        assert language_predictions["grouped_predictions"][0]["predictions"][0]["text"] == "Test!"

    def test_local_file_upload_configure(
        self, eval_data: EvalData, batch_client: HumeBatchClient, tmp_path_factory: TempPathFactory
    ) -> None:
        data_url = eval_data["text-happy-place"]
        data_filepath = tmp_path_factory.mktemp("data-dir") / "happy.txt"
        urlretrieve(data_url, data_filepath)
        config = LanguageConfig(granularity="sentence")
        job_files_dirpath = tmp_path_factory.mktemp("job-files")
        job = batch_client.submit_job([], [config], files=[data_filepath])
        self.check_job(job, config, LanguageConfig, job_files_dirpath, complete_config=False)

        predictions = job.get_predictions()

        assert len(predictions) == 1
        assert predictions[0]["results"]
        assert len(predictions[0]["results"]["predictions"]) == 1
        language_results = predictions[0]["results"]["predictions"][0]["models"]["language"]
        grouped_predictions = language_results["grouped_predictions"]
        assert len(grouped_predictions) == 1

        # Configuring 'sentence' granularity should give us only one prediction
        # rather than the nine we'd get if we used 'word' granularity.
        assert len(grouped_predictions[0]["predictions"]) == 1

    # test for the case where a file is passed as a byte string
    def test_file_upload_bytes_configure(
        self, eval_data: EvalData, batch_client: HumeBatchClient, tmp_path_factory: TempPathFactory
    ) -> None:
        data_url = eval_data["text-happy-place"]
        data_filepath = tmp_path_factory.mktemp("data-dir") / "happy.txt"
        urlretrieve(data_url, data_filepath)
        with data_filepath.open("rb") as f:
            data_bytes = f.read()
        config = LanguageConfig(granularity="sentence")
        job_files_dirpath = tmp_path_factory.mktemp("job-files")
        job = batch_client.submit_job([], [config], filebytes=[("happy.txt", data_bytes)])
        self.check_job(job, config, LanguageConfig, job_files_dirpath, complete_config=False)

        predictions = job.get_predictions()

        assert len(predictions) == 1
        assert predictions[0]["results"]
        assert len(predictions[0]["results"]["predictions"]) == 1
        assert predictions[0]["source"]["type"] == "file"
        assert predictions[0]["source"]["filename"] == "happy.txt"
        language_results = predictions[0]["results"]["predictions"][0]["models"]["language"]
        grouped_predictions = language_results["grouped_predictions"]
        assert len(grouped_predictions) == 1

        # Configuring 'sentence' granularity should give us only one prediction
        # rather than the nine we'd get if we used 'word' granularity.
        assert len(grouped_predictions[0]["predictions"]) == 1

    def check_job(
        self,
        job: BatchJob,
        config: Union[ModelConfigBase, TranscriptionConfig],
        config_class: Type[Union[ModelConfigBase, TranscriptionConfig]],
        job_files_dirpath: Path,
        complete_config: bool = True,
    ) -> None:
        if complete_config:
            self.check_complete_config(config, config_class)
        assert isinstance(job, BatchJob)
        assert len(job.id) == 36
        logger.info(f"Running test job {job.id}")
        details = job.await_complete()
        self.check_details(job, details, job_files_dirpath)

    def check_details(self, job: BatchJob, details: BatchJobDetails, job_files_dirpath: Path) -> None:
        assert isinstance(details.get_created_time(), datetime)
        assert isinstance(details.get_started_time(), datetime)
        assert isinstance(details.get_ended_time(), datetime)
        assert isinstance(details.get_run_time_ms(), int)

        predictions_filepath = job_files_dirpath / "predictions.json"
        job.download_predictions(predictions_filepath)
        logger.info(f"Predictions for job {job.id} downloaded to {predictions_filepath}")
        with predictions_filepath.open() as f:
            predictions = json.load(f)
            assert len(predictions) == 1
            assert "results" in predictions[0]

        artifacts_zip_filepath = job_files_dirpath / "artifacts.zip"
        job.download_artifacts(artifacts_zip_filepath)
        logger.info(f"Artifacts for job {job.id} downloaded to {artifacts_zip_filepath}")

        extracted_artifacts_dir = job_files_dirpath / "extract"
        extracted_artifacts_dir.mkdir(exist_ok=True)
        with zipfile.ZipFile(artifacts_zip_filepath, "r") as zip_ref:
            zip_ref.extractall(extracted_artifacts_dir)
        logger.info(f"Artifacts for job {job.id} extracted to {extracted_artifacts_dir}")
        assert len(list(extracted_artifacts_dir.iterdir())) == 1

    def check_complete_config(
        self,
        config: Union[ModelConfigBase, TranscriptionConfig],
        config_class: Type[Union[ModelConfigBase, TranscriptionConfig]],
        exceptions: Optional[list[str]] = None,
    ) -> None:
        exceptions_set = set(exceptions) if exceptions is not None else set()
        class_fields = set([field.name for field in fields(config_class)]) - exceptions_set
        instance_fields = set(config.to_dict().keys()) - exceptions_set
        assert len(instance_fields) == len(class_fields), "Model configuration must have all values set"
