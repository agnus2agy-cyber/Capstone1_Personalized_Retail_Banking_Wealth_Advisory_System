from pathlib import Path
from ingestion.ingestion import ingest_pdf
import shutil


def copy_pdf_to_data(source_file: str) -> Path:
    try:
        source_path = Path(source_file)

        if not source_path.exists():
            raise FileNotFoundError(f"File does not exist: {source_path}")

        if not source_path.is_file():
            raise ValueError(f"Path is not a file: {source_path}")

        if source_path.suffix.lower() != ".pdf":
            raise ValueError(f"Expected a PDF file. Found: {source_path.suffix}")

        data_folder = Path("data")
        data_folder.mkdir(parents=True, exist_ok=True)

        destination_path = data_folder / source_path.name

        if destination_path.exists():
            print(
                f"ℹ️ File already exists: {destination_path}. Proceed with processing"
            )
            return destination_path

        shutil.copy2(source_path, destination_path)

        print(f"✅ PDF copied successfully: {destination_path}")

        return destination_path

    except FileNotFoundError as e:
        print(f"❌ File not found: {e}")
        raise

    except PermissionError as e:
        print(f"❌ Permission denied: {e}")
        raise

    except ValueError as e:
        print(f"❌ Validation error: {e}")
        raise

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        raise


ingest_file = copy_pdf_to_data(
    """C://Capstone_Project_2_Personalized_Retail_Banking_FAQ.pdf"""
)

print("Destination path")
print(ingest_file)
# call the ingestion.py to load the pdf into D

ingest_pdf(ingest_file)
