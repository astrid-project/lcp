.. _authentication:

Authentication
==============

The authentication is done using |JWT|.

You can create a |JWT| token following the instruction at: https://jwt.io.

In particular, the required fields for the |JSON| payload for the token creation are:

- ``iat`` - issued at, in epoch time.
- ``exp`` - expirated at, in epoch time.
- ``nbf`` - valid not before, in epoch time.

The secret key is the one defined in the :ref:`configuration`.

To convert the human readable datetime you can use https://www.epochconverter.com.


.. |JSON| replace:: :abbr:`JSON (JavaScript Object Notation)`
.. |JWT| replace:: :abbr:`JWT (JSON Web Token)`
