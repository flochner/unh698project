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
 - [ ] Familiarize yourself with the Services and Software.
 - [ ] Setup Docker Cloud to monitor a GitHub repository
 - [ ] Configure Dockerfile 
 - [ ] Build the docker image
 - [ ] Use Docker Cloud to perform Unit Tests
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
    - Change Branch to Tag, enter this regular expression in the Source block:  `/^[0-9.]+$/`
    - Enter this in the Docker Tag block:  `release-{sourceref}`
    - At the bottom of the page click the Save box

#### Configure Dockerfile
Now that GitHub and Docker Cloud are linked, it's time to build the image which will run in a Docker virtual machine on an Amazon Web Services server.  Sound complicated?  It is, but we can write a recipe to make it simple, but more importantly, repeatable.  That recipe is the Dockerfile.  Its job is to specify a) the base image to start with (plain Ununtu linux), b) the software we need to run our website (Python / Flask / Prometheus), and c) the files we'll serve up to the Internet (Python / html).

```Dockerfile
 # (a)  Base image to use
 FROM ubuntu:xenial 

 # Update the package cache so we get the newest software
 RUN apt-get update
 RUN apt-get install -y apt-utils
 
 # (b)  Because of the multitude of dependencies,
 # these two packages will get us all the software we need
 RUN apt-get install -y \
    build-essential \
    python3-pip

 # (b)  Upgrade the Python installer and install the web server and monitoring software
 RUN pip3 install --upgrade pip
 RUN pip3 install flask prometheus_client

 # (c)  Copy all of the files in our GitHub repository to a directory on the Docker image (Ansible playbook / website pages / prometheus files)
 WORKDIR /src
 COPY . /src

 # Open the port that Flask serves pages from
 EXPOSE 5000
```

#### Build the Docker image
build

#### Use Docker Cloud to perform Unit Tests
Docker can be run entirely in a local environement, from image building to running the image to hosting web pages, or anything else.  A major benefit to using Docker Cloud to build images is its ability to perform Unit Testing.    
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
Remember, the Unit Tests only run when Docker Cloud is building the image, so when you finally deploy the server, Flask will need to be started in another manner (which we will cover shortly).
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
