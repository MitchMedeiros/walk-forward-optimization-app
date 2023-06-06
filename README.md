<h1>App Description &nbsp;&nbsp;
 <a href="https://pypi.org/project/vectorbt" alt="Python Versions">
 <img src="https://img.shields.io/pypi/pyversions/vectorbt.svg?logo=python&logoColor=white">
 </a>
</h1>

<h1>Core Dependencies</h1>

The core dependencies are:

<ol>
 <li>A compatible Python version (3.6-3.10)</li>
 <li>TA-Lib (C library)</li>
 <li>Python libraries in requirements.txt</li>
</ol>

<h2>Cloning This Repository</h2>


To run this app locally you can simply clone this repository. Make sure you have
<a href="https://git-scm.com/book/en/v2/Getting-Started-Installing-Git">
git installed</a>.
You can confirm this on Linux or Mac by typing `git --version` in a terminal. Navigate to the directory you want the app in and use the command:

```shell
git clone https://github.com/MitchMedeiros/dashapp.git
```

<h2>Creating the Virtual Environment</h2>

If you have Anaconda installed you can create a virtual environment called "backtesting" using:

```shell
conda create -n backtesting python=3.10
```

and activate it with `conda activate backtesting`. Note what default directory it's installed in if you plan to web host the app.

Alternately, you can use the Python venv module with the following command in the directory you want the environment in:

```shell
python3.10 -m venv backtesting
```

Activate it on Linux/Mac using: `source backtesting/bin/activate` or in Windows PowerShell: `backtesting\Scripts\activate`.

<h2>TA-Lib</h2>

At this point you should install the core TA-Lib library from source before you can install the TA-Lib Python library. This is necessary since the Python library is only a wrapper.

<h3>Ta-Lib Installation on Linux and Mac</h3>

If you have a web browser available you can download the source file by visiting <a href="https://sourceforge.net/projects/ta-lib/files/ta-lib/0.4.0/ta-lib-0.4.0-src.tar.gz/download?use_mirror=phoenixnap">soureforge</a>.

If using a Linux server, install wget if not already installed, using the appropriate 
<a href="https://www.maketecheasier.com/install-software-in-various-linux-distros/">
install command</a> 
for your Linux distro.

For Debian/Ubuntu:

```shell
sudo apt install wget
```

Download the TA-Lib library from 
<a href="https://sourceforge.net/projects/ta-lib/files/ta-lib/0.4.0/">
 SourceForge
</a>
using 

```shell
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
```

Once you have the tar file downloaded you should unpack it:

```shell
tar -xvf ta-lib-0.4.0-src.tar.gz
```

Delete the tar file and cd into the newly created folder.

```shell
rm ta-lib-0.4.0-src.tar.gz; cd ta-lib
```

Now we run the configure file on Debian/Ubuntu you should use the prefix /usr:

```shell
./configure --prefix=/usr
```

On Mac the prefix /usr/local should be used:
```shell
./configure --prefix=/usr/local
```

Run the `make` command to compile the TA-Lib files.\
Run `sudo make install`, which will copy the compiled files into /usr/include/ta-lib.

<h2>requirements.txt</h2>

After you've installed the core TA-Lib library, activate your virutal environment and navigate inside the app directory. Install the libraries in requirements.txt with pip:

```shell
pip3 install -r requirements.txt
```

You can now run the main.py file and visit <a href=127.0.0.1:8050>127.0.0.1:8050</a> in a web browser to access the app.

<h2>Optional Dependencies</h2>

The optional dependencies to extend the functionality of this app are:

<ol>
 <li>PostgreSQL database - for custom data</li>
 <li>Redis database - for faster caching</li>
 <li>mod_wsgi - for web hosting</li>
 <li>Apache HTTP - for web hosting</li>
</ol>

<h3>PostgreSQL and Redis Databases</h3>

The app hosted on <a ahref=backtest.fi>backtest.fi</a> utilizes a postgreSQL and Redis backend. However, the default configuration file when cloning this repository will use Yahoo Finance for data as well as the local file system for caching between Dash callbacks. If you have either or both databases installed you can connect them by simply providing your connection credentials in config.py, located in the parent directory of this repository.

