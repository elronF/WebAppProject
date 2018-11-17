# Investment Tracker Project

This project is an investment tracker web app. It utilizes Python, Flask and SQLAlchemy to allow a user to create, update, edit and delete a portfolio of investments spread across a set number of accounts.

## SETUP

A **Linux VM** and **Python3** is required to run this app.

**Vagrant** and **Virtual Box** were utilized to develop this project.  Installation instructions can be found at: -https://www.virtualbox.org/wiki/Download_Old_Builds_5_1 and https://www.vagrantup.com/downloads.html

Once Vagrant and Virtual Box are installed, pull the Vagrantfile from this project's repository and place it in a folder called "vagrant". From the terminal, navigate to your vagrant folder and run the command ```vagrant up```. An automated setup will run. Once complete, you can log-in to your VM using the command ```vagrant ssh```

The requirements needed to run this app include **Flask**, **SQLAlchemy**, **OAuth** and **PySocks**. Commands for installing these packages through pip are below:

```bash
pip3 install flask
pip3 install SQLAlchemy
pip3 install oauth2client
pip3 install PySocks
```

To access the full functionality of this Tracker app, a Gmail or Google+ account will be required in order to obtain authorization.

## Running Program

The app folder should be placed within a sub-folder of the 'vagrant' folder.

To run this program, navigate to the project folder and use the command python3 app.py. On your web browser, navigate to localhost:5000 to access