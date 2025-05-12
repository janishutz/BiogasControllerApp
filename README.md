<div id="title" align="center">
    <img src="./BiogasControllerApp-V2.3/BiogasControllerAppLogo.png" width="300">
    <h1>BiogasControllerApp</h1>
</div>

<div id="badges" align="center">
    <img src="https://img.shields.io/github/license/janishutz/BiogasControllerApp.svg">
    <img src="https://img.shields.io/github/repo-size/janishutz/BiogasControllerApp.svg">
    <img src="https://img.shields.io/tokei/lines/github/janishutz/BiogasControllerApp">
    <img src="https://img.shields.io/github/languages/top/janishutz/BiogasControllerApp">
    <img src="https://img.shields.io/github/directory-file-count/janishutz/BiogasControllerApp.svg">
    <br>
    <img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/janishutz/BiogasControllerApp">
    <img alt="GitHub watchers" src="https://img.shields.io/github/watchers/janishutz/BiogasControllerApp">
    <img src="https://img.shields.io/github/issues-pr-raw/janishutz/BiogasControllerApp">
    <img alt="GitHub forks" src="https://img.shields.io/github/forks/janishutz/BiogasControllerApp">
    <img alt="GitHub commit activity" src="https://img.shields.io/github/commit-activity/m/janishutz/BiogasControllerApp">
    <br>
    <img alt="GitHub all releases" src="https://img.shields.io/github/downloads/janishutz/BiogasControllerApp/total?label=Downloads (total)">
    <img alt="GitHub release (latest by date)" src="https://img.shields.io/github/downloads/janishutz/BiogasControllerApp/latest/total?label=Downloads (latest)">
    <img src="https://img.shields.io/github/release/janishutz/BiogasControllerApp.svg">
    <img src="https://img.shields.io/github/package-json/v/janishutz/BiogasControllerApp.svg?label=Development Version">
</div>

<div id="donate" align="center">
    <a href="https://store.janishutz.com/donate" target="_blank"><img src="https://store-cdn.janishutz.com/static/support-me.jpg" width="150px"></a>
</div>

BiogasControllerApp has just received a major rewrite, where I focused on code-readability, documentation and stability. The documentation in the code is aimed at beginners and does contain some unnecessary extra comments

If you are here to read the code, the files you are most likely looking for can be found in the `biogascontrollerapp/lib` folder. If you want to understand and have a look at all of the application, start with the `biogascontrollerapp.py` file in the `biogascontrollerapp` folder

# Features
- Read data the microcontroller in ENATECH sends
- Configure the microcontroller (Coefficients & Temperature). Old settings will be pre-loaded
- Focus on code quality and readability as well as stability
- Tips to resolve errors directly in the app
- The app is still maintained and as such known issues will be resolved
- Installer for Windows, deb, rpm and arch package available
- Clean UI focusing on ease of use
- Documented code so you can more easily understand what is happening


# Issues
If you encounter any bugs or other weird behaviour, please open an issue on this GitHub repository. 

# Documentation
You may find documentation for this project in its wiki here on GitHub. The code is also documented with explanations what it does

# Officially Supported OS
- Microsoft Windows 10, 11 (through my installer, may though support older Versions but this is not verified. Open an issue if you have managed to run it on an older version of Windows)
- Microsoft Windows XP, Vista, 7, 8, 10, 11 (through running the package with Python yourself)
- MacOS 10.9 (Mavericks) or later (required by Python)
- GNU/Linux: All distros that support Python 3.8 or later
- FreeBSD: If you have Pyhton 3.8 or later installed 

## Dependencies
Only needed if you run with python directly
- Python 3.10 - 3.12 (only tested on this version, but should work down to at least 3.8 and with the latest versions)
- kivy
- pyserial

To install them, run `pip install -r requirements.txt`

# Contributing
If you wish to contribute to this project, please fork this repository, create a new branch in your fork, make your changes and open a pull request in this repo. 


<div id="donate" align="center">
    <a href="https://store.janishutz.com/donate" target="_blank"><img src="https://store-cdn.janishutz.com/static/support-me.jpg" width="150px"></a>
</div>
