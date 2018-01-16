# Item Catalog

This repository contains code for an application that provides a catalog of baseball cards as well as a user registration and authentication system. Registered users will have the ability to post, edit and delete their own teams and cards.


## Getting Started

This project uses a the Flask framework to run a web server in Python that will allow user to view existing teams, players and cards in a database as well as add their own.

### Prerequisites

In order for the files in this repository to work, you will need a terminal, such as Git Bash, a virtual machine, and a version of Python.

### Installing

GitBash can be downloaded and installed from the [GitBash website](https://git-for-windows.github.io/).

The virtual machine can be accessed using [Virtual Box](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1) and [Vagrant](https://www.vagrantup.com/downloads.html).

Once the virtual machine has been successfully installed, the News database can then be accessed.  The .sql file which contains the database can be downloaded [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip).  Ensure that the extracted files are placed in the shared vagrant directory.

If you do not have Python installed on your computer, the most recent version can be downloaded from the [Downloads page on the Python Software Foundation website](https://www.python.org/downloads/).

Once these steps have been completed, the repository should be downloaded and saved in the shared vagrant directory.

### Running the Files

The first thing that needs to be done is loading the data into the virtual machine.  To do that, first log into the virtual machine using **vagrant ssh**.  After logging in, cd into the **/vagrant** shared directory.  Once the virtual machine is up and running, the initial database needs to be created.  Do this by running **python database_setup.py** and then **python populate_db.py** to populate the database with some initial data.  Once these steps are complete, the web server can be launched by entering **python project.py** and navigating to http://localhost:5000.  From there, the existing data can be viewed, or the user can log in to add new data.
