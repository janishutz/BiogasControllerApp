<div id="title" align="center">
    <img src="./BiogasControllerAppLogo.png" width="300">
    <h1>BiogasControllerApp</h1>
</div>

<div id="badges" align="center">
    <img src="https://img.shields.io/github/license/janishutz/BiogasControllerApp.svg">
    <img src="https://img.shields.io/github/repo-size/janishutz/BiogasControllerApp.svg">
    <img src="https://img.shields.io/github/languages/top/janishutz/BiogasControllerApp">
    <img src="https://img.shields.io/github/directory-file-count/janishutz/BiogasControllerApp.svg">
    <br>
    <img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/janishutz/BiogasControllerApp">
    <img alt="GitHub watchers" src="https://img.shields.io/github/watchers/janishutz/BiogasControllerApp">
    <img src="https://img.shields.io/github/issues-pr-raw/janishutz/BiogasControllerApp">
    <img alt="GitHub forks" src="https://img.shields.io/github/forks/janishutz/BiogasControllerApp">
    <img alt="GitHub commit activity" src="https://img.shields.io/github/commit-activity/m/janishutz/BiogasControllerApp">
    <br>
    <img alt="GitHub downloads all releases" src="https://img.shields.io/github/downloads/janishutz/BiogasControllerApp/total?label=Downloads (total)">
    <img alt="GitHub downloads release (latest release)" src="https://img.shields.io/github/downloads/janishutz/BiogasControllerApp/latest/total?label=Downloads (latest)">
    <img src="https://img.shields.io/github/release/janishutz/BiogasControllerApp.svg">
</div>

<div id="donate" align="center">
    <a href="https://store.janishutz.com/donate" target="_blank"><img src="https://store-cdn.janishutz.com/static/support-me.jpg" width="150px"></a>
</div>

BiogasControllerApp has just received a major rewrite, where I focused on code-readability, documentation and stability. The documentation in the code is aimed at beginners and does contain some unnecessary extra comments

If you are here to read the code, the files you are most likely looking for can be found in the `lib` folder. If you want to understand and have a look at all of the application, start with the `biogascontrollerapp.py` file

# Installation
To install it, navigate to the releases tab on the right hand side. Click the current release, scroll down to assets and select the version appropriate for your operating system.

That means:
- on Windows, select BiogasControllerApp-Windows.zip
- on Linux, you may download the tarball or you may also download the `install-linux.sh` script to automatically install it for you. Just note: You need to enable execute permissions for the file!

Compared to older versions, the new BiogasControllerApp doesn't install itself as an app and only resides in a folder where you can launch it using the executable or the `launch.sh` script.

## Troubleshooting
If you get a warning from Windows, the reason for this is that this app bundle is unsigned (since a signing certificate is about USD 350/year), so it might warn you about that. You can safely click "Run anyway" or the like to bypass that problem. 

If this makes you uncomfortable, you may simply install python and install the necessary dependencies (see below) and run the app using Python.

# Features
- Read data the microcontroller in ENATECH sends
- Configure the microcontroller (Coefficients & Temperature). Old settings will be pre-loaded
- Focus on code quality and readability as well as stability
- Tips to resolve errors directly in the app
- The app is still maintained and as such known issues will be resolved
- Clean UI focusing on ease of use
- Documented code so you can more easily understand what is happening

# Issues
If you encounter any bugs or other weird behaviour, please open an issue on this GitHub repository, contact me on my [support page](https://support.janishutz.com) or send me an [email](mailto:development@janishutz.com)

# Documentation
You may find documentation for this project in its wiki here on GitHub. The code is also documented with explanations what it does

# Officially Supported OS
- Microsoft Windows 10, 11 (through the provided compiled package, might work on older versions as well)
- Microsoft Windows XP, Vista, 7, 8, 10, 11 (through running the package with Python yourself)
- GNU/Linux: All distros that support Python 3.8 or later (use `install-linux.sh` to install and `launch.sh` to launch for convenience)
- FreeBSD: If you have Pyhton 3.8 or later installed 

## Dependencies
Only needed if you run with python directly
- Python 3.10 - latest (only tested on this version, but should work down to at least 3.8)
- kivy[base]==2.3.1
- kivymd==1.1.1
- pyserial==3.5

To install them, run `pip install -r requirements.txt`

# Contributing
If you wish to contribute to this project, please fork this repository, create a new branch in your fork, make your changes and open a pull request in this repo. 


<div id="donate" align="center">
    <a href="https://store.janishutz.com/donate" target="_blank"><img src="https://store-cdn.janishutz.com/static/support-me.jpg" width="150px"></a>
</div>
