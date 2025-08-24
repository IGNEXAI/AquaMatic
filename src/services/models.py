from typing import List, Literal, Dict
from datetime import date

from langsmith import unit
from pydantic import BaseModel, Field, computed_field, ValidationError, field_validator

# This dictionary stores specific issue messages
ISSUE_MESSAGES = {
    "out_of_range": "Value is outside the accepted range."
}


# This model represents a single water quality parameter.
class Parameter(BaseModel):
    """
    Represents a single water quality parameter and its validation status.
    """
    name: str = Field(..., description="The name of the water quality parameter (e.g., 'pH', 'Chloramine').")
    value: float = Field(..., description="The measured value for the parameter.")
    unit: str = Field(..., description="The unit of measurement for the parameter.")
    min_accepted_val: float = Field(default=None, description="The minimum accepted value for the parameter.")
    max_accepted_val: float = Field(default=None, description="The maximum accepted value for the parameter.")
    comment: str = Field(default="", description="Optional comments on the parameter's status.")
    status: Literal["OK", "OUT_OF_RANGE", "NOT_PHYSICALLY_POSSIBLE"] = Field(
        "OK", description="The validation status of the parameter."
    )
    issues: Dict[str, str] = Field(default_factory=dict, description="A dictionary of issues with corresponding messages.")
    
    @computed_field
    @property
    def is_acceptable(self) -> bool:
        """
        A boolean indicating if the measured value is within the accepted range.
        """
        is_in_range = True
        if self.min_accepted_val is not None and self.value < self.min_accepted_val:
            is_in_range = False
        if self.max_accepted_val is not None and self.value > self.max_accepted_val:
            is_in_range = False
        return is_in_range

    def __init__(self, **data):
        super().__init__(**data)
        # Manually update status and issues after initialization
        self.update_status()

    def update_status(self):
        """
        Updates the status and issues fields based on validation results.
        """
        if not self.is_acceptable:
            self.status = "OUT_OF_RANGE"
            if self.min_accepted_val and not self.max_accepted_val:
                self.issues["out_of_range"] = f"{self.name} is less than the minimum accepted value of "
                f"{self.min_accepted_val} {self.unit}."
            elif self.max_accepted_val and not self.min_accepted_val:
                self.issues["out_of_range"] = f"{self.name} is greater than the maximum accepted value of" 
                f"{self.max_accepted_val} {self.unit}."
            else:
                self.issues["out_of_range"] = f"{self.name} is not within the accpted range: "
                f"{self.max_accepted_val}-{self.min_accepted_val} {self.unit}."


# This is the main model for the entire AquaLimeLabs validation report.
class Report(BaseModel):
    """
    The main Pydantic model for the AquaLimeLabs Water Quality Validation Report.

    It structures the overall report, including the validation summary and
    detailed parameter data, making it ready to be rendered into a PDF.
    """
    report_date: date = Field(..., description="The date the report was generated.")
    parameters: List[Parameter] = Field(..., description="A list of Parameter objects detailing each water quality measurement.")
    # issues: List[str] = Field(default=[], description="A list of detailed issues for parameters that are out of range.")
    # the property above will be computed instead with the code below

    """A list of detailed issues for parameters that are out of range."""
    @computed_field
    @property
    def issues(self) -> List[str]:
        issues_ = []
        for parameter in self.parameters:
            issues_.extend(parameter.issues.values())
        return issues_

    @computed_field
    @property
    def overall_valid(self) -> bool:
        if len(self.issues) == 0:
            return True
        else:
            return False


if __name__ == "__main__":
    param2 = Parameter(name="Chloramine", unit="mg/L", value=5.0, min_accepted_val=0.5, max_accepted_val=4.0, is_valid=True)

    print(param2.status)
    print(param2.issues)
    print(param2.is_acceptable)
    