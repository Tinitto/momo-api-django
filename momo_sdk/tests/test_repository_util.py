"""
Tests for the respository utilities
These have been ported by Martin Ahindura from the mtn-pay-js Typescript package
https://github.com/sopherapps/mtn-pay-js/blob/master/src/__tests__/utils/repository.spec.ts
"""
from unittest import TestCase
from unittest.mock import patch
import requests
from momo_sdk.utils.repository import get_resources, RemoteResource


class TestRemoteResource(TestCase):
    """
    Tests for the RemoteResource class
    used to connect to remote resources via API calls
    """

    def setUp(self):
        """Do initial set up"""
        self.api_base_url = 'http://localhost'
        self.common_headers = {"Authorization": 'Bearer some-token'}
        self.specific_headers = {'X-security': 'helmet'}
        self.mock_resource_name = 'books'
        self.timeout = 0.01
        self.remote_resource = RemoteResource(
            self.mock_resource_name, api_base_url=self.api_base_url,
            common_headers=self.common_headers, timeout=self.timeout)
        self.resource_url = "{0}/{1}".format(self.api_base_url,
                                             self.mock_resource_name)

    @patch('momo_sdk.utils.repository.requests.get')
    def test_list_many_method(self, mock_get):
        """
        The list_many method returns the response from requests.get method with
        with the appropriate arguments
        """
        params = {'hello': 'world'}

        response = self.remote_resource.list_many(
            params=params, headers=self.specific_headers)

        self.assertEqual(response, mock_get.return_value)

        mock_get.assert_called_once_with(
            self.resource_url, params=params, headers={
                **self.common_headers, **self.specific_headers}, timeout=self.timeout)

    @patch('momo_sdk.utils.repository.requests.get')
    def test_get_one_method(self, mock_get):
        """
        The get_one method returns the response from the requests.get method call
        with appropriate arguments
        """
        resource_id = 20
        response = self.remote_resource.get_one(
            resource_id, headers=self.specific_headers)
        url = "{0}/{1}".format(self.resource_url, resource_id)

        self.assertEqual(response, mock_get.return_value)

        mock_get.assert_called_once_with(
            url, headers={**self.common_headers, **self.specific_headers},
            timeout=self.timeout)

    @patch('momo_sdk.utils.repository.requests.put')
    def test_update_method(self, mock_put):
        """
        The update method returns the response from the requests.put method call
        with appropriate arguments
        """
        resource_id = 20
        payload = {'1': 'hello'}
        response = self.remote_resource.update(
            resource_id, payload, headers=self.specific_headers)
        url = "{0}/{1}".format(self.resource_url, resource_id)

        self.assertEqual(response, mock_put.return_value)

        mock_put.assert_called_once_with(
            url, data=payload, headers={
                **self.common_headers, **self.specific_headers},
            timeout=self.timeout)

    @patch('momo_sdk.utils.repository.requests.delete')
    def test_destroy_method(self, mock_delete):
        """
        The destroy method returns the response from the requests.delete method call
        with appropriate arguments
        """
        resource_id = 20
        response = self.remote_resource.destroy(
            resource_id, headers=self.specific_headers)
        url = "{0}/{1}".format(self.resource_url, resource_id)

        self.assertEqual(response, mock_delete.return_value)

        mock_delete.assert_called_once_with(
            url, headers={**self.common_headers, **self.specific_headers},
            timeout=self.timeout)

    @patch('momo_sdk.utils.repository.requests.post')
    def test_create_method(self, mock_post):
        """
        The create method returns the response from the requests.post method call
        with appropriate arguments
        """
        payload = {'1': 'hello'}
        response = self.remote_resource.create(
            payload=payload, headers=self.specific_headers)

        self.assertEqual(response, mock_post.return_value)

        mock_post.assert_called_once_with(
            self.resource_url, data=payload, headers={
                **self.common_headers, **self.specific_headers},
            timeout=self.timeout)


class TestGetResources(TestCase):
    """Tests for the get_resources utility function"""

    def setUp(self):
        """Initialize some variables"""
        self.resource_names = ['books', 'tables', 'pens']
        self.api_base_url = 'http://localhost'
        self.common_headers = {"Authorization": 'Bearer some-token'}
        self.specific_headers = {'X-security': 'helmet'}

    def test_get_resources(self):
        """
        Returns a dictionary of RemoteResource objects with
        the keys being the names of these resources
        """
        resources = get_resources(
            self.resource_names, api_base_url=self.api_base_url,
            common_headers=self.common_headers)

        for name in resources:
            remote_resource = resources[name]
            self.assertEqual(remote_resource._base_url,
                             "{0}/{1}".format(self.api_base_url, name))
