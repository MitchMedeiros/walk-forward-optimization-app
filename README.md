Vectorbt will install most of the neccisarry libraries for you such as numba, numpy, pandas, plotly, etc. However, the TA-Lib python compatability library cannot be installed until the original TA-Lib library it depends upon is manually installed. For Linux see the steps below. It's currently also possible on M1 Mac; you'll need to use Homebrew.

Ta-lib installation for Linux:
Open the command line and perform the following actions.
Install wget if you don't have it using the appropriate install command for your linux distrubtion. For Debian based distros:

sudo get install wget

Now download the ta-lib library from the web

wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz

unzip the tar file

tar -xvf ta-lib-0.4.0-src.tar.gz

cd into the newly created folder and run the configure file. (Note that if you're Linux distro doesn't use the /usr/include directory for storing header files for C compilers you'll need to change the below prefix to the approptiate directory.)

cd ta-lib; ./configure --prefix=/usr

Now run the make command to compile everything

make

and finally using make install will copy the compiled files into /usr/include/ta-lib

sudo make install

From here you can pip install vectorbt and it will install the ta-lib python library and all other vectorbt dependencies for you. For the latest version of vectorbt you should have 3.6 =< Python < 3.11.
pip install -U vectorbt

WSGI Server setup for apache2:
If you want to host the app online you'll need to use the app.wsgi file in the root directory of this repository as well as follow the steps outlined below to setup your server. 

Install the wsgi library for python

pip install mod-wsgi

Now print the path for for the newly created wsgi files with the command