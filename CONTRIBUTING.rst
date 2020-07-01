Contributing
============

lcp is open-source and very open to contributions.

If you're part of a corporation with an |NDA|, and you may require updating the LICENSE.
See Updating Copyright below.

Submitting issues
-----------------

Issues are contributions in a way so don't hesitate to submit reports on the `official bugtracker`_.

Provide as much informations as possible to specify the issues:

- the lcp version used,
- a stacktrace,
- installed applications list,
- a code sample to reproduce the issue,
- etc.


Submitting patches (bugfix, features, ...)
------------------------------------------

Follow these steps, if you want to contribute some code:

1. Fork the `official lcp repository`_.
2. Ensure an issue is opened for your feature or bug.
3. Create a branch with an explicit name (like ``my-new-feature`` or ``issue-XX``).
4. Do your work in it
5. Commit your changes. Ensure the commit message includes the issue.
   Also, if contributing from a corporation, be sure to add a comment with the Copyright information.
6. Rebase it on the master branch from the official repository (clean-up your history by performing an interactive rebase).
7. Add your change to the changelog.
8. Submit your pull-request.
9. 2 Maintainers should review the code for bugfix and features. 1 maintainer for minor changes (such as docs)
10. After review, a maintainer a will merge the PR. Maintainers should not merge their own PRs

There are some rules to follow:

- your contribution should be documented (if needed),
- your contribution should be tested and the test suite should pass successfully,
- your code should be mostly PEP8 compatible with a 120 characters line length,
- your contribution should support both Python 3 (use ``tox`` to test).

You need to install some dependencies to develop on lcp:

.. code-block:: console

    $ pip install -r requirements.txt

An Invoke ``tasks.py`` is provided to simplify the common tasks:

.. code-block:: console

    $ inv -l
    Available tasks:

    all         Run conversions, tests, reports and packaging
    benchmark   Run benchmarks
    clean       Clean-up all build artifacts
    cover       Run tests suite with coverage
    deps        Install or update development dependencies
    docs        Build the documentation
    pypi        Build package for pypi
    qa          Run a quality report
    rst2html    Convert restructuredText file to HTML using Pandoc
    rst2htmls   Convert rst files: AUTHORS, CHANGELOG, CONTRIBUTING, README to HTML
    rst2md      Convert restructuredText file to Markdown using Pandoc
    rst2pdf     Convert restructuredText file to PDF using Pandoc
    tests       Run tests suite
    tox         Run tests against Python versions

To ensure everything is fine before submission, use ``tox``.
It will run the test suite on all the supported Python version
and ensure the documentation is generating.

.. code-block:: console

    $ tox

You also need to ensure your code is compliant with the lcp coding standards:

.. code-block:: console

    $ inv qa

To ensure everything is fine before committing, you can launch the all in one command:

.. code-block:: console

    $ inv qa tox

It will ensure the code meet the coding conventions, runs on every version on python
and the documentation is properly generating.

.. _official lcp repository: https://github.com/astrid-project/lcp
.. _official bugtracker: https://github.com/astrid-project/lcp/issues


Code Style
----------

Naming convention rules:

- name *variables* and *methods*: **lower snake case** (example: ``extract_info``).
- name *classes*: **title snake case** (example: ``Exec_Env_Document``).


Semantic Version
----------------

Given a version number MAJOR.MINOR.PATCH, increment the:

- MAJOR version when you make incompatible API changes,
- MINOR version when you add functionality in a backwards compatible manner, and
- PATCH version when you make backwards compatible bug fixes.

Additional labels for pre-release and build metadata are available as extensions to the MAJOR.MINOR.PATCH format.


Updating Copyright
------------------

If you're a part of a corporation with an |NDA|, you may be required to update the LICENSE.

1. Check with your legal department first.
2. Add an appropriate line to the LICENSE file. See the Akamai entry for an example
3. When making a commit, add the specific copyright notice.

Double check with your legal department about their regulations. Not all changes
constitute new or unique work.


.. |NDA| replace:: :abbr:`NDA (Non-Disclosure Agreement)`
