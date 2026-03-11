*This activity has been created as part of the 42 curriculum by maziza*

# Description

Born2beRoot is a system project aiming to teach how to setup the basics of user session, partitioning and users/admin rights.

To do so, I had to emulate OS through a Virtual Machine software such as Oracle VirtualBox and setup differents things to have a proper system environment.

## Project Description

As mentioned in the subject, I chose to work with Debian as the operating system, mainly because of its simplicity in setup and its beginner-friendly package management through apt. It also provides strong community support, great stability, and a well-documented environment. On the other hand, Rocky Linux is more enterprise-oriented and better suited for long-term stability in production environments, but slightly heavier and less intuitive for testing or learning setups.

Following the use of Debian, AppArmor was selected as the mandatory access control system. It integrates naturally with Debian and offers an easier configuration process compared to SELinux, which is more complex but known for its deeper control and stricter policies.

For firewall configuration, UFW (Uncomplicated Firewall) was used, since it’s the default option on Debian. It provides a straightforward command syntax and is ideal for quick setup. In comparison, firewalld, used mainly on Red Hat–based distributions like Rocky Linux, offers a more layered and dynamic approach but adds unnecessary overhead for this project.

Finally, Oracle VirtualBox was chosen for virtualization, as the development machine is Linux-based. UTM, while a good alternative, is primarily designed for macOS environments, which made VirtualBox a more logical choice.

# Instructions

To open the Virtual Machine setup by the learner, one must open it through the VM creator the learner used.

# Resources

To learn about the basics setup, I used a gitbook teaching about system setup, as well as different websites teaching how to use commands like lsblk or who.
