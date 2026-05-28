Ubuntu Robotics documentation
=============================

*Source for the Ubuntu Robotics documentation site, built with Sphinx and bootstrapped from the `Canonical sphinx-stack template <https://github.com/canonical/sphinx-stack>`_. This repository documents the Ubuntu Robotics stack; it is not the template itself.*

This repository contains the documentation for Canonical's Ubuntu Robotics stack,
including packaging and distribution with snaps, observability with COS for
Robotics, security hardening, and ROS ESM guidance.

Repository layout
-----------------

The documentation source lives under :file:`docs/`.

Key locations:

* :file:`docs/index.rst` - documentation home page
* :file:`docs/tutorials/` - guided, learning-oriented tutorials
* :file:`docs/how-to-guides/` - task-focused maintenance and operations guides
* :file:`docs/references/` - reference material
* :file:`docs/explanations/` - conceptual background
* :file:`docs/Makefile` - local build, preview, and validation targets
* :file:`.github/workflows/` - CI checks that run for documentation changes

Contributing
------------

Prerequisites
~~~~~~~~~~~~~

Install the core tools used by the local documentation workflow:

.. code-block:: bash

   sudo apt update
   sudo apt install make python3 python3-venv python3-pip

Some optional checks also require additional tooling:

.. code-block:: bash

   sudo apt install npm snapd

Local setup
~~~~~~~~~~~

From :file:`docs/`, create the virtual environment and install dependencies:

.. code-block:: bash

   cd docs
   make install

Local preview
~~~~~~~~~~~~~

Run a live-reloading preview server:

.. code-block:: bash

   cd docs
   make run

Then open ``http://127.0.0.1:8000`` in your browser.

Local build and checks
~~~~~~~~~~~~~~~~~~~~~~

Before opening a pull request, run the checks that match your change.

Build the site cleanly:

.. code-block:: bash

   cd docs
   make clean-doc
   make html

Lint Markdown:

.. code-block:: bash

   cd docs
   make lint-md

Check spelling:

.. code-block:: bash

   cd docs
   make spelling

Check inclusive language:

.. code-block:: bash

   cd docs
   make woke

Run style-guide linting with Vale:

.. code-block:: bash

   cd docs
   make vale

Check links:

.. code-block:: bash

   cd docs
   make linkcheck

Optional accessibility check:

.. code-block:: bash

   cd docs
   make pa11y-install
   make pa11y

GitHub Actions also run documentation checks for pull requests that touch
:file:`docs/`.

Maintainer pull request workflow
--------------------------------

Use a git worktree rather than editing directly in your main checkout. A typical
maintainer workflow looks like this:

.. code-block:: bash

   git fetch origin
   git worktree add ../robotics_documentation-my-change -b docs/my-change origin/main
   cd ../robotics_documentation-my-change

Make your changes, run the relevant checks from :file:`docs/`, then commit and
push your branch:

.. code-block:: bash

   git status
   git add readme.rst docs/
   git commit
   git push -u origin docs/my-change

Open a pull request against ``main`` and let CI complete before requesting
review or merging. Avoid force-pushing once review is in progress unless there
is a clear need to rewrite history.

Notes for maintainers
---------------------

* Keep repository-level guidance in this README focused on this documentation
  project, not on the upstream template.
* If pages move, add redirects in :file:`docs/conf.py` so existing links keep
  working.
* Add project-specific spelling exceptions to :file:`docs/.custom_wordlist.txt`
  instead of editing shared upstream word lists.
* When adjusting documentation structure, update the relevant index or toctree
  pages under :file:`docs/`.

Resources
---------

* `Ubuntu Robotics documentation site <https://canonical-robotics.readthedocs-hosted.com/>`_
* `Ubuntu Robotics on Ubuntu.com <https://ubuntu.com/robotics>`_
* `Canonical sphinx-stack template <https://github.com/canonical/sphinx-stack>`_
