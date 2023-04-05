<h1>App Description and Preview</h1>

<h2>Dependencies &nbsp;
    <a href="https://pypi.org/project/vectorbt" alt="Python Versions">
        <img src="https://img.shields.io/pypi/pyversions/vectorbt.svg?logo=python&logoColor=white">
    </a>
</h2>

<ol>
    <li>It is assumed that you already have a compatible version of Python (listed above) and ideally a fresh virtual environment</li>
    <li>The C-based TA-Lib library</li>
    <li>The libraries in requirements.txt</li>
    <li>(optional) A CSV file or database containing market data</li>
    <li>(optional) A WSGI setup if web hosting the app</li>
</ol>

For a barebones installation you only need to install TA-Lib, clone this repository, and run pip3 install -r requirements.txt in your python environment. Detailed instruction for reproducing the full web app connected to a PostgreSQL/TimescaleDB database are provided below.

The TA-Lib Python library serves only as a compatibility layer for the original TA-Lib library based in C and this must be installed before running `pip install ta-lib`. For Linux, I've provided the steps below. For Mac, a fairly similar procedure can be followed: 
<a href="https://medium.com/@mkstz/install-ta-lib-without-homebrew-61f57a63c06d">
    Installing TA-Lib without Homebrew
</a>

<h2>Ta-Lib Installation on Linux</h2>

Install wget, if not already installed, using the appropriate 
<a href="https://www.maketecheasier.com/install-software-in-various-linux-distros/">
    install command
</a> 
for your Linux distro.\
For Debian/Ubuntu:

```shell
sudo apt-get install wget
```

Download the TA-Lib library from 
<a href="https://sourceforge.net/projects/ta-lib/files/ta-lib/0.4.0/">
    SourceForge
</a>
using 

```shell
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
```

Unpack the tar file

```shell
tar -xvf ta-lib-0.4.0-src.tar.gz
```

Delete the tar file, cd into the new folder, and run the configure file inside

```
rm ta-lib-0.4.0-src.tar.gz; cd ta-lib; ./configure --prefix=/usr
```

Run the `make` command to compile the TA-Lib files.\
Run `sudo make install`, which will copy the compiled files into /usr/include/ta-lib.

You should now be able to install vectorbt and all dependencies without any issues

```shell
pip3 install -r requirements.txt
```
If this generates errors about ta-lib then confirm that your Linux distro stores header files in a subdirectory of /usr. If not, change `./configure --prefix=/appropriate_directory` in the earlier step.

<h2>Importing Your Own Data</h2>

The dataframe used for the strategy simulation is created in make_df.py. Inside it you will find the Yahoo Finance API used to reduce the overhead of getting the app running. 

<h3>Importing from a CSV</h3>

You can easily use a CSV file instead by uncommenting the lines below ##For CSV## and specifying your CSV's directory and commenting out the yfinance lines.


<h3>Importing from a PostreSQL/TimescaleDB</h3>

You'll also find the code for this in make_df.py under ##For PostgreSQL/Timescale database##\
You'll need to install psycopg2 (see details below) then input your database information inside credentials.py and add the file to .getignore if you plan to share your repository. Note that you can use any database with this app that has a Python API but the process may vary.

<h4>Installing psycopg2</h4>

You should first check if you meet the 
<a href="https://www.psycopg.org/docs/install.html#install-from-source">
    build requirements 
</a> 
to install psycopg2. If so simply `pip install psycopg2` inside your python environment. If you experience issues the easiest workaround is to `pip uninstall psycopg2` and `pip install psycopg2-binary`. 

As a disclaimer, using psycopg2-binary is not recommended for production systems since it can create binary upgradeability issues. This is because psycopg2 is a compatibility library similar to TA-Lib, and psycopg2-binary installs the relevant C libraries and pre-compiled binary for you to make setup simple. However, these libraries won't be upgradeded by your system and can create conflicts.

Note that you can shortcut the cursor creation process for importing data with psycopg2 using the pandas function `pd.read_sql_query('''your query''', conn)`, however, this is officially untested for psycopg2.

<h2>WSGI Setup for an Apache Server</h2>

This section explains optionally how to web host the app on a server. It assumes you have an Apache server setup and linked to a domain name.

Even with Apache installed, you may be missing important files for WSGI. For Debian/Ubuntu run:

```shell
sudo apt-get install apache2-dev
```

Now with your python environment active 

```shell
pip install mod-wsgi
```

Locate your newly created wsgi files with

```shell
mod_wsgi-express module-config
```

and copy the output. Now create a new .load file in your /etc/apache2/mods-available directory and paste that output inside it

```shell
vim /etc/apache2/mods-available/wsgi.load
```

(If you're new to vim press `i` to insert text, paste like normal, press `escape`, then `:wq` to save changes and exit. If you make a mistake press `escape` then `:q!` to exit without saving changes or creating the new file.)

Enable the new mod with `a2enmod wsgi`.

Nagivate to the .config or .htaccess file (depending on your OS) that you have your virutal host information in. You'll need to add a `WSGIScriptAlias` specifying the location of the app.wsgi file in this repository.

If your site is only using http, your virtual host info should look similar to the below. If you have your site in a different directory from /var/www/ then change the root directory appropriately.

```apache
<VirtualHost *:80>
    ServerName yoursite.com
    ServerAlias www.yoursite.com
    WSGIScriptAlias / /var/www/yoursites_folder/dashapp/app.wsgi
    
    <Directory /var/www/yoursites_folder/dashapp/>
        Order allow,deny
        Allow from all
    </Directory>
</VirtualHost>
```

If your site is setup to use https via Let's Encrypt then your .htaccess or .config file should look something like 

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
    WSGIScriptAlias / /var/www/yoursites_folder/dashapp/app.wsgi

    <Directory /var/www/yoursites_folder/dashapp/>
        Order allow,deny
        Allow from all
    </Directory>
    
    Include /etc/letsencrypt/options-ssl-apache.conf
    SSLCertificateFile /etc/letsencrypt/live/yoursite.com/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/yoursite.com/privkey.pem
</VirtualHost>
</IfModule>
```

If you've created a new .config or .htaccess file in one of your ...-available folders rather than adding to an existing file then you'll also need to activate it with the appropriate `a2ensite`, `a2enmod`, or `a2enconf` command.

Finally, you should edit the app.wsgi file in this repository by changing the sys.path line shown below to the appropriate root directory for your app

```python
sys.path.insert(0,"/var/www/yoursites_folder/dashapp/")
```

Now restart Apache: `systemctl restart apache2` for all changes to take effect. The app should now be accessible through your domain name! 🤩
