# Logs Analysis

This repository contains code for a reporting tool that prints out reports (in plain text) based on the data in the database. This reporting tool is a Python program using the psycopg2 module to connect to the database.

Here are the questions the reporting tool answers:

1. What are the most popular three articles of all time? Which articles have been accessed the most?

2. Who are the most popular article authors of all time? That is, when you sum up all of the articles each author has written, which authors get the most page views?

3. On which days did more than 1% of requests lead to errors?

## Getting Started

This project uses 3 python files that each connect to the NEWS database and runs a unique query.  The results are printed in command prompt as well as into a text file.

### Prerequisites

In order for the files in this repository to work, you will need a terminal, such as [GitBash](https://git-for-windows.github.io/), a virtual machine, the News database that is provided and a version of Python 3.6.

### Installing

The virtual machine can be accessed using [Virtual Box](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1) and [Vagrant](https://www.vagrantup.com/downloads.html).

Once the virtual machine has been successfully installed, the News database can then be accessed.  The .sql which contains the database can be downloaded [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip).  Ensure that the extracted files are placed in the shared vagrant directory.

If you do not have Python 3.6 installed on your computer, the most recent version can be downloaded from the [Downloads page on the Python Software Foundation website](https://www.python.org/downloads/).

### Running the Files

The first thing that needs to be done is loading the data into the virtual machine.  To do that, first log into the virtual machine using **vagrant ssh**.  After logging in, cd into the **/vagrant** shared directory and enter the command **psql -d news -f newsdata.sql**.  After the data has been loaded the queries can be run successfully using the **python** command for each .py script in the respository.  The results of each query will print in the prompt as well as into its own text file.
