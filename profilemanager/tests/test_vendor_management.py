from rest_framework.test import APIClient
from rest_framework import status

class TestVendorManagement:
    def test_if_api_requires_token_returns_401(self):
        # Arrange
        # Act
        client = APIClient()
        response = client.get('/profilemanager/vendors')
        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    
