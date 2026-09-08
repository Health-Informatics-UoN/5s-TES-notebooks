import json
import secrets
import shlex
import string
from urllib.error import HTTPError
import logging

import ipywidgets as widgets
from five_safes_tes_workbench.workbench import Workbench
from IPython.display import display
from ipywidgets.widgets.widget_box import VBox

class WorkbenchForm:
    def __init__(
            self,
            layout: widgets.Layout = widgets.Layout(width = "50%")
            ) -> None:
        self._username: widgets.Text = widgets.Text(
            value="Who are you?",
            placeholder="Who are you?",
            description="User name:",
            disabled=False,
            layout=layout,
        )

        self._password: widgets.Password = widgets.Password(
            value="password",
            placeholder="Enter password",
            description="Password:",
            disabled=False,
            layout=layout,
        )

        # self.output = widgets.Output()
        # self.check_conn_button = widgets.Button(description="Check your connection")
        # self.check_conn_button.on_click(self.check_connection)

    def display(self):
        display(VBox([self._username, self._password]))

    def validate(self) -> Workbench:
        wb = Workbench()

        logger = logging.getLogger()
        logger.setLevel(logging.CRITICAL)

        wb.validate(
            project="OHDSIDemo",
            tres=["Nottingham TRE 01", "Nottingham TRE 02"],
            tes_base_url="https://api.5s-tes.federated-research.com/",
            keycloak_url="https://drs-core-identity.azurewebsites.net/",
            client_id="Dare-Control-S3",
            client_secret="tBqx2MQnMI9oEG1QDKNpq3EKkPZMs7M6",
            username=self._username.value,
            password=self._password.value,
        )

        logger.setLevel(logging.INFO)

        return wb

    def check_connection(self, known_task: int = 1856):
        wb = self.validate()

        try:
            wb.fetch_outputs(task_id=known_task)
            print("\n\n\n----------------------------")
            print("You're connecting just fine!")
        except HTTPError:
            print("Bad connection 😱")


class IncidencePrevalenceForm:
    def __init__(
            self,
            layout: widgets.Layout = widgets.Layout(width = "50%")
            ) -> None:
        self._concept_sets: widgets.Textarea = widgets.Textarea(
            value='{"diabetes": [4131907,4220821]}', description="Concept sets", layout=layout
        )
        self._outcome_cohort_name: widgets.Text = widgets.Text(
            value="diabetes_cohort", description="Outcome cohort name", layout=layout
        )
        self._denominator_cohort_name: widgets.Text = widgets.Text(
            value="diabetes_denominator", description="Denominator cohort name", layout=layout
        )
        self._researcher_name: widgets.Text = widgets.Text(
            value="John Snow", description="Researcher name", layout=layout
        )

    @property
    def researcher_name(self) -> str:
        return self._researcher_name.value

    def display(self):
        display(
            VBox(
                [
                    self._researcher_name,
                    self._outcome_cohort_name,
                    self._concept_sets,
                    self._denominator_cohort_name,
                ]
            )
        )

    def checked_concept_sets(self) -> str:
        try:
            concept_dict = {str(k): [int(x) for x in v] for k,v in json.loads(self._concept_sets.value).items()}
            return json.dumps(concept_dict)
        except ValueError:
            raise ValueError("Invalid concept set!")

    @staticmethod
    def random_table_ids(id_length: int):
        alphabet = string.ascii_lowercase + string.digits
        return "".join(secrets.choice(alphabet) for _ in range(id_length))

    def render_executor(self):
        random_id = self.random_table_ids(8)
        outcome_cohort_name = f"{self._outcome_cohort_name.value}{random_id}"
        denominator_cohort_name = f"{self._denominator_cohort_name.value}{random_id}"
        full_script = (
            f"Rscript inst/scripts/defineConceptCohortSet.R {shlex.quote(outcome_cohort_name)} "
            f"--conceptSet={shlex.quote(self.checked_concept_sets())} && "
            f"Rscript inst/scripts/incidencePrevalence.R {shlex.quote(denominator_cohort_name)} "
            f"--outcomeCohortName={shlex.quote(outcome_cohort_name)} "
            "--denominatorCohortDateRange=1990-01-01,2030-01-01 "
            f"--estimateIncidenceOutputPath=outputs/incidence.csv && "
            f"Rscript inst/scripts/cleanUpCohortTables.R {shlex.quote(outcome_cohort_name)} && "
            f"Rscript inst/scripts/cleanUpCohortTables.R {shlex.quote(denominator_cohort_name)}"
        )

        return [
            {
                "image": "ghcr.io/health-informatics-uon/omop-r-tools:sha-9aa526d",
                "command": ["/bin/sh", "-c", full_script],
            }
        ]
