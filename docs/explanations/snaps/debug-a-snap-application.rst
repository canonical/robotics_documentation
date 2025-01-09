Debug a snap application
========================

Once a snap is built and installed one might face unexpected problems like missing a configuration file or a library or simply not the expected behaviour.

Even if snaps are immutable there are still means to introspect and analyse their state as well as running tests inside the snap environment.

Keep in mind that we want to debug the packaging. Debugging your own code etc should be done prior and outside the packaging.


Snap logs
---------

When we call a snap app command, the logs are usually printed in the terminal. On the contrary when we are running a daemon, the logs are not instantly visible. Snap daemon are ``systemd`` background services.

To visualise the last 100 lines of a snap daemon:

.. code:: shell

    sudo snap logs SNAP_NAME.DAEMON_NAME -n 100


In case we want to wait for new lines and print them as they come in. We can use the -f option.

Additionally, if our snap contains multiple applications daemons, we can log them all by simply omitting the application name:

.. code:: shell

    sudo snap logs SNAP_NAME -f


Similarly, we can use the pure systemd command:

.. code:: shell

    journalctl -u snap.SNAP_NAME.DAEMON_NAME.service

As we can see, snap daemon are simply ``systemd`` services with the ``snap.`` prefix and the ``.service`` suffix. For the sake of simplicity, the ``snap logs`` command is preferred,

If the robot is not behaving as expected this should be the first action.

This way we can quickly check the output of our ``launchfiles``.


Snap environment
----------------

When our snap is built and installed but doesn’t work as expected there are solutions. Our snap is running in a confined and containerised environment making the debugging sometimes more difficult.

Snap file structure
~~~~~~~~~~~~~~~~~~~


If we are curious about the folder/file structure of our system, we can simply check it from our host. As an example, we can list the files at the root of our snap system with:

.. code:: shell

    $ ls /snap/SNAP_NAME/current

    etc/ lib/ meta/ opt/ usr/ var/


Everything under this directory ``/snap/SNAP_NAME/current`` is only for our snap. When strictly confined, our snap cannot access anything outside this (apart from the different data directories). Checking the files in this directory can sometimes be enough to figure out our issue.

Snap run
~~~~~~~~

When it’s not enough, and we actually need to be in the snap environment to debug, we can run the snap run command along with the ``--shell`` option.

.. code:: shell

    snap run --shell SNAP_NAME.APP_NAME


This command is actually going to start a shell of the snap app environment (``command-chain`` included) instead of starting our app. This way, **we have the exact same environment** to run any kind of command. We can even call the application ourselves if we want to reproduce the issue. We can also potentially launch an entirely different command. Furthermore, we can then check the environment variables, files location, permissions etc.

Note that when calling ``snap run --shell`` the started shell will be in the same directory where the command was called. Shelling into the snap environment will keep the original snap permissions.

This method has a very high potential for debugging our snaps.

Debugging a missing library
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Robotics applications sometimes rely on hundreds of dynamic libraries. A very common error is that when an application starts, a library is missing. When this is happening a good way to verify that is to use ``ldd``. It will print the shared object libraries and their paths as they are found. So after calling the ``snap run --shell SNAP_NAME.APP_NAME`` it’s the perfect moment to call ``ldd`` on a library.

.. code:: shell

    $ ldd $SNAP/opt/ros/foxy/lib/librmw.so

    linux-vdso.so.1 (0x00007fff841c5000) librcutils.so => /snap/MYSNAP/REVISION/opt/ros/foxy/lib/librcutils.so (0x00007f4c2276a000)

    libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f4c2251b000)

    libdl.so.2 => /lib/x86_64-linux-gnu/libdl.so.2 (0x00007f4c22515000) /lib64/ld-linux-x86-64.so.2 (0x00007f4c2278d000)

In case one library is marked as not found, the definition of ``$LD_LIBRARY_PATH`` is usually at fault.

If a library is missing in the library path but is installed, we can find its location with the help of the find command after entering the snap shell:

.. code:: shell
 
    find $SNAP -type f -name "librmw.so"



Snap connections
----------------

Snaps are strictly confined, but they can access our host by the means of interfaces. These interfaces can sometimes be the source of our problems. Let’s see the different ways to troubleshoot them.

The very first thing that can help is the following command:

.. code:: shell

    $ snap connections lxd

    Interface        Plug                Slot             Notes

    lxd              multipass:lxd       lxd:lxd          -
    Lxd-support      lxd:lxd-support     :lxd-support     -
    network          lxd:network         :network         -
    network-bind     lxd:network-bind    :network-bind    -
    system-observe   lxd:system-observe  :system-observe  -

Here we listed all the connections of our snap ``lxd``. As we can see all the interfaces have a ``plug`` and a ``slot``. This means that everything is connected.

Some interfaces are auto-connect while some others are not. This means that we must connect them manually.

To do so we must use the command snap connect. An example of the usage would be:

.. code:: shell

    sudo snap connect SNAP_NAME:camera :camera

The command above presupposes that our snap application had the `camera plug declared <https://snapcraft.io/docs/camera-interface>`_. Similarly, we can use the ``snap disconnect`` command to undo the ``connect`` action.

When a snap cannot access a host resource that it was declared to access, checking the connection is usually a good starting point.

One can `request “auto-connect“ on the forum <https://snapcraft.io/docs/process-for-aliases-auto-connections-and-tracks>`_ of an interface that doesn't auto-connect for a snap.

Snappy-debug
------------

The snap, being strictly confined, sometimes tries to access resources that were not declared. It generates an `App Armor <https://apparmor.net/>`_ policy violation that might be hard to diagnose.

The easiest way to find and fix policy violations is to use `the snappy-debug tool <https://snapcraft.io/snappy-debug>`_. It’s a tool provided by Canonical and allows us to:

* watches syslog for policy violations
* shows them in a human-readable format
* get recommendations for how to solve them

We can install the ``snappy-debug`` tool with the command:

.. code:: shell

    sudo snap install snappy-debug


We can then call the ``snappy-debug`` command and in another terminal, call our snap app. The `snappy-debug` tool could then produce an output similar to the following one:

.. code:: text

    mars 02 17:27:39 user-computer audit[721546]: AVC apparmor="DENIED" operation="open" profile="snap.SNAP_NAME" name="/dev/video0" pid=721546 comm="APP" requested_mask="c" denied_mask="c" fsuid=1000 ouid=1000


In this log we can see that the access to ``/dev/video0`` was attempted and denied. This gives us the information that either our snap misses the ``camera`` ``plug``, or that we simply forgot to connect it.