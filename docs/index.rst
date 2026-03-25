Robotics Documentation
======================

.. toctree::
  :hidden:
  :maxdepth: 3

  tutorials/index
  how-to-guides/index
  references/index
  explanations/index

**Ubuntu gives robotics teams a complete, production-grade platform** to package, deploy, and maintain robot software at scale.

**Ubuntu Core, Snaps, ROS ESM, and the Dedicated Snap Store work together** to provide secure, reliable infrastructure for building, distributing, and updating robot applications — from a single device to a global fleet.

**Robotics developers shouldn't have to become DevOps engineers.** Our open source tools take the infrastructure burden off your plate, so you can focus on building great robots.

**This platform is for software developers and system integrators** who need to ship robot applications reliably – without building deployment infrastructure from scratch.

In this documentation
=====================

* **First Steps:** :doc:`Canonical Robotics Stack overview <references/ref_architecture/reference_architecture>` | :doc:`Deploy a robot with snaps and Ubuntu Core <tutorials/snaps-core/index>` | :doc:`Monitor your robot fleet with COS for robotics <tutorials/observability/index>`
* **Packaging & distribution:** :doc:`Package a ROS application as a snap <tutorials/snaps-core/packaging-ros-application-as-snap>` | :doc:`ROS architectures with snaps <explanations/snaps/ros-architectures-with-snaps>` | :doc:`Migrate from Docker to snap <how-to-guides/packaging/migrate_from_docker_to_snap>` | :doc:`Snapcraft plugins <references/snapcraft/plugins>` and :doc:`extensions <references/snapcraft/extensions>` for ROS
* **Observability & monitoring:** :doc:`What is COS for robotics <explanations/observability/what-is-cos-for-robotics>` | :doc:`COS components <explanations/observability/components-explanations>` | :doc:`Alert rules configuration <explanations/observability/alert-rules-configuration-from-device>` | :doc:`Deploy COS with TLS encryption <how-to-guides/operation/deploy-cos-for-robotics-with-tls-encryption>`
* **Security:** :doc:`Harden your robot <how-to-guides/security/hardening-your-robot>` | :doc:`What is ROS ESM <explanations/security/what-is-ros-esm>` | :doc:`Security vulnerability audits <explanations/security/security-audits>` | :doc:`Security considerations for COS <explanations/observability/security-considerations-for-cos>`
* **Maintenance & operations:** :doc:`Dedicated Snap Store <explanations/dedicated-snap-store>` | :doc:`Observe COS for robotics <how-to-guides/operation/observe-cos-rob>` | :doc:`Enable ROS ESM <how-to-guides/maintenance/enable-ros-esm>` | :doc:`Check if a CVE is fixed <how-to-guides/maintenance/check-cves>`

How this documentation is organized
-------------------------------------

.. list-table::
   :header-rows: 0
   :widths: 50 50

   * - `Tutorials <tutorials>`__

       .. include:: tutorials/index.md
          :start-after: % Include start summary
          :end-before: % Include stop summary

     - `How-to guides <how-to-guides>`__

       .. include:: how-to-guides/index.md
          :start-after: % Include start summary
          :end-before: % Include stop summary

   * - `Explanation <explanations>`__

       .. include:: explanations/index.md
          :start-after: % Include start summary
          :end-before: % Include stop summary

     - `Reference <references>`__

       .. include:: references/index.md
          :start-after: % Include start summary
          :end-before: % Include stop summary

Project and community
=====================

Snap, snapcraft and Ubuntu Core projects are members of the Ubuntu family. They are open source projects that warmly welcome community projects, contributions, suggestions, fixes and constructive feedback.

* `Our Code of Conduct <https://ubuntu.com/community/ethos/code-of-conduct>`_
* `Community engagement commitment <https://documentation.ubuntu.com/core/explanation/community-engagement/>`_
* `How to get support <https://discourse.ubuntu.com/c/project/robotics/121>`_
* `Join the Discourse forum <https://forum.snapcraft.io/c/device/10>`_
* `Interactive chat on Matrix.org <https://ubuntu.com/community/communications/matrix>`_
* `Product roadmap <https://snapcraft.io/docs/snapd-roadmap>`_

Thinking about using Ubuntu Core for your next project? `Get in touch! <https://ubuntu.com/core/contact-us>`_

.. _heading--navigation:






..    .. list-table::
..       :header-rows: 1

..       * - Old path
..         - New URL
