# Identify functionalities and applications of a robotics snap

Since snap is meant to deploy applications, we must define our robot applications. Our robot applications are meant to fulfil the functionalities of a robotics product.


## Robot functionalities

The robot functionalities are defined by the product. They refer to how a person/customer can use a product or what they can do with it. These functionalities are defined by the person in charge of the product definition. The functionalities usually come from the customer's needs.

Snaps are going to be a support to distribute those software functionalities. They must be identified before starting the snapping of the software stack.

As an example, a supermarket needs a robot to clean the floor and possibly patrol at night. The functionalities associated are:

- The robot must be able to clean the floor.
- The robot must be able to patrol.

For the robot to have such functionalities, developers must create applications. One functionality can be performed by one or multiple applications. Some applications can even be used for multiple functionalities.

In the following drawing, we represented the two functionalities: “Clean the floor” and “Patrol”. Both functionalities need their own application. Additionally, they share an application to control the mobile base.

![|624x239](https://lh6.googleusercontent.com/gOoI-JvGvUhOWNoJ2vq9N2jb3gacSR2ya97NVWZfGB4Jsuy7QDjC73Ldj_RUS_6dCCJqPUKzBl8UC1raUsou0DeAna0jPmpKU8M66LuEiEBRy2X0kQyopADEz4QHFVZHpcvnWf_rFlcgG1f88pbc4KA)

## Snap applications


### What are snap applications?

Applications can be programs to call from a terminal or daemons if we need them to start automatically at boot or as background services. One snap can contain one or multiple applications.

An example would be the “bring up”. This application will be responsible for running the robot model and motor controllers. This application would be a background service available for other applications.


### Define the role and the scope of the applications

#### Identify the applications and their roles

Designing our snap is very much like designing a library. We must first define what the API will be. Based on the desired functionalities, we must define what are the key components but also, identify the scope of each component. We want the applications of a snap to be at the same time independent enough to make sense as an application, but also modular enough to be potentially composed with each other.

**Think about the final user.** When distributing our software, we want to keep it as simple as possible for the user to use it. Seeing our robotics application from the user perspective will guide us toward our snap designing decisions.

Reusing our supermarket robot cleaner example, all our functionalities require the same base (the same bring-up) to control the robot, etc. We will define one background service to start all the basic controls etc and two different applications for our robot use cases.


#### Define the applications

Defining the applications will be the task of expanding our ROS workspace into an application-oriented workspace.

For instance, a single snap application can replace all the launch files and commands called.

In the case of the Patrol application, one might need to run one `launchfile` and call a service at the start. All this can be done within one application simplifying the end-user experience.

We must also identify what applications must be started automatically at boot and which ones are commands to be called from the terminal.

The majority of the applications implementing functionalities are going to be started as daemons at boot, but we might want some calibration routines to be only started manually from the terminal.


#### Snap architecture

Finally, while the simplest snap architecture is one snap containing all our applications, we could also have a multi-snap architecture in order to distribute our application across multiple snaps. All the possible architectures for a ROS application are described [in the documentation](/docs/explanations/snaps/ros-architectures-with-snaps) for further investigation.


#### Example

To illustrate a potential structure of snap applications within a snap, we represented an example of such a structure.

In the following picture, we see “supermarket-robot-snap” containing all our applications. The snap contains all the OS/system and ROS dependencies. These dependencies can be Debian or manually built and installed ROS packages. Similarly, our snap contains any file necessary for our applications. The first application “core”, is a background service meant to be always running. The application is responsible for running all the basic and common nodes (robot model, motors controllers). It is shared and used by the two other applications. The second application “Patrol”, is also a background service, but we can enable/disable it. This application will be responsible for patrolling behaviour meaning sending navigation goals and reporting suspicious activity. The Patrol application is fulfilling our desired “Patrol” functionality. The last application “Clean”, is also an activatable background service. This application is responsible for cleaning of the floor, meaning navigating and activating the correct actuators. This application is fulfilling the “Clean” functionality of our product.

As we can see everything is packaged inside a single snap but yet let the developer define multiple applications covering all the software functionalities of a robot.

![|605x380](https://lh4.googleusercontent.com/dl5thSNLWZZTAysnewv1TBuTbXnYSOoHu6lUg6TJZDV7QnRsIunEWpGDGNzpKZ5_FNyzKNYfbXzHe9gwb7Y9kWgbtSvVa2_aSmwdjTzDaQLu0aho0sPXPR3ks0vIqvU29fPpxlVedrpWYxkXSqpz-PI)
