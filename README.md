# Initial Setup 
TA-Lib is used in this app and requires a manual installation if you want to recreate the app yourself.

The TA-Lib Python library merely serves as a compatibility layer for the original TA-Lib library, which must be installed before running `pip install ta-lib`. For Linux see the steps below. For Mac a similar procedure can be followed see [installing TA-Lib without Homebrew](https://medium.com/@mkstz/install-ta-lib-without-homebrew-61f57a63c06d).

## Ta-Lib Installation for Linux:

Install *wget* if you don't already have it, using the appropriate [install command](https://www.maketecheasier.com/install-software-in-various-linux-distros/) for your Linux distro. **For Debian/Ubuntu:**

```shell
sudo apt-get install wget
```

Download the TA-Lib library from [SourceForge](https://sourceforge.net/projects/ta-lib/files/ta-lib/0.4.0/)

```shell
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
```

Unzip the tar file

```shell
tar -xvf ta-lib-0.4.0-src.tar.gz
```

Delete the tar file, cd into the new folder, and run the configure file inside

```
rm ta-lib-0.4.0-src.tar.gz; cd ta-lib; ./configure --prefix=/usr
```

Run the `make` command to compile the TA-Lib files.\
Now run `sudo make install`, which will copy the compiled files into */usr/include/ta-lib*.

You should now be able to install vectorbt and all other dependencies without any issues

```shell
pip3 install -r requirements.txt
```
If this generates errors still then confirm that your Linux distro stores header files in a subdirectory of /usr. If not, change `./configure --prefix=/appropriate_directory` in the earlier step.

## WSGI Server Setup for Apache 2:
To host this app online you'll need to edit the path in the app.wsgi file to the appropriate directory for your app. Additionally, follow the steps outlined below to setup your server: 

Install the wsgi Python library

```shell
pip3 install mod-wsgi
```

Print the path for the newly created wsgi files with the command
