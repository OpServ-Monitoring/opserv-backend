echo "Starting deploy script"
echo $env:PYTHON_VERSION
echo $env:PYTHON_ARCH
if ($env:PYTHON_VERSION -eq "3.4.x" -and $env:PYTHON_ARCH -eq "32") {
  "%CMD_IN_ENV% pip install pyinstaller"
  npm install -g bower
  git clone https://github.com/OpServ-Monitoring/opserv-frontend.git app/server/static_hosting/public
  cd app/server/static_hosting/public
  bower install
  cd ..
  cd ..
  cd .. # we are now in app folder
  pyinstaller main.py --hiddenimport=psutil --hiddenimport=clr --hiddenimport=cpuinfo --hiddenimport=pyspectator --add-data "extern_dependency/*;extern_dependency/" --add-data "server/static_hosting/public;server/static_hosting/public"
  7z a -tzip opserv-win-build.zip dist/main/*
  ls -la
  cd ..
} ELSE {
    ECHO "Skipping build, only 3.4.4 builds are going to be deployed"
}