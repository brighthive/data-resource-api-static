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
A detailed Swagger specification for this API can be found at `https://app.swaggerhub.com/apis-docs/BrightHive/data-resource-api/v1.0 <https://app.swaggerhub.com/apis-docs/BrightHive/data-resource-api/v1.0>`_.

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
Write something about API version here.