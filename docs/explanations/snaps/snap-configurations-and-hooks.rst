

Snap configurations and hooks
=============================

Snaps have the capabilities to trigger actions depending on ``snapd`` hooks. These hooks are also the entry point to manage your snap parameters. Snap support being configured by the means of parameters.

As an example for a robotics snap this could be used to select the right LIDAR device.

What are hooks?
------------------

A hook is an executable file that runs within a snap’s confined environment when a certain action occurs.

Common examples of actions requiring hooks include:

* Notifying a snap that something has happened
    Example: If a snap has been upgraded, the snap may need to trigger a scripted migration process to port an old data format to the new one.
* Notifying a snap that a configuration was done
    Example: When the user runs snap set|unset to change a configuration option

A hook is defined as an executable within a snap’s ``hooks/`` directory. Hooks are usually POSIX shell scripts. The filename of the executable is based on the name of the hook. All the hooks stored in ``snap/hooks/`` are automatically going to be imported in our snap. ``snapd`` will execute the file when required by that hook’s action.

The following hooks are currently implemented:

* `configure hook <https://snapcraft.io/docs/supported-snap-hooks#heading--the-configure-hook>`_
* `full-disk-encryption hook <https://snapcraft.io/docs/supported-snap-hooks#heading--fde>`_
* `gate-auto-refresh <https://snapcraft.io/docs/supported-snap-hooks#heading--gate-auto-refresh>`_
* `install hook <https://snapcraft.io/docs/supported-snap-hooks#heading--install>`_
* `install-device hook <https://snapcraft.io/docs/supported-snap-hooks#heading--install-device>`_
* `interface hooks <https://snapcraft.io/docs/supported-snap-hooks#heading--interface>`_
* `prepare-device hook <https://snapcraft.io/docs/supported-snap-hooks#heading--prepare-device>`_
* `pre-refresh hook <https://snapcraft.io/docs/supported-snap-hooks#heading--pre-refresh>`_
* `post-refresh hook <https://snapcraft.io/docs/supported-snap-hooks#heading--post-refresh>`_
* `remove hook <https://snapcraft.io/docs/supported-snap-hooks#heading--remove>`_

Hooks are called with no parameters. When a hook needs to request or modify information within ``snapd``, they can do so via the ``snapctl`` tool, which is always available within a snap’s environment. The  `snapctl tool <https://snapcraft.io/docs/using-snapctl>`_ can be used to access parameters, interface connections or even control our snap daemons.

Since our hooks are scripts we must make sure to make them executable. We can do so with:

.. code:: shell

    chmod +x snap/hooks/*


Snap configurations
--------------------

Snaps can have configurations. With these configurations our snaps can expose different behaviour, or we can set parameters options for our background services.

Snap configurations work hand in hand with hooks. Every time we set a parameter the configure hook is called. This might remind the mechanism of `ROS dynamic reconfigure <http://wiki.ros.org/dynamic_reconfigure>`_. In the hook script, we can decide if we want to take actions based on the new parameter. We can also use the ``install`` hook to define the parameters.

The command snap set|get allows us to access configurations. An example would be:

.. code:: shell

    $ sudo snap set mysnap myconfig=2

    $ sudo snap get mysnap myconfig

    2



The entire set of configuration options can be dumped as JSON by using the ``-d`` option:

.. code:: shell

    $ sudo snap get -d snapcraft
    {
        "provider": "lxd"
    }



These configurations can be accessed from within the snap.

As presented, the ``snapctl`` tool can be used inside the snap to access a parameter with the command:

.. code:: shell

    snapctl get myconfig


To manage our configuration we will need to define our hooks.

The ``install`` hook file ``snap/hooks/install`` :



.. code:: shell

    #!/bin/sh -e
    # set default configuration value
    snapctl set myconfig=false

And the configure hook file ``snap/hooks/configure``:

.. code:: shell

    #!/bin/sh -e
    MYCONFIG="$(snapctl get myconfig)"

    case "$MYCONFIG" in
            "true") ;;
            "false") ;;
            *)
                >&2 echo "'$MYCONFIG is not a supported value for myconfig." \
            "Possible values are true, false"
                return 1
                ;;
    esac

    snapctl stop "$SNAP_INSTANCE_NAME"
    snapctl start "$SNAP_INSTANCE_NAME"

With these two simple hooks, we define a parameter in the ``install`` hook. When it’s set we make sure in the configure hook that the parameter was acceptable. Finally, we decide to restart our application. All that with the help of the ``snapctl`` command.

Later in our application we can also use the ``snapctl`` command to get the value of our parameter and use it.

The parameters are kept over updates, but we can of course define a ``post-refresh`` hook if we want a custom behaviour for our updates and parameters.