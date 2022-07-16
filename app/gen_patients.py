from dataclasses import dataclass, field
from datetime import datetime

from flask import redirect, url_for


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
    report_url

    """
    report_url: str
    fname: str = field(repr=False, default="John")
    lname: str = field(repr=False, default="Doe")
    admission_date: datetime = field(default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), repr=False)
    name: str = field(init=False, repr=True)
    id: str = field(init=False, repr=True)

    def __post_init__(self):
        self.name = f"{self.lname+', ' if self.lname else ''}{self.fname}"
        self.id = f"{self.admission_date}{self.name[0]}{self.name[-1]}".replace('-', '').replace(':', '').replace(' ', '').lower()
    
    def __repr__(self) -> str:
        return '{'+f'"name": "{self.name}", "admission_date": "{self.admission_date}", "id": "{self.id}", "report_url": "{self.report_url}"'+'}'


def get_patients():
    Jim = example()
    return [Jim]


def example():
    Jimmy = Patient(
        "patient_1.csv",
        "John",
        "Doe",
        '2022-01-12 13:56:12'
    )
    print(Jimmy.name)
    return Jimmy


def read_data():
    model_path = r"model\best_model\dataset2.sav"


    for _pid in (1, 2, 3, 4, 5):
        print(get_prediction(rf"app\static\patients\patient_{_pid}.csv", model_path, True))


if __name__ == "__main__":
    jim = example()
    print(jim)
    print(jim.admission_date)
