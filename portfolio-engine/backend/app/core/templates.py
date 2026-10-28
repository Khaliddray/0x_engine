from pathlib import Path
from fastapi.templating import Jinja2Templates

TEMPLATES_DIR = (
    Path(__file__).resolve().parent.parent.parent.parent
    / "frontend"
    / "templates"
)

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


def _smart_url_for(request, name: str, **kwargs) -> str:
    # Support Flask-style filename parameter in Starlette's url_for
    if "filename" in kwargs and "path" not in kwargs:
        kwargs["path"] = kwargs.pop("filename")
    return str(request.url_for(name, **kwargs))


# Expose smart_url_for on template environment globals
templates.env.globals["smart_url_for"] = _smart_url_for
