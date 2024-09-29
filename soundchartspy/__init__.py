from importlib.metadata import version, PackageNotFoundError

from dotenv import load_dotenv

load_dotenv()

try:
    __version__ = version("soundchartspy")
except PackageNotFoundError:
    __version__ = "unknown"
