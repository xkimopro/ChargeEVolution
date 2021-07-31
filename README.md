# Requirements

The following programms need to be downloaded to your device before starting the proccess of installing our project's material.

## Latest XAMPP update

It is used for building our site on a local web server on the computer.

## Latest python 3.9 update

Is the primary coding language used for the back-end development.

## React 17.01

It is used for building our user interface and for handling the view layer for our web app.

## Git bash(for HTTPS)

It provides an emulation layer for a Git command line experience.

# Database

The following steps need to be completed in order to set our database in your device.

## Open XAMPP

## Start Apache

Start the Apache HTTP Server.

## Start MySQL

**Be carefull not to run at the same time any other database programm locally on your computer, or it will not start**

## Click Admin in MySQL 

Pressing the Admin button in XAMPP's MySQL, you will be navigated to the phpMyAdmin site.

## Create database: chargeevolution

Now you are set to import the database's data.

## Click Shell in XAMPP

Clicking this button you will be navigated to the control panel of XAMPP.

## Import commands

Firstly, you need to type `cd` and the path of your directory which refers to the bin in the mysql file, which is included in the XAMPP's file. Most likely the path is the following `C:\xampp\mysql\bin`.
Secondly, you need to import the database, which is in a sql type file in the directory of our project's folder using the command `mysql -u root -p chargeevolution< C:\Users\User\tl20-54\back-end\sql_and_data/chargeevolution.sql`.

**You need to adapt the Users\User part in the path `C:\Users\User\tl20-54\back-end\sql_and_data/chargeevolution.sql` accordingly to your own path!**

# Build Backend

The following steps need to be completed so you can use our API.

## Pipenv installation

In a powershell on your computer type `pip install pipenv`. This command will automatically create and manage a virtual environment for your projects and add/remove packages from your Pipfile as you install/uninstall packages.

## Navigate to the project's path

Type `cd` and the TL20-54\back-end path.

## Pipenv activation

Type the command `pipenv sync`, which will install all the latest packages specified in the Pipfile.
Then, type the command `pipenv shell` which will activate the project's virtenv. 

## flask run

Flask provides a run command to run the application with a development server. In development mode, this server provides an interactive debugger and will reload when code is changed.

# Build Frontend

The following steps need to be completed so that you have all the proper packages and updates for our front-end.

## Navigate to the project's path

Open a Powershell. Then, type `cd` and the TL20-54\front-end path.

## `npm install`

Type `npm install` and press enter.
This command downloads a package and it's dependencies.

## `npm start` 

Type `npm start` and press enter.
This command runs the app in the development mode.

# HTTPS frontend

Go to front-end's `HTTPS_README` for details.