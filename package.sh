#!/bin/sh

# packaging script
rm -rf ./build/
rm -rf ./dist/

# build windows package
wine pyinstaller BiogasControllerApp.spec

if [ $? -ne 0 ]; then
    echo -e "\nBuild unsuccessful, aborting..."
    exit 1
fi

# Build successful
cp -r ./gui ./dist
cp -r ./lib ./dist
cp ./biogascontrollerapp.py ./dist/
cp ./BiogasControllerAppLogo.png ./dist/
cp ./changelog ./dist/
cp ./config.ini ./dist/
cp ./README.md ./dist/
cp ./requirements.txt ./dist/
cp ./SECURITY.md ./dist/

# Remove build directories
rm -rf ./build/

rm -rf ./dist/biogascontrollerapp/


# Create Windows archive (zip)
zip -9r BiogasControllerApp-Windows.zip ./dist

# Create Linux archive (tar)
rm ./dist/BiogasControllerApp.exe
cp ./install-linux.sh ./dist/
cp ./launch.sh ./dist/

ouch compress -y ./dist/ biogascontrollerapp-linux.tar.gz

rm -rf ./dist

echo "Done!"
