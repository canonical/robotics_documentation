Ubuntu Robotics documentation
=============================

Source for the `Ubuntu Robotics documentation site <https://canonical-robotics.readthedocs-hosted.com/en/latest/>`__, built with Sphinx and bootstrapped from the `Canonical sphinx-stack template <https://github.com/canonical/sphinx-stack>`__. This repository documents the Ubuntu Robotics stack; it is not the template itself.

This repository contains the documentation for Canonical's Ubuntu Robotics stack,
including packaging and distribution with snaps, observability with COS for
Robotics, security hardening, and ROS ESM guidance.

Repository layout
-----------------

The documentation source lives under `docs/ <docs/>`__.

Key locations:

* `docs/index.rst <docs/index.rst>`__ - documentation home page
* `docs/tutorials/ <docs/tutorials/>`__ - guided, learning-oriented tutorials
* `docs/how-to-guides/ <docs/how-to-guides/>`__ - task-focused maintenance and operations guides
* `docs/references/ <docs/references/>`__ - reference material
* `docs/explanations/ <docs/explanations/>`__ - conceptual background
* `docs/Makefile <docs/Makefile>`__ - local build, preview, and validation targets
* `.github/workflows/ <.github/workflows/>`__ - CI checks that run for documentation changes

Contributing
------------

Prerequisites
~~~~~~~~~~~~~

Install the core tools used by the local documentation workflow:

.. code-block:: bash

   sudo apt update
   sudo apt install make python3 python3-venv python3-pip

The optional accessibility check requires additional tooling:

.. code-block:: bash

   sudo apt install npm

Local setup
~~~~~~~~~~~

From `docs/ <docs/>`__, create the virtual environment and install dependencies:

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
`docs/ <docs/>`__.

Maintainer pull request workflow
--------------------------------

Use a git worktree rather than editing directly in your main checkout. A typical
maintainer workflow looks like this:

.. code-block:: bash

   git fetch origin
   git worktree add ../robotics_documentation-my-change -b docs/my-change origin/main
   cd ../robotics_documentation-my-change

Make your changes, run the relevant checks from `docs/ <docs/>`__, then commit and
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
* Redirect strategy divergence from upstream template: this repository intentionally
  keeps `sphinx-reredirects` with an inline ``redirects = {}`` mapping in
  `docs/conf.py <docs/conf.py>`__ instead of `sphinx-rerediraffe` with a
  ``redirects.txt`` file. Preserve this choice during future stack updates unless
  you deliberately migrate redirect tooling.
* If pages move, add redirects in `docs/conf.py <docs/conf.py>`__ so existing links keep
  working.
* Add project-specific spelling exceptions to `docs/.custom_wordlist.txt <docs/.custom_wordlist.txt>`__
  instead of editing shared upstream word lists.
* When adjusting documentation structure, update the relevant index or toctree
  pages under `docs/ <docs/>`__.

Resources
---------

* `Ubuntu Robotics documentation site <https://canonical-robotics.readthedocs-hosted.com/>`_
* `Ubuntu Robotics on Ubuntu.com <https://ubuntu.com/robotics>`_
* `Canonical sphinx-stack template <https://github.com/canonical/sphinx-stack>`_
