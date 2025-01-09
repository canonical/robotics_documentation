Application orchestration
=========================

Snap robotics applications can be called from the terminal but also run in the background as daemons. Snap and snapcraft offer orchestration features that can become handy for robotics applications.

Command-chain
-------------

*Valid for CLI: Yes*

*Valid for daemon: Yes*


The ``command-chain`` keyword allows us to list commands to be executed before our main command. The `ros1-noetic extension <https://snapcraft.io/docs/ros-noetic>`_ is actually using this mechanism. Thanks to it, we don’t have to worry about sourcing the ROS environment in the snap.

The main difference between ``command-chain`` and simply adding commands to the script launcher is that ``snapd`` is aware of it. Hence, if we are trying to debug something (with ``snap run --shell myapp``) the command chain is still going to be called.

Note that an ``exec $@`` is necessary at the end of our ``command-chain`` scripts since our actual command is given as an argument of the ``command-chain``.

This means that with the following snapcraft example:

.. code:: yaml

    apps:
    my_app:
        command-chain: [command_chain_script1, command_chain_script2]
        command: main_command

The generated call will be:

.. code:: shell

    ./command_chain_script1 command_chain_script2 main_command

Potential use cases of command-chain are:

* Set up a shell environment (like setting up a ROS environment)
* Wait for another service to be started

Stop-command
------------

*Valid for CLI: No*

*Valid for daemon: Yes*

``stop-command`` allows one to specify a script, or a command, to be called right before the stop signal is sent to a program. This is only available for daemons since this is triggered by the ``snap stop`` command.

Potential use cases of stop-command are:

* Make sure everything is synchronised
* Wait for a job to finish
* Save before exiting

Post-stop-command
-----------------

*Valid for CLI: No*

*Valid for daemon: Yes*

Similarly to the ``stop-command`` entry, the ``post-stop-command`` is also calling a command, but this time, only after the service is stopped. This means that in the sequence we are calling ``stop-command``, then stopping the command with a signal and once it’s done we call the ``post-stop-command``. Also, only available for daemons.

Potential use cases of ``post-stop-command`` are:

* Clean-up after program exited (temporary files etc)
* Notify a system that the command has stopped
* Move generated files

The ``snapcraft`` `documentation for daemons <https://snapcraft.io/docs/services-and-daemons>`_ describes many more features that could be useful in other projects.