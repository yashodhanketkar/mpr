from dataclasses import dataclass, field
from datetime import datetime

try:
    from .lib import get_prediction
except ImportError:
    print("Error occured during import")
    from lib import get_prediction


@dataclass
class Patient:
    """Patients Dataclass

    This class stores the patients data in instance object.

    Attributes:
    report_url (str): Name of the ECG report file.
    fname (str): First name of the patient
    lname (str): Last name of the patient
    admission_date (datetime): Admission time of patient
    name (str): Full name generated from fname and lname
    id (str): ID generated from name and admission date
    """

    report_url: str
    fname: str = field(repr=False, default="John")
    lname: str = field(repr=False, default="Doe")
    admission_date: datetime = field(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), repr=False)
    name: str = field(init=False, repr=True)
    id: str = field(init=False, repr=True)

    def __post_init__(self):
        self.name = f"{self.lname+', ' if self.lname else ''}{self.fname}"
        self.id = (
            f"{self.admission_date}{self.name[0]}{self.name[-1]}".replace("-", "")
            .replace(":", "")
            .replace(" ", "")
            .lower()
        )

    def __repr__(self) -> str:
        return (
            "{"
            + f'"name": "{self.name}", "admission_date": "{self.admission_date}", "id": "{self.id}", "report_url": "{self.report_url}"'
            + "}"
        )


def example():
    """Example for get patients"""
    Jimmy = Patient("patient_1.csv", "John", "Doe", "2022-01-12 13:56:12")
    print(Jimmy.name)
    return Jimmy


if __name__ == "__main__":
    jim = example()
    print(jim)
