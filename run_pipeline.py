"""Master CLI Entrypoint for SwiftLog Logistics Analytics & AI Transformation Solution."""
import sys
from src.pipeline import SwiftLogMasterPipeline


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    pipeline = SwiftLogMasterPipeline()
    results = pipeline.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
