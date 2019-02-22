BrightHive Data Resource API
============================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Introduction
^^^^^^^^^^^^

This document provides an overview of the BrightHive Data Resource API.
The Data Resource API enables authorized consumers to retrieve data related
to training programs, training program providers, and credentials provided by
these training programs.


API Specification
^^^^^^^^^^^^^^^^^
A detailed Swagger specification for this API can be found at `https://app.swaggerhub.com/apis-docs/BrightHive/data-resource-api/1.0.0 <https://app.swaggerhub.com/apis-docs/BrightHive/data-resource-api/1.0.0>`_.

User Auth
^^^^^^^^^^
The sandbox version of this API uses Basic Auth for restricting access. Users
are provided with an access token that gets passed with all API requests.
**Note**: This auth mechanism is only temporary and will be replaced by a
more rigorous mechanism in operational use. An example of providing the token
is shown in the code snippet below.

.. code-block:: bash

    curl -X GET https://sandbox.brighthive.net/data-resource-api/programs -H 'Authorization: Bearer 1qaz2wsx3edc'

API Versioning
^^^^^^^^^^^^^^
The versioning philosophy adopted by this API is to provide the API version
as a part of the request header. This header is optional; however, users are
cautioned that the default behavior for the API is to handle requests using the
oldest supported API version in the absence of a version header. An example of
providing the API version number is shown in the code snippent below.

.. code-block:: bash

    curl -X GET https://sandbox.brighthive.net/data-resource-api/programs -H 'Authorization: Bearer 1qaz2wsx3edc' -H 'X-Api-Version: 1.0.0'

API versioning follows the `Semantic Versioning <https://semver.org/>`_
convention.
