from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DIRECTORIES = [
    PROJECT_ROOT / "outputs",
    PROJECT_ROOT / "outputs" / "figures",
    PROJECT_ROOT / "outputs" / "maps",
    PROJECT_ROOT / "outputs" / "tables",
    PROJECT_ROOT / "assets",
    PROJECT_ROOT / "assets" / "screenshots",
    PROJECT_ROOT / "data",
    PROJECT_ROOT / "data" / "raw",
    PROJECT_ROOT / "data" / "interim",
    PROJECT_ROOT / "data" / "processed",
]

NOTEBOOKS = [
    "drought_risk_mapping_MENA_real_data_portfolio.ipynb",
    "archive/notebooks/drought_risk_mapping_mena_real_data.ipynb.ipynb",
    "archive/notebooks/drought_risk_mapping_MENA_portfolio_prototype.ipynb",
    "archive/notebooks/drought_risk_mapping_MENA.ipynb",
]


def create_directories() -> None:
    created = []
    for directory in DIRECTORIES:
        if not directory.exists():
            directory.mkdir(parents=True, exist_ok=True)
            created.append(directory)

    if created:
        print("Created directories:")
        for directory in created:
            print(f"  - {directory.relative_to(PROJECT_ROOT)}")
    else:
        print("All standard project directories already exist.")


def show_notebook_summary() -> None:
    print("\nNotebook inventory:")
    for notebook in NOTEBOOKS:
        notebook_path = PROJECT_ROOT / notebook
        if notebook_path.exists():
            print(f"  - {notebook}")
        else:
            print(f"  - {notebook} (missing)")

    print("\nRecommended primary notebook:")
    print("  - drought_risk_mapping_MENA_real_data_portfolio.ipynb")
    print("Archived drafts are kept under archive/notebooks/")


def main() -> None:
    print(f"Project root: {PROJECT_ROOT}")
    create_directories()
    show_notebook_summary()

    print("\nSuggested next steps:")
    print("  1. Install dependencies from requirements.txt")
    print("  2. Run scripts/environment_check.py")
    print("  3. Open the recommended notebook in Jupyter")


if __name__ == "__main__":
    main()
