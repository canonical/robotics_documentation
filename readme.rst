Robotics Documentation
======================

This repository contains the documentation for the Canonical Robotics stack.

It was originally bootstrapped from the
`canonical/sphinx-docs-starter-pack <https://github.com/canonical/sphinx-docs-starter-pack>`_
template, and is now maintained as a project-specific documentation set.

What this repo is
-----------------

- Product documentation for Canonical Robotics (content in ``docs/``)
- Sphinx-based documentation build and validation tooling
- Repository-specific configuration and workflows layered on top of the starter pack

What this repo is not
---------------------

- Not the generic starter-pack template itself
- Not a source of truth for template-wide guidance

For template-level guidance and updates, see:
`canonical/sphinx-docs-starter-pack <https://github.com/canonical/sphinx-docs-starter-pack>`_

Quick start
-----------

From the repository root:

.. code-block:: bash

   make install
   make run

Then open http://127.0.0.1:8000.

Useful local checks
-------------------

.. code-block:: bash

   make html
   make spelling
   make linkcheck

Contributing
------------

- Edit documentation content under ``docs/``.
- Keep repository-specific settings in this repository.
- When needed, manually adopt relevant changes from the starter pack instead of
  replacing local project content with template defaults.

License
-------

See ``LICENSE`` for licensing information.
