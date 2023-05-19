import pycodestyle
import os

ROOT_FOLDER = os.path.dirname(os.path.dirname(__file__))

paths = [
    os.path.join(ROOT_FOLDER, 'app')
]


def test_conformance(paths=paths):
    """Test that pyIncore conforms to PEP-8."""
    style = pycodestyle.StyleGuide(quiet=False, max_line_length=120)
    result = style.check_files(paths)
    assert result.total_errors == 0

test_conformance()
