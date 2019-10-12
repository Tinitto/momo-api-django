"""
This module holds the utility to query any API endpoint
It is ported by Martin Ahindura from the mtn-pay-js TypeScript package
https://github.com/sopherapps/mtn-pay-js/blob/master/src/utils/repository.ts
"""

import requests


def get_resources(resource_names,
                  api_base_url='http://localhost:8080/api',
                  common_headers={}):
    """
    Generates a list of RemoteResource objects
    corresponding to the resource_names passed
    """
    return {resource_name: RemoteResource(
        resource_name, api_base_url=api_base_url,
        common_headers=common_headers) for resource_name in resource_names}


class RemoteResource:
    """A class that has utilities for accessing a remote resource"""

    def __init__(self, resource, api_base_url, common_headers={}, timeout=1):
        self._base_url = "{api_base_url}/{resource}".format(
            api_base_url=api_base_url, resource=resource)
        self._common_headers = common_headers
        self._timeout = timeout

    def __get_url_for_resource_id(self, resource_id):
        return "{base_url}/{resource_id}".format(
            base_url=self._base_url, resource_id=resource_id)

    def create(self, payload, headers={}):
        """Creates a new instance of the remote resource remotely via API POST call"""
        return requests.post(
            self._base_url, data=payload, headers={**self._common_headers, **headers}, timeout=self._timeout)

    def destroy(self, resource_id, headers={}):
        """Deletes an instance of a resource with id resource_id"""
        url = self.__get_url_for_resource_id(resource_id)
        return requests.delete(url, headers={**self._common_headers, **headers}, timeout=self._timeout)

    def get_one(self, resource_id, headers={}):
        """Retrieves a single instance of a given resource with id resource_id"""
        url = self.__get_url_for_resource_id(resource_id)
        return requests.get(url, headers={**self._common_headers, **headers}, timeout=self._timeout)

    def list_many(self, params={}, headers={}):
        """
        Returns a list of instances of a given resource fulfilling the
        filters passed in the params
        """
        return requests.get(
            self._base_url, params=params, headers={**self._common_headers, **headers}, timeout=self._timeout)

    def update(self, resource_id, payload, headers={}):
        """
        Updates the instance of the resource of id resource_id
        with the data in payload
        """
        url = self.__get_url_for_resource_id(resource_id)
        return requests.put(
            url, data=payload, headers={**self._common_headers, **headers}, timeout=self._timeout)
