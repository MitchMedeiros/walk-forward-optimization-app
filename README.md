# Initial Setup 
TA-Lib is used in this project and requires additional setup for the app to work properly.
The TA-Lib Python library merely serves as a compatibility layer for the original TA-Lib library, which should be manually installed. For M1 Macs use *brew install*. For Linux see the steps below.

## Ta-Lib Installation for Linux:

Install *wget* if you don't already have it, using the appropriate install command for your Linux distro. **For Debian/Ubuntu:**

```shell
sudo apt-get install wget
```

Download the TA-Lib library from SourceForge

```shell
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
```

Unzip the tar file

```shell
tar -xvf ta-lib-0.4.0-src.tar.gz
```

Delete the tar file, cd into the new folder, and run the configure file inside. *(If your Linux distro doesn't use the /usr/include directory for storing header files, you'll need to change the below prefix to the appropriate directory.)*

```shell
rm ta-lib-0.4.0-src.tar.gz; cd ta-lib; ./configure --prefix=/usr
```

Run *make* to compile everything

```shell
make
```

Finally, run *make install* to copy the compiled files into */usr/include/ta-lib*.

```shell
sudo make install
```

From here you can *pip install vectorbt* to install the ta-lib python library and all other vectorbt dependencies for you. Make sure you have Python >=3.6, < 3.11.

```shell
pip3 install -U vectorbt
```

## WSGI Server Setup for Apache 2:
To host this app online you'll need to edit the path in the app.wsgi file to the appropriate directory for your app. Additionally, follow the steps outlined below to setup your server: 

Install the wsgi Python library

```shell
pip3 install mod-wsgi
```

Print the path for for the newly created wsgi files with the command
