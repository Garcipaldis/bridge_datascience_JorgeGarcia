## **Class Guide**

---------

**Work-in:**

1. AWS register
2. Create EC2
    ### Check city of the server (Ohio, London)!
    On EC2:
    3. Open Security Group - Inbound & Outbound all traffic. 
    4. Key Pairs - Import keys - **Directly in AWS** 
    5. Launch instance - Free tier -  Linux 2 AMI (HVM) SSD
        - With the key-pair
        - With the Security Group
        - All basics
        https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html#ec2-launch-instance

5. Install python-env
6. Create requirements.txt
7. Create Dockerfile in your project with necessary requeriments.txt

8. Filezilla: ssh - To send files - https://filezilla-project.org/download.php
    - Connect using your private .ppk
    - Send the project. "__EXECUTOR__.sh", "Dockerfile", "install_docker_yum.sh" and "install_python_yum.sh" must be in the same folder of the project.

9. Connect to EC2 via ssh. There, in the same folder of the project, execute:

  9.1: "bash install_docker_yum.sh" without ""
    9.1.1 This install docker (only execute one time)
  9.2: "bash __EXECUTOR__.sh" without "". This script:
    9.1 Build the Docker image 
    9.2 Create a Docker container with Python and the project inside itself
    9.3 Install every single library in requirements.txt
    9.4 Expose two ports
    9.5 Run flask and streamlit

10. Check all is great using the public ip of your EC2 instance

---------

**Work-out:**

1. Do the same as previous with your ML project to expose Streamlit and flask publically
2. Improve streamlit & flask of project

---------

*Remember, you have many cheatsheets. Learn to use it.*

*PythonTutor is your friend... take care of it.*

*Use Google everytime you need. Google must be your shadow.*

---------

**Lead Instructor**: *Gabriel Vázquez Torres*

- gabriel@thebridgeschool.es

*Tutorials*: https://calendly.com/gabrielvazqueztb

**Teacher Assistant**: *Borja Puig de la Bellacasa*

- borja@thebridgeschool.es

*Tutorials*: https://calendly.com/borpuig/15min

**Teacher Assistant**: *Leonardo Sánchez*

- leonardo@thebridgeschool.es

*Tutorials*: https://calendly.com/leo-sanchez 