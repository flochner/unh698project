# Deploying and Monitoring a Website

#### Services
 - Github
 - Docker Cloud
 - Amazon Web Services

#### Software
- Docker
- Python
- Flask
- Ansible
- Prometheus

## Tasks
- [ ] Setup DockerCloud to monitor github repository
- [ ] Configure Dockerfile 
- [ ] 
- [ ]

### Detailed tasks
#### Setup DockerCloud to monitor github repository
1. Connect Docker Cloud to github
    - Under username, click Settings
    - In the Source providers section click the plug next to GitHub and fill in your GitHub username
2. Create repository
    - Click the plus sign in the top bar
    - For repository name, use the same name as you github repo (probably not required, but why cause confusion)
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

