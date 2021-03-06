echo "Starting deploy script"
echo $env:PYTHON_VERSION
echo $env:PYTHON_ARCH
if ($env:PYTHON_VERSION -eq "3.4.x" -and $env:PYTHON_ARCH -eq "32") {
  pip install pyinstaller
  npm install -g bower
  git clone https://github.com/OpServ-Monitoring/opserv-frontend.git app/server/static_hosting/public
  cd app/server/static_hosting/public
  bower install
  cd ..
  cd ..
  cd .. # we are now in app folder
  ls
  pyinstaller main.py -D --hiddenimport=psutil --hiddenimport=clr --hiddenimport=cpuinfo --hiddenimport=pyspectator --add-data "extern_dependency/*;extern_dependency/" --add-data "server/static_hosting/public;server/static_hosting/public"
  cd ..
  cp appveyor/main.exe.config app/dist/main/main.exe.config
  7z a -tzip opserv-win-build.zip app/dist/main/*
} ELSE {
    ECHO "Skipping build, only 3.4.x builds are going to be deployed"
}