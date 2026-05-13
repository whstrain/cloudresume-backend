import pytest
from unittest.mock import MagicMock, patch
import json
import os
import sys

class TestGetVisitorCount:
    
    def setup_method(self):
        """Reset module imports before each test"""
        if 'function_app' in sys.modules:
            del sys.modules['function_app']
        os.environ["COSMOS_CONNECTION_STRING"] = "DefaultEndpointsProtocol=https;AccountName=test;AccountKey=dGVzdA==;TableEndpoint=https://test.table.cosmos.azure.com:443/;"

    def test_returns_json_with_count(self):
        """Test that the function returns a JSON response with a count key"""
        with patch('azure.data.tables.TableServiceClient') as mock_table_service:
            mock_table = MagicMock()
            mock_table_service.from_connection_string.return_value.get_table_client.return_value = mock_table
            mock_table.get_entity.return_value = {"counter": 5}

            import azure.functions as func
            req = func.HttpRequest(
                method='GET',
                url='/api/GetVisitorCount',
                body=b'',
                params={}
            )

            from function_app import GetVisitorCount
            response = GetVisitorCount(req)

            data = json.loads(response.get_body())
            assert "count" in data
            assert isinstance(data["count"], int)

    def test_count_increments(self):
        """Test that the count is incremented by 1"""
        with patch('azure.data.tables.TableServiceClient') as mock_table_service:
            mock_table = MagicMock()
            mock_table_service.from_connection_string.return_value.get_table_client.return_value = mock_table
            mock_table.get_entity.return_value = {"counter": 10}

            import azure.functions as func
            req = func.HttpRequest(
                method='GET',
                url='/api/GetVisitorCount',
                body=b'',
                params={}
            )

            from function_app import GetVisitorCount
            response = GetVisitorCount(req)

            data = json.loads(response.get_body())
            assert data["count"] == 11