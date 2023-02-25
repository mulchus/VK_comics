In english | [По-русски](../README.md)

# Script for publishing comics in the VKontakte community
Publishes a random comic from the site `https://xkcd.com /`


### How to use?
Python3 should already be installed.

Then use pip (or pip3, there is a conflict with Python2) to install dependencies.
Open the command line with the Win+R keys and enter:
```commandline
pip install -r requirements.txt
```
It is recommended to use virtualenv/venv to isolate the project.
(https://docs.python.org/3/library/venv.html)



### Setting environment variables

Before starting, you need to create a ".env" file in the PATH_FOLDER_WITH_SCRIPT\
and configure the environment variables by writing in it:
```
VK_ACCESS_TOKEN=Your token in VK
```
instructions on Implicit Flow for obtaining the access key of the VK user
```
https://vk.com/dev/implicit_flow_user
```

```
VK_GROUP_ID=ID of the VK community you created
```
is recorded in the settings ("Management") community (only numbers are needed)


### How to use?

Command to run a script to place a random comic in the VK:
```commandline
python main.py
```

### Project Goals
This code was written for educational purposes as part of an online course for web developers at [dvmn.org](https://dvmn.org/).
