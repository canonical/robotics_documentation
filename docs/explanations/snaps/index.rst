:sequential_nav: next

Snaps
=====

Snaps are containers that bundle an application and all its dependencies.
As such, snaps offer a solution to build and distribute containerized
robotics applications or any software.

Snaps are ideal for robotics developers,
as they bundle all your dependencies and assets in one package,
making applications installable on dozens of Linux distributions and across distributions versions.
You won't even have to install anything else on your robots' operating system,
no dependencies, not even ROS if you are using it.

The creation of snaps can be integrated into your CI pipeline,
making the updates effortless.
Snaps can update automatically and transactionally,
making sure the device is never broken.

`Snapcraft <https://snapcraft.io/docs/snapcraft-overview>`_, the tooling for building snaps,
comes with native integrations through plugins and extensions dedicated to both
`ROS <https://snapcraft.io/docs/ros-applications>`_ and `ROS 2 <https://snapcraft.io/docs/ros2-applications>`_;
developed and maintained by Canonical.

.. toctree::
   :maxdepth: 1

   ros-architectures-with-snaps.md
   identify-functionalities-and-apps-of-robotics-snap.md
   snap-configurations-and-hooks
   snap-data-and-file-storage
   snap-environment-variables
   application-orchestration
   vcstool-and-rosinstall-file
   debug-the-build-of-a-snap
   debug-a-snap-application
