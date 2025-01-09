Vcstool and rosinstall file
===========================

In ROS, it’s common to have the list of repositories listed in a `rosinstall file <https://docs.ros.org/en/independent/api/rosinstall/html/rosinstall_file_format.html>`_. These files are read by `Vcstool <https://github.com/dirk-thomas/vcstool>`_ to import the specified repositories.

In the ``snapcraft.yaml``, writing multiple parts in order to cover multiple git repositories might not be necessary. Instead, a ``rosinstall`` file could be used.

Snapcraft `support various source-type <https://snapcraft.io/docs/snapcraft-yaml-schema>`_ but ``rosinstall`` is not part of the default implementation. Fortunately, we can still leverage the features of ``Vcstool`` within snapcraft by the means of the `overrides part steps <https://snapcraft.io/docs/overrides>`_ feature.


Overrides part steps
--------------------

Snapcraft provides plugins that ease the build steps of our parts. It automatises everything based on the most common way to use a tool.

Obviously, sometimes we might need to do things slightly differently. And that is why snapcraft has an `overrides part steps <https://snapcraft.io/docs/overrides>`_ feature. This feature allows overriding and customising steps of a  `part’s life-cycle <https://snapcraft.io/docs/parts-lifecycle>`_ (pull, build, stage, and prime). Also, we can still call the default step action within our script. As an example, we display a message at the end of our build with:

.. code:: yaml

    parts:
    foo:
        plugin: colcon
        # ...
        override-build: |
        craftctl build
        echo "Everything built!"

That is exactly what we need for our ``rosinstall`` case.

Using Vcstool
-------------

With a ``rosinstall`` file call ``my_robot.rosinstall`` placed at the root of our repository, we could simply call ``Vcstool`` manually. Also, we should make sure that ``python3-vcstool`` is listed in our ``build-packages`` as we will need it at build-time.

.. code:: yaml

    parts:
    workspace:
        plugin: colcon # or catkin
        source: . # import our rosinstall file
        build-packages: [python3-vcstool]
        override-pull: |
        craftctl default # or snapcraftctl pull
        # Here we are going to use the local .rosinstall file
        vcs import --input my_robot.rosinstall


As we can see apart from the ``rosinstall`` specificity, building a whole robot stack inside a robot is actually as simple as building a basic `talker-listener` example.