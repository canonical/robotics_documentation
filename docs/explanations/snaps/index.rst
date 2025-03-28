:sequential_nav: next

Snaps
=====

.. toctree::
   :maxdepth: 3
   :caption: snapcraft

   ROS architectures with snaps <ros-architectures-with-snaps.md>
   Identify functionalities and applications of a robotics snap <identify-functionalities-and-apps-of-robotics-snap.md>
   Snap configurations and hooks <snap-configurations-and-hooks>
   Snap data and file storage <snap-data-and-file-storage>
   Snap environment variables <snap-environment-variables>
   Application orchestration <application-orchestration>
   Vcstool and rosinstall file <vcstool-and-rosinstall-file>
   Debug the build of a snap <debug-the-build-of-a-snap>
   Debug a snap application <debug-a-snap-application>


Snaps are containers that bundle an application and all its dependencies. As such, snaps offer a solution to build and distribute containerised robotics applications or any software.

Snaps are ideal for robotics developers,developers as they bundle all your dependencies and assets in one package, making applications installable on dozens of Linux distributions and across distro versions. You won’t even have to install anything else on your robots’ operating system, no dependencies, not even ROS if you are using it.

The creation of snaps can be integrated into your CI pipeline, making the updates effortless. Snaps can update automatically and transactionally, making sure the device is never broken.

`Snapcraft <https://snapcraft.io/docs/snapcraft-overview>`_, the tooling for building snaps, comes with native integrations through plugins and extensions dedicated to both `ROS <https://snapcraft.io/docs/ros-applications>`_ and `ROS 2 <https://snapcraft.io/docs/ros2-applications>`_; developed and maintained by Canonical.


.. note::
   
   `Learn more about Snaps for robotics <https://snapcraft.io/docs/robotics>`_.

