from pathlib import Path

import pandas as pd

from .config import ProjectConfig


def ensure_project_directories(config: ProjectConfig) -> None:
    for directory in [
        config.outputs_dir,
        config.figures_dir,
        config.maps_dir,
        config.tables_dir,
        config.project_root / "assets" / "screenshots",
        config.project_root / "data" / "raw",
        config.project_root / "data" / "interim",
        config.project_root / "data" / "processed",
    ]:
        directory.mkdir(parents=True, exist_ok=True)


def month_starts(start_date: str, end_date: str) -> list[str]:
    dates = pd.date_range(start=start_date, end=end_date, freq="MS")
    return [pd.Timestamp(date).strftime("%Y-%m-%d") for date in dates]


def project_path(*parts: str | Path) -> Path:
    return ProjectConfig().project_root.joinpath(*parts)
