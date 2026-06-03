"""Tests for pipeline helper functions (cleaning, transforming, validating)."""

import os

import pandas as pd
import pytest

from src.clean import clean_sales
from src.pipeline import get_config
from src.transform import join_customers
from src.pipeline import fetch_data, get_config, save_results


class TestGetConfig:
    def test_returns_api_key_from_env(self, monkeypatch):
        monkeypatch.setenv("API_KEY", "test-key-123")
        monkeypatch.delenv("OUTPUT_DIR", raising=False)
        config = get_config()
        assert config["api_key"] == "test-key-123"

    def test_uses_default_output_dir(self, monkeypatch):
        monkeypatch.setenv("API_KEY", "test-key-123")
        monkeypatch.delenv("OUTPUT_DIR", raising=False)
        config = get_config()
        assert config["output_dir"] == "output"

    def test_reads_custom_output_dir(self, monkeypatch):
        monkeypatch.setenv("API_KEY", "test-key-123")
        monkeypatch.setenv("OUTPUT_DIR", "/tmp/myout")
        config = get_config()
        assert config["output_dir"] == "/tmp/myout"

    def test_raises_when_api_key_missing(self, monkeypatch):
        monkeypatch.delenv("API_KEY", raising=False)
        with pytest.raises((RuntimeError, KeyError, SystemExit)):
            get_config()


class TestFetchData:
    def test_returns_list(self):
        records = fetch_data("any-key")
        assert isinstance(records, list)

    def test_returns_at_least_one_record(self):
        records = fetch_data("any-key")
        assert len(records) >= 1

    def test_records_are_dicts(self):
        records = fetch_data("any-key")
        assert all(isinstance(r, dict) for r in records)


class TestSaveResults:
    def test_creates_output_dir(self, tmp_path):
        output_dir = tmp_path / "new_dir"
        save_results([{"id": 1}], output_dir)
        assert output_dir.exists()

    def test_writes_results_file(self, tmp_path):
        save_results([{"id": 1}, {"id": 2}], tmp_path)
        results_file = tmp_path / "results.txt"
        assert results_file.exists()

    def test_file_contains_records(self, tmp_path):
        save_results([{"id": 1}, {"id": 2}], tmp_path)
        content = (tmp_path / "results.txt").read_text()
        assert len(content.strip().splitlines()) >= 2


def test_clean_sales_normalizes_product_name():
    sales = pd.DataFrame(
        {
            "transaction_id": [1],
            "product_name": ["  widget  "],
            "customer_email": ["A@X.COM"],
            "price": [10.0],
            "quantity": [1],
            "date": ["2024-01-01"],
        }
    )
    result = clean_sales(sales)
    assert result.iloc[0]["product_name"] == "Widget"


def test_join_customers_adds_high_value_flag():
    sales = pd.DataFrame(
        {
            "customer_email": ["a@b.com"],
            "price": [100.0],
            "quantity": [2],
        }
    )
    customers = pd.DataFrame(
        {
            "customer_email": ["a@b.com"],
            "customer_name": ["Alice"],
            "region": ["EU"],
            "loyalty_tier": ["gold"],
            "category": ["tech"],
        }
    )
    result = join_customers(sales, customers)
    assert bool(result.iloc[0]["is_high_value"])
    assert result.iloc[0]["line_revenue"] == 200.0


def test_get_config_raises_when_api_key_missing():
    os.environ["GITHUB_USERNAME"] = "test-user"
    os.environ.pop("API_KEY", None)
    with pytest.raises(RuntimeError, match="API_KEY"):
        get_config()
