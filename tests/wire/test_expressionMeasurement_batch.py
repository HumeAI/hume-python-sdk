from .conftest import get_client, verify_request_count


def test_expressionMeasurement_batch_list_jobs() -> None:
    """Test list-jobs endpoint with WireMock"""
    test_id = "expression_measurement.batch.list_jobs.0"
    client = get_client(test_id)
    client.expression_measurement.batch.list_jobs()
    verify_request_count(test_id, "GET", "/v0/batch/jobs", None, 1)


def test_expressionMeasurement_batch_start_inference_job() -> None:
    """Test start-inference-job endpoint with WireMock"""
    test_id = "expression_measurement.batch.start_inference_job.0"
    client = get_client(test_id)
    client.expression_measurement.batch.start_inference_job(
        urls=["https://hume-tutorials.s3.amazonaws.com/faces.zip"], notify=True
    )
    verify_request_count(test_id, "POST", "/v0/batch/jobs", None, 1)


def test_expressionMeasurement_batch_get_job_details() -> None:
    """Test get-job-details endpoint with WireMock"""
    test_id = "expression_measurement.batch.get_job_details.0"
    client = get_client(test_id)
    client.expression_measurement.batch.get_job_details(id="job_id")
    verify_request_count(test_id, "GET", "/v0/batch/jobs/job_id", None, 1)


def test_expressionMeasurement_batch_get_job_predictions() -> None:
    """Test get-job-predictions endpoint with WireMock"""
    test_id = "expression_measurement.batch.get_job_predictions.0"
    client = get_client(test_id)
    client.expression_measurement.batch.get_job_predictions(id="job_id")
    verify_request_count(test_id, "GET", "/v0/batch/jobs/job_id/predictions", None, 1)


def test_expressionMeasurement_batch_start_inference_job_from_local_file() -> None:
    """Test start-inference-job-from-local-file endpoint with WireMock"""
    test_id = "expression_measurement.batch.start_inference_job_from_local_file.0"
    client = get_client(test_id)
    client.expression_measurement.batch.start_inference_job()
    verify_request_count(test_id, "POST", "/v0/batch/jobs", None, 1)
