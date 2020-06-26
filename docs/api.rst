.. _api:


API
===

.. currentmodule:: api

.. autofunction:: api


Error Handler
-------------

.. currentmodule:: api.error_handler

.. autoclass:: Base_Handler
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Bad_Request_Handler
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Internal_Server_Error_Handler
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Unsupported_Media_Type_Handler
    :members:
    :private-members:
    :inherited-members:


Media Handler
-------------

.. currentmodule:: api.media_handler

.. autoclass:: XML_Handler
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: YAML_Handler
    :members:
    :private-members:
    :inherited-members:


Middleware
----------

.. currentmodule:: api.middleware

.. autoclass:: Basic_Auth_Backend_Middleware
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Negotiation_Middleware
    :members:
    :private-members:
    :inherited-members:


Spec
----

.. currentmodule:: api.spec

.. autoclass:: Spec
    :members:
    :private-members:
    :inherited-members:


Docstring
---------

.. currentmodule:: docstring

.. autodecorator:: docstring


Lib
---

.. currentmodule:: lib.http

.. autoclass:: HTTP_Method
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: HTTP_Status
    :members:
    :private-members:
    :inherited-members:

.. currentmodule:: lib.polycube

.. autoclass:: Polycube
    :members:
    :private-members:
    :inherited-members:


Response
--------

.. currentmodule:: lib.response

.. autoclass:: Base_Response
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Bad_Request_Response
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Conflict_Response
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Content_Response
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Created_Response
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Internal_Server_Error_Response
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: No_Content_Response
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Not_Acceptable_Response
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Not_Found_Response
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Not_Modified_Response
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Ok_Response
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Reset_Content_Response
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Unauthorized_Response
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Unprocessable_Entity_Response
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Unsupported_Media_Type_Response
    :members:
    :private-members:
    :inherited-members:


Reader
------

.. currentmodule:: reader.arg

.. autoclass:: Arg_Reader
    :members:
    :private-members:
    :inherited-members:

.. currentmodule:: reader.config

.. autoclass:: Config_Reader
    :members:
    :private-members:
    :inherited-members:


Resource
--------

.. currentmodule:: resource

.. autofunction:: routes

.. currentmodule:: resource.base

.. autoclass:: Base_Resource
    :members:
    :private-members:
    :inherited-members:

.. currentmodule:: resource.code

.. autoclass:: Code_Resource
    :members:
    :private-members:
    :inherited-members:

.. currentmodule:: resource.config

.. autoclass:: Config_Resource
    :members:
    :private-members:
    :inherited-members:

.. currentmodule:: resource.status

.. autoclass:: Status_Resource
    :members:
    :private-members:
    :inherited-members:

Schema
------

.. currentmodule:: schema.validate

.. autoclass:: In
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Unique_List
    :members:
    :private-members:
    :inherited-members:

.. currentmodule:: schema.base

.. autoclass:: Base_Schema
    :members:
    :private-members:
    :inherited-members:


Code
^^^^
.. currentmodule:: schema.code

.. autoclass:: Code_Request_Schema
    :members:
    :private-members:
    :inherited-members:


Config
^^^^^^

.. currentmodule:: schema.config

Request
"""""""

.. autoclass:: Config_Request_Schema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Config_Action_Request_Schema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Config_Parameter_Request_Schema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Config_Resource_Request_Schema
    :members:
    :private-members:
    :inherited-members:


Response
""""""""

.. autoclass:: Config_Action_Response_Schema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Config_Parameter_Response_Schema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Config_Parameter_Value_Response_Schema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Config_Resource_Response_Schema
    :members:
    :private-members:
    :inherited-members:


Status
^^^^^^

.. currentmodule:: schema.status

.. autoclass:: Status_Request_Schema
    :members:
    :private-members:
    :inherited-members:


.. autoclass:: Status_Response_Schema
    :members:
    :private-members:
    :inherited-members:


Response
^^^^^^^^

.. currentmodule:: schema.response

.. autoclass:: Exception_Response_Schema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Base_Response_Schema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Bad_Request_Response_Schema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Conflict_Response_Schema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Content_Response_Schema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Created_Response_Schema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: No_Content_Response_Schema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Not_Acceptable_Response_Schema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Not_Found_Response_Schema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Not_Modified_Response_Schema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Ok_Response_Schema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Reset_Content_Response_Schema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Unauthorized_Response_Schema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Unprocessable_Entity_Response_Schema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Unsupported_Media_Type_Response_Schema
    :members:
    :private-members:
    :inherited-members:


Utils
-----

Datetime
^^^^^^^^

.. currentmodule:: utils.datetime

.. autodata:: FORMAT

.. autofunction:: datetime_from_str

.. autofunction:: datetime_to_str


Exception
^^^^^^^^^

.. currentmodule:: utils.exception

.. autofunction:: extract_info

.. autofunction:: reload_import

.. autofunction:: to_str


Hash
^^^^

.. currentmodule:: utils.hash

.. autofunction:: hash

.. autofunction:: generate_username

.. autofunction:: generate_password


JSON
^^^^

.. currentmodule:: utils.json

.. autofunction:: dumps

.. autofunction:: loads


Log
^^^

.. currentmodule:: utils.log

.. autoclass:: Log
    :members:
    :private-members:
    :inherited-members:


Sequence
^^^^^^^^

.. currentmodule:: utils.sequence

.. autofunction:: expand

.. autofunction:: format

.. autofunction:: is_dict

.. autofunction:: is_list

.. autofunction:: iterate

.. autofunction:: subset

.. autofunction:: table_to_dict

.. autofunction:: wrap


Signal
^^^^^^

.. currentmodule:: utils.signal

.. autofunction:: send_tree


String
^^^^^^

.. currentmodule:: utils.string

.. autoclass:: Formatter
    :members:
    :private-members:
    :inherited-members:

.. autofunction:: is_str

.. autodata:: format


Time
^^^^

.. currentmodule:: utils.time

.. autofunction:: get_seconds
