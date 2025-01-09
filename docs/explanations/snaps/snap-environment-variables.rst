Snap environment variables
==========================

Environment variables are widely used across Linux to provide convenient access to system and application properties. Both ``snapcraft`` and ``snapd`` consume, set, and pass-through specific environment variables to support building and running snaps.

All the following examples are assuming the snap ``hello-world`` revision 27.

Snap makes available certain environment variables to identify the snap at run-time.


SNAP
----

The most important environmental variable is `$SNAP`. It contains the path to the directory where the snap is mounted. This is where all the installed files in our snap are visible in the filesystem. Remember, an installed snap is read-only and cannot be changed.

This variable is typically pointing to the host location:

.. code:: shell

    /snap/hello-world/27

Which is the snap revision specific installation path. It also corresponds to:

.. code:: shell

    /snap/hello-world/current


The typical use cases of this variable are:

* Locate a file relatively to the snap (an executable, a library, configuration file)
* Extend the ``$LD_LIBRARY_PATH`` to a new location inside our snap.

This variable is available with ``snapd`` and ``snapcraft``.

SNAP_INSTANCE_NAME
------------------

The ``$SNAP_INSTANCE_NAME`` variable is less common.

This variable is going to contain the exact name of the snap. In the case of `snap parallel installs <https://snapcraft.io/docs/parallel-installs>`_ a snap could be installed under a different name. We could even have multiple times the same snap installed. By leveraging the ``$SNAP_INSTANCE_NAME`` we can make sure that we refer to our snap instance and not another one.

The typical use cases of this variable are:

* Restart a daemon application from a hook: ``snapctl restart $SNAP_INSTANCE_NAME.MY_APP``
* Make sure there are no confusion between parallel installs

The `snap documentation for environment variables <https://snapcraft.io/docs/environment-variables>`_ describe many more features that could be useful in other projects.