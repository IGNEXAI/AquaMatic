from typing import List
from datetime import date

from src.services.models import Parameter, Report


# Example of a valid data set
valid_data = {
    "pH": Parameter(name="pH", unit="pH", value=7.0, min_accepted_val=6.0, max_accepted_val=8.0),
    "hardness": Parameter(name="Hardness", unit="mg/L", value=500, min_accepted_val=400, max_accepted_val=600),
    "solids": Parameter(name="Solids", unit="mg/L", value=500, min_accepted_val=400, max_accepted_val=600),
    "chloramine": Parameter(name="Chloramine", unit="mg/L", value=5.0, min_accepted_val=0.5, max_accepted_val=4.0),
    "sulfate": Parameter(name="Sulfate", unit="mg/L", value=200, min_accepted_val=100, max_accepted_val=300),
    "conductivity": Parameter(name="Conductivity", unit="uS/cm", value=555, min_accepted_val=400, max_accepted_val=600),
    "turbidity": Parameter(name="Turbidity", unit="NTU", value=2.0, min_accepted_val=1.0, max_accepted_val=3.0)
}

# Example of an invalid data set
invalid_data = {
    "pH": 9.2,
    "hardness": 650,
    "solids": 600,
    "chloramine": 5.1,
    "sulfate": 200,
    "conductivity": 555,
    "turbidity": 2.0
}


def create_water_quality_report(data: List[Parameter]) -> Report:
    """
    Validates water quality data and generates a detailed report of issues.

    Args:
        data: A dictionary containing the water quality parameters.

    Returns:
        A dictionary containing the validation result and a detailed report.
    """
    report = Report(
        report_date=date.today(),
        parameters=data
    )

    return report

# Let's test it

if __name__ == "__main__":
    params = []
    for value in valid_data.values():
        params.append(value)
    new_report = create_water_quality_report(params)
    print(new_report.issues)
