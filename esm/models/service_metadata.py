# coding: utf-8

from __future__ import absolute_import
#
from .base_model_ import Model
from datetime import date, datetime
from typing import List, Dict
from ..util import deserialize_model


class ServiceMetadata(Model):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, display_name: str=None, image_url: str=None, long_description: str=None, provider_display_name: str=None, documentation_url: str=None, support_url: str=None, extras: object=None):
        """
        ServiceMetadata - a model defined in Swagger

        :param display_name: The display_name of this ServiceMetadata.
        :type display_name: str
        :param image_url: The image_url of this ServiceMetadata.
        :type image_url: str
        :param long_description: The long_description of this ServiceMetadata.
        :type long_description: str
        :param provider_display_name: The provider_display_name of this ServiceMetadata.
        :type provider_display_name: str
        :param documentation_url: The documentation_url of this ServiceMetadata.
        :type documentation_url: str
        :param support_url: The support_url of this ServiceMetadata.
        :type support_url: str
        :param extras: The extras of this ServiceMetadata.
        :type extras: object
        """
        self.swagger_types = {
            'display_name': str,
            'image_url': str,
            'long_description': str,
            'provider_display_name': str,
            'documentation_url': str,
            'support_url': str,
            'extras': object
        }

        self.attribute_map = {
            'display_name': 'displayName',
            'image_url': 'imageUrl',
            'long_description': 'longDescription',
            'provider_display_name': 'providerDisplayName',
            'documentation_url': 'documentationUrl',
            'support_url': 'supportUrl',
            'extras': 'extras'
        }

        self._display_name = display_name
        self._image_url = image_url
        self._long_description = long_description
        self._provider_display_name = provider_display_name
        self._documentation_url = documentation_url
        self._support_url = support_url
        self._extras = extras

    @classmethod
    def from_dict(cls, dikt) -> 'ServiceMetadata':
        """
        Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The ServiceMetadata of this ServiceMetadata.
        :rtype: ServiceMetadata
        """
        return deserialize_model(dikt, cls)

    @property
    def display_name(self) -> str:
        """
        Gets the display_name of this ServiceMetadata.
        The name of the service to be displayed in graphical clients.

        :return: The display_name of this ServiceMetadata.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name: str):
        """
        Sets the display_name of this ServiceMetadata.
        The name of the service to be displayed in graphical clients.

        :param display_name: The display_name of this ServiceMetadata.
        :type display_name: str
        """

        self._display_name = display_name

    @property
    def image_url(self) -> str:
        """
        Gets the image_url of this ServiceMetadata.
        The URL to an image.

        :return: The image_url of this ServiceMetadata.
        :rtype: str
        """
        return self._image_url

    @image_url.setter
    def image_url(self, image_url: str):
        """
        Sets the image_url of this ServiceMetadata.
        The URL to an image.

        :param image_url: The image_url of this ServiceMetadata.
        :type image_url: str
        """

        self._image_url = image_url

    @property
    def long_description(self) -> str:
        """
        Gets the long_description of this ServiceMetadata.
        Long description

        :return: The long_description of this ServiceMetadata.
        :rtype: str
        """
        return self._long_description

    @long_description.setter
    def long_description(self, long_description: str):
        """
        Sets the long_description of this ServiceMetadata.
        Long description

        :param long_description: The long_description of this ServiceMetadata.
        :type long_description: str
        """

        self._long_description = long_description

    @property
    def provider_display_name(self) -> str:
        """
        Gets the provider_display_name of this ServiceMetadata.
        The name of the upstream entity providing the actual service.

        :return: The provider_display_name of this ServiceMetadata.
        :rtype: str
        """
        return self._provider_display_name

    @provider_display_name.setter
    def provider_display_name(self, provider_display_name: str):
        """
        Sets the provider_display_name of this ServiceMetadata.
        The name of the upstream entity providing the actual service.

        :param provider_display_name: The provider_display_name of this ServiceMetadata.
        :type provider_display_name: str
        """

        self._provider_display_name = provider_display_name

    @property
    def documentation_url(self) -> str:
        """
        Gets the documentation_url of this ServiceMetadata.
        Link to documentation page for service.

        :return: The documentation_url of this ServiceMetadata.
        :rtype: str
        """
        return self._documentation_url

    @documentation_url.setter
    def documentation_url(self, documentation_url: str):
        """
        Sets the documentation_url of this ServiceMetadata.
        Link to documentation page for service.

        :param documentation_url: The documentation_url of this ServiceMetadata.
        :type documentation_url: str
        """

        self._documentation_url = documentation_url

    @property
    def support_url(self) -> str:
        """
        Gets the support_url of this ServiceMetadata.
        Link to support for the service.

        :return: The support_url of this ServiceMetadata.
        :rtype: str
        """
        return self._support_url

    @support_url.setter
    def support_url(self, support_url: str):
        """
        Sets the support_url of this ServiceMetadata.
        Link to support for the service.

        :param support_url: The support_url of this ServiceMetadata.
        :type support_url: str
        """

        self._support_url = support_url

    @property
    def extras(self) -> object:
        """
        Gets the extras of this ServiceMetadata.
        additional attributes

        :return: The extras of this ServiceMetadata.
        :rtype: object
        """
        return self._extras

    @extras.setter
    def extras(self, extras: object):
        """
        Sets the extras of this ServiceMetadata.
        additional attributes

        :param extras: The extras of this ServiceMetadata.
        :type extras: object
        """

        self._extras = extras
