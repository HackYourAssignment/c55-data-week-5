"""Tests for the Week 5 pipeline."""

import pytest

from src.pipeline import fetch_data, get_config, save_results


class TestGetConfig:
    """Tests for get_config()."""
    def test_returns_api_key_from_env(self, monkeypatch):
        """Test that get_config() reads API_KEY from the environment."""
        monkeypatch.setenv("API_KEY", "test-key-123")
        monkeypatch.delenv("OUTPUT_DIR", raising=False)
        config = get_config()
        assert config["api_key"] == "test-key-123"

    def test_uses_default_output_dir(self, monkeypatch):
        """Test that get_config() uses 'output' as the default output directory."""
        monkeypatch.setenv("API_KEY", "test-key-123")
        monkeypatch.delenv("OUTPUT_DIR", raising=False)
        config = get_config()
        assert config["output_dir"] == "output"

    def test_reads_custom_output_dir(self, monkeypatch):
        """Test that get_config() reads OUTPUT_DIR from the environment."""
        monkeypatch.setenv("API_KEY", "test-key-123")
        monkeypatch.setenv("OUTPUT_DIR", "/tmp/myout")
        config = get_config()
        assert config["output_dir"] == "/tmp/myout"

    def test_raises_when_api_key_missing(self, monkeypatch):
        """Test that get_config() raises RuntimeError when API_KEY is missing."""
        monkeypatch.delenv("API_KEY", raising=False)
        with pytest.raises((RuntimeError, KeyError, SystemExit)):
            get_config()


class TestFetchData:
    """Tests for fetch_data()."""
    def test_returns_list(self):
        """Test that fetch_data() returns a list."""
        records = fetch_data("any-key")
        assert isinstance(records, list)

    def test_returns_at_least_one_record(self):
        """Test that fetch_data() returns at least one record."""
        records = fetch_data("any-key")
        assert len(records) >= 1

    def test_records_are_dicts(self):
        """Test that each record returned by fetch_data() is a dict."""
        records = fetch_data("any-key")
        assert all(isinstance(r, dict) for r in records)


class TestSaveResults:
    """Tests for save_results()."""
    def test_creates_output_dir(self, tmp_path):
        """Test that save_results() creates the output directory if it doesn't exist."""
        output_dir = tmp_path / "new_dir"
        save_results([{"id": 1}], output_dir)
        assert output_dir.exists()

    def test_writes_results_file(self, tmp_path):
        """Test that save_results() writes results.txt in the output directory."""
        save_results([{"id": 1}, {"id": 2}], tmp_path)
        results_file = tmp_path / "results.txt"
        assert results_file.exists()

   def test_file_contains_records(self, tmp_path):
    """Test that save_results() writes the expected record count."""
        save_results([{"id": 1}, {"id": 2}], tmp_path)
        content = (tmp_path / "results.txt").read_text()
        assert len(content.strip().splitlines()) >= 2
