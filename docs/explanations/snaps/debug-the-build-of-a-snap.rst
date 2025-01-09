Debug the build of a snap
=========================

Before the snap is built, things can already go wrong. The parts could fail to build, or the application declaration might even fail, etc.

When snapcraft is building our snap, it’s first starting a VM or a container. This way everything is built in an isolated environment. We can step into this environment in order to find out why our snap is not building.

Snapcraft environment
---------------------

When the command snapcraft is called, by default snapcraft is launching an instance with an isolated environment ( can be a container, a VM or even the host if enforced ). The instance default directory is ``/root`` which is containing multiple folders:

.. code:: shell

    ├── parts/
    ├── prime/
    ├── project/
    ├── snap/
    └── stage/


Most of these directories correspond to different `lifecycle steps <https://snapcraft.io/docs/parts-lifecycle#heading--steps>`_ of our snap building.


Project
~~~~~~~
This is the simplest directory. It’s simply the mount point of the directory from where we called the snapcraft command. 
The debugging value of this directory is rather low.


Parts
~~~~~

``Parts`` will contain different directories. One for each part. Inside each directory we will find a copy of the sources as well as the different build artefacts. 
We will retrieve our ROS workspace as well as the ``build/``, ``install/`` and ``log/`` folders. They might be useful to find out why our part is not building. 
We could for example check the content of log, cache files etc.

This corresponds to the different ``pull`` and ``build`` steps of the snap.

Stage
~~~~~
This corresponds to the ``stage`` step of the snap. The directory is going to be populated if the build step went well. 
It’s in this directory that we can make sure that everything we compiled and wanted to be installed in our snap is really present. 
This directory is populated by the ``stage-packages`` entry but also by the ``depend/exec-depend`` from your package.xml.


Prime
~~~~~
This corresponds to the ``prime`` step. This directory is going to be populated after the stage step. Only what is necessary at run time will be copied to this directory. 
The ``prime`` directory should contain absolutely everything our snap needs. It can be a cleaner version of the stage (e.g. without header files) or exactly the same content.


Snap
~~~~

This directory corresponds to the installed snap data directory. Indeed, some snaps are installed inside our container. 
An example would be all the ``build-snaps`` of our parts or even our base snap.

The instance environment itself is used to build our parts. This means that if one needed APT packages to build a part, they should be installed inside the instance itself. 
Hence, regular commands like ``apt``, ``dpkg``, etc can be used to inspect the packages available at build time.


Snapcraft debug
---------------

At the first error, the `snapcraft` command is going to fail and exit. This can be changed in order to step into the building environment after the error with the option ``--debug``. 
The command is then:

.. code:: shell

    snapcraft --debug

At the first error, we are going to step into our container in the ``/root/project`` folder.

We can then verify why our build is failing. Keep in mind that when entering the instance, the environment of the shell won’t be specific to any part. 
One might need to redefine environment variables or sources scripts.

The ``--debug`` option is the perfect solution in case the ``snapcraft`` command fails. When developing a snap it’s recommended to always enable this flag.


Snapcraft shell-after
---------------------

Sometimes there is no error but yet the built snap is not what we expected it to be. We can still check the state of the building environment with the flag ``--shell-after``. 
With this flag, once our snap is completely built we will still step into the build environment. The complete command is:

.. code:: shell

    snapcraft --shell-after

We will enter the instance environment similarly to the `--debug` flag.


Snapcraft try
-------------

The `snapcraft try command <https://snapcraft.io/docs/snap-try>`_ can be used in combination with ``snap try`` to quickly test a snap and fix issues.

``snapcraft try`` runs through the build process to the completion of the prime stage. It then exposes the resultant prime directory to the snapcraft directory.

Once you run:

.. code:: shell

    snapcraft try

To use the built snap you can then run:

.. code:: shell

    snap try prime

This way you can modify the content of the ``prime/`` directory without having to rebuild the snap. As an example we could modify a ``launchfile``, a python script, etc.