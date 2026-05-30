from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path


@dataclass(frozen=True)
class ProjectConfig:
    start_date: str = "2018-01-01"
    end_date: str = "2024-12-31"
    bbox: tuple[float, float, float, float] = (-17.0, 12.0, 65.0, 42.0)
    grid_dx: float = 1.0
    grid_dy: float = 1.0
    reduce_scale: int = 5000

    ndvi_dataset_id: str = "MODIS/061/MOD13A3"
    rainfall_dataset_id: str = "UCSB-CHG/CHIRPS/DAILY"
    lst_dataset_id: str = "MODIS/061/MOD11A2"

    @property
    def extraction_end_date(self) -> str:
        end_date = datetime.strptime(self.end_date, "%Y-%m-%d").date()
        return (end_date + timedelta(days=1)).isoformat()

    @property
    def project_root(self) -> Path:
        return Path(__file__).resolve().parents[2]

    @property
    def outputs_dir(self) -> Path:
        return self.project_root / "outputs"

    @property
    def figures_dir(self) -> Path:
        return self.outputs_dir / "figures"

    @property
    def maps_dir(self) -> Path:
        return self.outputs_dir / "maps"

    @property
    def tables_dir(self) -> Path:
        return self.outputs_dir / "tables"

    @property
    def class_names(self) -> dict[int, str]:
        return {
            0: "Normal / Wet",
            1: "Mild Drought",
            2: "Moderate Drought",
            3: "Severe Drought",
        }
