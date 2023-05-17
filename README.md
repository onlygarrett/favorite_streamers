## *Favorite Streamers*

This basic python script that utilizing Twitch.tv's helix API to generate a simple list of a user's followed streamers with details.The purpose of this application was to let me mess around with python GUI's.

> There are 2 options for rendering the output because one of them I wanted to try out running a script through asyncio's subprocess library

#### The output of this file currently includes:

- The channel's name
- The current game or category that they are under 
- Their current amount of viewers

---

## Dependencies
This application mostly requires [nicegui](https://github.com/zauberzeug/nicegui/)'s gui frame work as well as a few other common libraries like `requests`

All libraries are in the `requirements.txt`

---

## Authentication Requirements
The main requirement that is needed for this script is **Client Id** and **Authorization Token**.

Both of these can be retrieved from [this handy token generator](https://twitchtokengenerator.com/) with the `user:read:follows` scope.

A **User Id** will also be prompted and can be grabbed from [another handy generator](https://www.streamweasels.com/tools/convert-twitch-username-to-user-id/) 

This script will prompt for re-entry of all these variables when running the script and be stored in a `config.ini` file.

---

## Usage

Simply clone this repo to your machine.

Create a virtualenv in the base directory, activate it, and install requirements with

```bash
virtualenv venv
source .venv/bin/activate
pip install -r requirements.txt
```
Once done just run the application with 
```bash
python3 application.py
```

### **Note: config.ini needs to have the following format to parse**
```code
[config]
accesstoken = xxxx
clientid = xxxxxx
userid = xxxx
```

---

I really have no other plans to update this. More of just me messing around with python gui's. Feel free to copy!
