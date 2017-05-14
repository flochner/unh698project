# Deploying and Monitoring a Website

#### Services
 - GitHub [link](https://github.com/features)
 - Docker Cloud [link](https://cloud.docker.com/swarm/fml2001/dashboard/onboarding/continuous-integration)
 - Amazon Web Services [link](https://aws.amazon.com/what-is-cloud-computing/?nc2=h_l2_cc)

#### Software
 - Python [link](https://www.python.org/about/gettingstarted/)
 - Flask [link](http://flask.pocoo.org/docs/0.12/tutorial/#tutorial)
 - Docker [link](https://www.docker.com/what-docker#/overview)
 - Ansible [link](https://www.ansible.com/continuous-delivery)
 - Prometheus [link](https://prometheus.io/docs/introduction/overview/)

## Tasks
 - [x] Familiarize yourself with the Services and Software
 - [ ] [Setup Docker Cloud to monitor a GitHub repository](#Setup-Docker-Cloud-to-monitor-a-GitHub-repository)
 - [ ] [Configure Dockerfile and build Docker image](#Configure-Dockerfile-and-build-Docker-image)
 - [ ] [Use Docker Cloud to perform Unit Tests](#Use-Docker-Cloud-to-perform-Unit-Tests)
 - [ ] [Automate web server builds with Ansible](#Automate-web-server-builds-with-Ansible)
 - [ ] [Monitor web servers with Prometheus](#Monitor-web-servers-with-Prometheus)

### Detailed tasks
#### Setup Docker Cloud to monitor a GitHub repository
Docker Cloud enhances Continuous Integration and Continuous Deployment (CI/CD) by allowing developers to easily and quickly create code for testing on any number of platforms.  Operating System images of any configuration can be configured, created, destroyed and then re-created in a repeatable manner, and in short order.  Together with GitHub, re-creation is as simple as pushing to your remote repository and waiting for the results.  Let's set it up:
1. Connect Docker Cloud to github
    - Under username, click Settings
    - In the Source providers section click the plug icon next to GitHub and fill in your GitHub username
    - Go to Settings -> Authorized Applications in GitHub and approve Docker Cloud Builder
2. Create Docker Cloud repository
    - Click the plus sign in the top bar
    - For repository name, use the same name as your github repo (probably not required, but why cause confusion)
    - Click Create at the bottom of the page
3. Configure Repository to monitor github master branch
    - Click Repositories then select your new repo
    - Click Builds then the Configure Automated Builds box
    - In the Select Organization block click on your GitHub username
    - In the Select Repository block be sure to click the new repo you made in GitHub
4. Configure Builds for specific *tags* from github
    - In the AUTOTEST section click the Internal Pull Requests radio button
    - Click the plus sign next to BUILD RULES.  A new line appears.
    - Change Branch to Tag, enter this regular expression in the Source block:  `/^[0-9.]+$/`
    - Enter this in the Docker Tag block:  `release-{sourceref}`
    - At the bottom of the page click the Save box

#### Configure Dockerfile and build Docker image
Now that GitHub and Docker Cloud are linked, it's time to build the image which will run in a Docker virtual machine on an Amazon Web Services server.  Sound complicated?  It is, but we can write a recipe to make it simple, and more importantly, repeatable.  That recipe is the Dockerfile.  Its job is to specify a) the base image to start with (plain Ununtu linux), b) the software we need to run your website (Python / Flask / Prometheus), and c) the files we'll serve up to the Internet (Python / html).  Later, we'll load two images based on the tags we setup earlier, one for the production web server and one for the staging web server.

```Dockerfile
 # (a)  Base image to use
 FROM ubuntu:xenial 

 # Update the package cache so we get the newest software
 RUN apt-get update
 RUN apt-get install -y apt-utils
 
 # (b)  Because of the multitude of dependencies,
 # these one package will get us all the software we need
 RUN apt-get install -y python3-pip

 # (b)  Upgrade the Python installer and install the web server and monitoring software
 RUN pip3 install --upgrade pip
 RUN pip3 install flask prometheus_client

 # (c)  Copy all of the files in your GitHub repository to a directory on the Docker image:
 #      (Ansible playbook / website pages / prometheus files)
 WORKDIR /src
 COPY . /src

 # Open the port that Flask serves pages from
 EXPOSE 5000
```

Now, since Docker Cloud is monitoring your GitHub repository, all you need to do in order to build your image is push your Dockerfile to GitHub, do a Pull Request and the build starts automatically.  GitHub tells you tests are being performed. The build process can be monitored on Docker Cloud in the Builds section.

#### Use Docker Cloud to perform Unit Tests
A major benefit to using Docker Cloud to build images is its ability to perform Unit Testing.    
Once you're satisfied with your server and you've begun building your website, it would be nice to know if it's broken before you go through the whole deployment process.  Units Tests are very small scripts that check for expected conditions, e.g., whether the server is running and returning html.  The way it can tell this is happening is if certain expected text is returned in the server's response, which should be in the html, but could be an error message.  This is especially likely when running a Web Application rather than just serving up static html pages.    
The process is simple:    
1. Create a `docker-compose.test.yml` file.  This is the main engine for the Docker Cloud tests.  It can be very complex and perform many functions, but all we need it to do is run a bash script:
```yaml
sut:
  build: .
  command: ./run_tests.sh
```
2. That `run_tests.sh` bash script is simple as well.  All we need it to do is start the Unit Tests main function which is written in Python:
```bash
#!/bin/bash
echo "Running Flask Unit Tests"
python3 project_unitTests.py
```
3. Here's where the fun begins.  In `project_unitTests.py`, the `unittest` package starts the Flask webserver in the `setUp()` function.  We don't need to use the `tearDown()` function, but it needs to be defined so that the `unittest` package can perform testing.  Also required is any number of functions that start with "test_".  Here, we are only performing one:    
`test_home_page()` retrieves the homepage ('/') and tests the returned text for the phrase "Hello, World!"  If the test passes then you know the Flask webserver can start, and that your homepage is available.   
Remember, the Unit Tests only run when Docker Cloud is building the image, so when you finally deploy the server, Flask will need to be started in another manner which we will cover shortly.
```python
import unittest
import projectWeb

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.app = projectWeb.app.test_client()

    def tearDown(self):
        pass

    def test_home_page(self):
        response = self.app.get('/')
        assert b'Hello, World!' in response.data

if __name__ == '__main__':
    unittest.main()
```

#### Automate web server builds with Ansible
Ansible is software that can be setup to automate almost anything.  We're going to use it on your AWS server to install Docker, pull the Docker image from Docker Cloud, and start the web servers (one for the production website, and one for the staging website).  This also seems simple enough, right?  On the surface it's not at all, because of all the files and folders, but really, Ansible simply runs a script, called a playbook, which calls dependent scripts to perform tasks.  The first step is to log in to your AWS server, as all of the following steps will be performed from there.

##### Install Docker
This is the more daunting of the two main tasks, but only because the installation of Docker requires a fair amount of steps:    
The starting script is `configure-host.yml`.  It is started with the command `ansible-playbook ansible/configure-host.yml`. It starts the docker role from the `main.yml` script which installs docker, adds your username to the Linux 'docker' group, then makes sure the service is running.    
docker role `main.yml`:
```yaml
---
# Include a series of tasks for setting up a docker service

- include: install.yml
- include: user.yml
- include: service.yml
```
1. The first step in docker `main.yml` script calls `install.yml` which simply installs Docker.  The installation steps follow the instructions from the Docker website, noted in the first comment in the `install.yml` script below:
```yaml
---
# Install the docker service
# This task follows the install directions found here:
# https://docs.docker.com/engine/installation/linux/ubuntu/
- name: install docker dependencies
  apt:
    pkg: '{{ item }}'
    update_cache: yes
    cache_valid_time: 1800
  with_items:
    - apt-transport-https
    - ca-certificates 
    - curl
    - software-properties-common

# Add docker's GPG key
# http://docs.ansible.com/ansible/apt_key_module.html
- name: Setup docker repository key
  apt_key:
    id: 0EBFCD88
    url: https://download.docker.com/linux/ubuntu/gpg
    state: present
  notify: apt-get update

# This command runs on the server to determine what version of ubuntu is running
# The command's output to `lsb_release -c -s` is saved in `release` and
# available for the next step.
- name: Get release
  command: lsb_release -c -s
  register: release

# Here we add docker's repository to allow the system to do an apt-get install of
# official docker packages.
# http://docs.ansible.com/ansible/apt_repository_module.html
- name: Add docker repo
  apt_repository:
    repo: deb [arch=amd64] https://download.docker.com/linux/ubuntu {{ release.stdout }} stable
    state: present
    filename: docker
  notify: apt-get update

# Install the docker service.
# http://docs.ansible.com/ansible/apt_module.html
- name: Install the latest version of docker community edition
  apt:
    pkg: docker-ce
    update_cache: yes
    cache_valid_time: 1800
```
2. The second step in docker `main.yml` script calls `user.yml` which adds your username to the Linux 'docker' group.  This allows you control Docker which requires root privileges for most operations.  We'll cover the use of variables in the 'Deploy websites' section below.
```yaml
---
# Make it a little easier for you by adding your
# username to the docker linux group on this host.
# Hints:
#   http://docs.ansible.com/ansible/user_module.html
#   A variable is being used here
- name: Adding user to group docker
  user:
    name: "{{ student_name }}"
    group: docker
    append: yes
```
3. The third step in the docker `main.yml` script calls `service.yml` which runs a script that tests whether the docker service is running.  If it isn't, you won't be able to pull the staging or production website images from Docker Hub.
```yaml
---
# This should ensure that the docker service is running.
# See the following for usage hints:
# http://docs.ansible.com/ansible/service_module.html
- name: Ensure docker service is started
  service:
    name: docker
    state: started
```

##### Deploy websites
Now that the Docker service is installed and running, it's time to pull the Docker images from Docker Hub.  There is only one Ansible 'role' used for pulling and starting the images, but it can used to start any number of images by using variables which are contained in the main playbook.  Below are two examples.  With descptive variables, it is easy to tell which release (GitHub tag) correlates to which server, the ports each will run on, and the role this Ansible playbook will start.    
`deploy-website-staging.yml`:
```yaml
---
- name: Deploy the staging version of your website based on the newest tag of your docker-cloud-test image
  hosts: localhost
  become: true
  vars:
    projectWeb_environment: staging
    projectWeb_image_version: release-0.1.2
    projectWeb_host_port: 8081
    projectWeb_container_port: 5000
  roles:
    - projectWeb
```
and `deploy-website-production.yml`:
```yaml
---
- name: Deploy the production version of your website based on the previous tag of your docker-cloud-test image
  hosts: localhost
  become: true
  vars:
    projectWeb_environment: production
    projectWeb_image_version: release-0.0.5
    projectWeb_host_port: 8080
    projectWeb_container_port: 5000
  roles:
    - projectWeb
```
Each playbook calls the projectWeb `main.yml` script which ensures the Docker service is running on your AWS server, starts the docker image (called a 'container' when it is instantiated), then verifies the server is running by pulling the homepage and checking for a '200' status code which means the page was served and received.    
projectWeb role `main.yml`:
```yaml
---
# The following python package is required for ansible to interact with
# the docker service to manage docker containers.
- name: Ensure python docker-py package is installed
  pip:
    name: docker-py

# When running a playbook, this step can take a while the first time 
# on a new image since it will be doing a `docker pull` in the background.
# You don't need to make any modifications here, but you'll need to
# read a bit on how variable precedence works with ansible
# http://docs.ansible.com/ansible/playbooks_variables.html#variable-precedence-where-should-i-put-a-variable
# http://docs.ansible.com/ansible/docker_container_module.html
- name: Start/Restart the projectWeb container
  docker_container:
    name: "projectWeb-{{ projectWeb_environment }}"
    image: "{{ projectWeb_image }}:{{ projectWeb_image_version }}"
    command: "{{ projectWeb_command }}"
    state: started
    ports:
     - "{{ projectWeb_host_port }}:{{ projectWeb_container_port }}"    

# This should check that the container that is started in the last step
# is up and running by checking the localhost's webpage.
# Determine how to format the url used for the check.
# Hints:
#   A variable should be used in the url
#   http://docs.ansible.com/ansible/uri_module.html
- name: verify that webserver is running
  uri:
    url: http://{{ my_AWS_IP }}:{{ projectWeb_host_port }}
    method: GET
    status_code: 200
```
Just as in the main Ansible playbooks above, you may want to set variables for some of the above steps to start the web server as your needs may change based on the repository, website filenames and your AWS ip address.    
The variable filenames in the vars directory correspond to their task scripts(*task* yml and *vars* yml are both named `main.yml`).
```yaml
---
# Here we define variables in a key: value setting
# that will be used in the projectWeb role.
projectWeb_image: fml2001/unh698project
projectWeb_command: python3 /src/projectWeb.py
my_AWS_IP: 54.183.17.xxx
```

#### Monitor web servers with Prometheus