<h3>WSGI Setup for an Apache Server on Linux</h3>

This section explains how to web host the app on a server. It assumes you have an Apache virtual host set up and linked to a domain name.

You should first install the Apache header files for third-party modules. If you have Apache 2.4 then on Debian/Ubuntu run:

```shell
sudo apt install apache2-dev
```

Now, with your Python virtual environment active:

```shell
pip3 install mod-wsgi
```

Locate your newly created wsgi files with:

```shell
mod_wsgi-express module-config
```

and copy the output. Now create a new .load file in your /etc/apache2/mods-available directory and paste that output inside it

```shell
vim /etc/apache2/mods-available/wsgi.load
```

(If you're new to VIM press `i` to insert text, paste like normal, press `escape`, then `:wq` to save changes and exit. If you make a mistake press `escape` then `:q!` to exit without saving changes or creating a new file.)

Enable the new mod with `a2enmod wsgi`.

Navigate to the .config or .htaccess file (depending on your OS) that you have your virtual host information in. You'll need to add a `WSGIScriptAlias` specifying the location of the app.wsgi file.

If your site is only using HTTP, your virtual host info should look similar to the snippet below. Make sure to replace /path_to_cloned_repository with the appropriate path and yoursite.com with your domain name.

```apache
<VirtualHost *:80>
    ServerName yoursite.com
    ServerAlias www.yoursite.com

    WSGIDaemonProcess dashapp python-home=your_python_virtual_env_directory user=www-data group=www-data

    WSGIProcessGroup dashapp
    WSGIApplicationGroup %{GLOBAL}

    WSGIScriptAlias / /path_to_cloned_repository/dashapp/app.wsgi

    <Directory /path_to_cloned_repository/dashapp/>
        Require all granted
    </Directory>
</VirtualHost>
```

If your site is set up to use HTTPS via Let's Encrypt then your .config or .htaccess file should look like 

```apache
<VirtualHost *:80>
    ServerName yoursite.com
    ServerAlias www.yoursite.com

    RewriteEngine on
    RewriteCond %{HTTPS} off
    RewriteRule ^(.*)$ https://yoursite.com/$1 [L,R=301]
</VirtualHost>

<IfModule mod_ssl.c>
<VirtualHost *:443>
    ServerName yoursite.com
    ServerAlias www.yoursite.com

    Include /etc/letsencrypt/options-ssl-apache.conf
    SSLCertificateFile /etc/letsencrypt/live/yoursite.com/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/yoursite.com/privkey.pem

    WSGIDaemonProcess dashapp python-home=/path_to_your_virtual_environment user=www-data group=www-data

    WSGIProcessGroup dashapp
    WSGIApplicationGroup %{GLOBAL}

    WSGIScriptAlias / /path_to_cloned_repository/dashapp/app.wsgi

    <Directory /path_to_cloned_repository/dashapp/>
        Require all granted
    </Directory>
</VirtualHost>
</IfModule>
```

If you've created a new .config file in one of your ...-available folders rather than adding to an existing file then you'll also need to activate it with the appropriate `a2ensite`, `a2enmod`, or `a2enconf` command.

Now you will need to edit the app.wsgi file in the root directory of the repository. First change the shebang line at the top of the file to the location of your virtual environment and Python version:
```python
#!/path_to_your_virtual_environment/bin/python3.10
```
Also changing the sys.path line shown below to the appropriate root directory for your app

```python
sys.path.insert(0,"/path_to_cloned_repository/dashapp/")
```

Finally, insure that the Apache user: www-data has sufficient file permissions. At a minimum the entire app directory should have the group as www-data with read permissions on all files and also execute permission for app.wsgi. You should add further write or execute permissions to files only as necessary. For security reasons, the directory should be owned by a user other than root.

Restart Apache: `systemctl restart apache2` for all changes to take effect. The app should now be accessible through your domain name!
