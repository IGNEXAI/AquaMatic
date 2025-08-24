from datetime import date
import pytest
from pydantic import ValidationError
from src.services.create_report import create_water_quality_report
from src.services.models import Parameter, Report


def test_validate_water_quality_with_valid_data():
    """
    Tests that the function returns a valid report when given valid data.
    """
    data = [
        Parameter(name="pH", value=7.2, unit="pH"),
        Parameter(name="Chloramine", value=0.8, unit="mg/L"),
    ]
    report = create_water_quality_report(data)
    assert isinstance(report, Report)
    assert report.overall_valid is True
    assert report.report_date == date.today()
    assert len(report.parameters) == 2


def test_validate_water_quality_with_invalid_data():
    """
    Tests that the function raises a validation error when given invalid data.
    """
    with pytest.raises(ValidationError):
        create_water_quality_report([{"name": "pH", "value": "invalid", "unit": "pH"}])


def test_validate_water_quality_with_out_of_range_data():
    """
    Tests that the function correctly identifies out-of-range data.
    """
    data = [
        Parameter(
            name="pH",
            value=8.6,
            unit="pH",
            min_accepted_val=6.5,
            max_accepted_val=8.5,
        ),
        Parameter(
            name="Chloramine",
            value=0.8,
            unit="mg/L",
            min_accepted_val=0.5,
            max_accepted_val=4.0,
        ),
    ]
    report = create_water_quality_report(data)
    # The current implementation of validate_water_quality does not check for out of range values.
    # This test will fail until the logic is updated.
    assert report.overall_valid is False
    assert report.parameters[0].is_acceptable is False
    assert report.parameters[1].is_acceptable is True
