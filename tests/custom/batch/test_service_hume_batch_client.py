import json
import logging
import zipfile
from datetime import datetime
from pathlib import Path
from urllib.request import urlretrieve

import pytest
from pytest import TempPathFactory

from hume.client import HumeClient
from hume.core.api_error import ApiError
from hume.expression_measurement.batch.legacy.batch_job import BatchJob
from hume.expression_measurement.types.face import Face
from hume.expression_measurement.types.language import Language
from hume.expression_measurement.types.models import Models
from hume.expression_measurement.types.ner import Ner
from hume.expression_measurement.types.prosody import Prosody
from hume.expression_measurement.types.transcription import Transcription
from hume.expression_measurement.types.union_job import UnionJob
from utilities.eval_data import EvalData

logger = logging.getLogger(__name__)


@pytest.mark.batch
@pytest.mark.service
class TestServiceHumeBatchClient:

    def test_face(
        self,
        eval_data: EvalData,
        hume_client: HumeClient,
        tmp_path_factory: TempPathFactory,
    ) -> None:
        data_url = eval_data["image-obama-face"]
        config = Models(
            face=Face(
                fps_pred=5,
                prob_threshold=0.24,
                identify_faces=True,
                min_face_size=78,
                facs={},
                descriptions={},
                save_faces=False,
            )
        )
        job_files_dirpath = tmp_path_factory.mktemp("job-files")
        job = hume_client.expression_measurement.batch_legacy.submit_job(
            [data_url], config
        )

        self.check_job(job, job_files_dirpath)

    def test_burst(
        self,
        eval_data: EvalData,
        hume_client: HumeClient,
        tmp_path_factory: TempPathFactory,
    ) -> None:
        data_url = eval_data["burst-amusement-009"]
        config = Models(burst={})
        job_files_dirpath = tmp_path_factory.mktemp("job-files")
        job = hume_client.expression_measurement.batch_legacy.submit_job(
            [data_url], config
        )

        self.check_job(job, job_files_dirpath)

    def test_prosody(
        self,
        eval_data: EvalData,
        hume_client: HumeClient,
        tmp_path_factory: TempPathFactory,
    ) -> None:
        data_url = eval_data["prosody-horror-1051"]
        config = Models(
            prosody=Prosody(
                identify_speakers=True,
                granularity="word",
                window={"length": 4.0, "step": 1.0},
            )
        )
        job_files_dirpath = tmp_path_factory.mktemp("job-files")
        job = hume_client.expression_measurement.batch_legacy.submit_job(
            [data_url], config
        )
        self.check_job(job, job_files_dirpath)

    def test_language(
        self,
        eval_data: EvalData,
        hume_client: HumeClient,
        tmp_path_factory: TempPathFactory,
    ) -> None:
        data_url = eval_data["text-happy-place"]
        config = Models(
            language=Language(
                granularity="word",
                identify_speakers=True,
                sentiment={},
                toxicity={},
            )
        )
        job_files_dirpath = tmp_path_factory.mktemp("job-files")
        job = hume_client.expression_measurement.batch_legacy.submit_job(
            [data_url], config
        )
        self.check_job(job, job_files_dirpath)

    def test_ner(
        self,
        eval_data: EvalData,
        hume_client: HumeClient,
        tmp_path_factory: TempPathFactory,
    ) -> None:
        data_url = eval_data["text-obama-news"]
        config = Models(ner=Ner(identify_speakers=True))
        job_files_dirpath = tmp_path_factory.mktemp("job-files")
        job = hume_client.expression_measurement.batch_legacy.submit_job(
            [data_url], config
        )
        self.check_job(job, job_files_dirpath)

    def test_facemesh(
        self,
        eval_data: EvalData,
        hume_client: HumeClient,
        tmp_path_factory: TempPathFactory,
    ) -> None:
        data_url = eval_data["three-faces-mediapipe"]
        config = Models(facemesh={})
        job_files_dirpath = tmp_path_factory.mktemp("job-files")
        job = hume_client.expression_measurement.batch_legacy.submit_job(
            [data_url], config
        )
        self.check_job(job, job_files_dirpath)

    def test_transcription(
        self,
        eval_data: EvalData,
        hume_client: HumeClient,
        tmp_path_factory: TempPathFactory,
    ) -> None:
        data_url = eval_data["prosody-noticias"]
        config = Models(language=Language())
        transcription_config = Transcription(language="es")
        job = hume_client.expression_measurement.batch_legacy.submit_job(
            [data_url], config, transcription_config=transcription_config
        )
        assert isinstance(job, BatchJob)
        assert len(job.id) == 36
        logger.info(f"Running test job {job.id}")
        details = job.await_complete()
        job_files_dirpath = tmp_path_factory.mktemp("job-files")
        self.check_details(job, details, job_files_dirpath)

    def test_client_invalid_api_key(self, eval_data: EvalData) -> None:
        invalid_client = HumeClient(api_key="invalid-api-key")
        data_url = eval_data["image-obama-face"]
        with pytest.raises(ApiError):
            invalid_client.expression_measurement.batch_legacy.submit_job(
                [data_url], Models(face=Face())
            )

    def test_local_file_upload_simple(
        self,
        eval_data: EvalData,
        hume_client: HumeClient,
        tmp_path_factory: TempPathFactory,
    ) -> None:
        data_url = eval_data["image-obama-face"]
        data_filepath = tmp_path_factory.mktemp("data-dir") / "obama.png"
        urlretrieve(data_url, data_filepath)
        config = Models(face=Face())
        job_files_dirpath = tmp_path_factory.mktemp("job-files")
        job = hume_client.expression_measurement.batch_legacy.submit_job(
            [], config, files=[data_filepath]
        )
        self.check_job(job, job_files_dirpath)

        predictions = job.get_predictions()
        assert predictions[0].source.filename == "obama.png"

    def test_data_as_raw_text(
        self, hume_client: HumeClient, tmp_path_factory: TempPathFactory
    ) -> None:
        data_raw_text = "Test!"
        config = Models(language=Language())
        job_files_dirpath = tmp_path_factory.mktemp("job-files")
        job = hume_client.expression_measurement.batch_legacy.submit_job(
            [], config, text=[data_raw_text]
        )
        self.check_job(job, job_files_dirpath)

        predictions = job.get_predictions()
        language_predictions = predictions[0].results.predictions[0].models.language
        assert predictions[0].source.type == "text"
        assert (
            language_predictions.grouped_predictions[0].predictions[0].text
            == "Test!"
        )

    def test_local_file_upload_configure(
        self,
        eval_data: EvalData,
        hume_client: HumeClient,
        tmp_path_factory: TempPathFactory,
    ) -> None:
        data_url = eval_data["text-happy-place"]
        data_filepath = tmp_path_factory.mktemp("data-dir") / "happy.txt"
        urlretrieve(data_url, data_filepath)
        config = Models(language=Language(granularity="sentence"))
        job_files_dirpath = tmp_path_factory.mktemp("job-files")
        job = hume_client.expression_measurement.batch_legacy.submit_job(
            [], config, files=[data_filepath]
        )
        self.check_job(job, job_files_dirpath)

        predictions = job.get_predictions()

        assert len(predictions) == 1
        assert predictions[0].results
        assert len(predictions[0].results.predictions) == 1
        language_results = predictions[0].results.predictions[0].models.language
        grouped_predictions = language_results.grouped_predictions
        assert len(grouped_predictions) == 1

        # Configuring 'sentence' granularity should give us only one prediction
        # rather than the nine we'd get if we used 'word' granularity.
        assert len(grouped_predictions[0].predictions) == 1

    def check_job(
        self,
        job: BatchJob,
        job_files_dirpath: Path,
    ) -> None:
        assert isinstance(job, BatchJob)
        assert len(job.id) == 36
        logger.info(f"Running test job {job.id}")
        details = job.await_complete()
        self.check_details(job, details, job_files_dirpath)

    def check_details(
        self, job: BatchJob, details: UnionJob, job_files_dirpath: Path
    ) -> None:
        assert isinstance(details.state.created_timestamp_ms, int)
        assert isinstance(details.state.started_timestamp_ms, int)
        assert isinstance(details.state.ended_timestamp_ms, int)

        predictions_filepath = job_files_dirpath / "predictions.json"
        job.download_predictions(predictions_filepath)
        logger.info(
            f"Predictions for job {job.id} downloaded to {predictions_filepath}"
        )
        with predictions_filepath.open() as f:
            predictions = json.load(f)
            assert len(predictions) == 1
            assert "results" in predictions[0]

        artifacts_zip_filepath = job_files_dirpath / "artifacts.zip"
        job.download_artifacts(artifacts_zip_filepath)
        logger.info(
            f"Artifacts for job {job.id} downloaded to {artifacts_zip_filepath}"
        )

        extracted_artifacts_dir = job_files_dirpath / "extract"
        extracted_artifacts_dir.mkdir(exist_ok=True)
        with zipfile.ZipFile(artifacts_zip_filepath, "r") as zip_ref:
            zip_ref.extractall(extracted_artifacts_dir)
        logger.info(
            f"Artifacts for job {job.id} extracted to {extracted_artifacts_dir}"
        )
        assert len(list(extracted_artifacts_dir.iterdir())) == 1
