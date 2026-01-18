from pydantic import RootModel
from typing import Dict

class FileSummaries(RootModel[Dict[str, str]]):
    pass
