import pytest
import sys
import os

# Ensure src is in path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from validator import FileValidator

@pytest.fixture
def validator():
    return FileValidator()

def test_valid_filename(validator):
    name = "1001_LAB_20231025.pdf"
    is_valid, _, error = validator.normalize(name)
    assert is_valid is True
    assert error is None

def test_invalid_filename_format(validator):
    name = "bad_file_name.pdf"
    is_valid, _, error = validator.normalize(name)
    assert is_valid is False
    assert "Does not match" in error

def test_invalid_extension(validator):
    name = "1001_LAB_20231025.exe"
    is_valid, _, error = validator.normalize(name)
    assert is_valid is False
    assert "Extension .exe not allowed" in error

def test_metadata_extraction(validator):
    name = "999_XR_20240101.jpg"
    meta = validator.get_metadata(name)
    assert meta['id'] == "999"
    assert meta['type'] == "XR"
    assert meta['date'] == "20240101"
