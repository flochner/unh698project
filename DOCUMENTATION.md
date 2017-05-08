# Deploying and Monitoring a Website

#### Services
 - GitHub
 - Docker Cloud
 - Amazon Web Services

#### Software
 - Docker
 - Python
 - Flask
 - Ansible
 - Prometheus

## Tasks
 - [ ] Setup Docker Cloud to monitor a GitHub repository
 - [ ] Configure Dockerfile 
 - [ ] 

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
    - Change Branch to Tag, enter this regular expression in the Source block:  */^[0-9.]+$/*
    - Enter this in the Docker Tag block:  *release-{sourceref}*
    - At the bottom of the page click the Save box

#### Configure Dockerfile
Now that GitHub and Docker Cloud are linked, it's time to build the image which will run in a Docker virtual machine on an Amazon Web Services server.  Sound complicated?  It is, but we can write a recipe to make it simple, but more importantly, repeatable.  That recipe is the Dockerfile.  Its job is to specify a) the base image to start with (plain Ununtu linux), b) the software we need to run our website (Python / Flask / Prometheus), and c) the files we'll serve up to the Internet (Python / html).

```Dockerfile
 FROM ubuntu:xenial 

 ENV DEBIAN_FRONTEND=noninteractive

 RUN apt-get update
 RUN apt-get install -y apt-utils
 
 RUN apt-get install -y \
    build-essential \
    python3-pip

 RUN pip3 install --upgrade pip
 RUN pip3 install flask prometheus_client

 ENV DEBIAN_FRONTEND=teletype

 WORKDIR /src
 COPY . /src

 EXPOSE 5000
```

