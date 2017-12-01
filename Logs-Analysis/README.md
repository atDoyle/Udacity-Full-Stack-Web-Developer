# Logs Analysis

This repository contains code for a reporting tool that prints out reports (in plain text) based on the data in the database. This reporting tool is a Python program using the psycopg2 module to connect to the database.

Here are the questions the reporting tool answers:

1. What are the most popular three articles of all time? Which articles have been accessed the most?

2. Who are the most popular article authors of all time? That is, when you sum up all of the articles each author has written, which authors get the most page views?

3. On which days did more than 1% of requests lead to errors?

## Getting Started

This project uses 3 python files that each connect to the NEWS database and runs a unique query.  The results are printed in command prompt as well as into a text file.

### Prerequisites

These python files are meant to be run on a virtual machine with the NEWS database already installed.  The 3 python files should be saved to the shared vagrant directory.

### Installing

If you do not have Python 3.6 installed on your computer, the most recent version can be downloaded from the [Downloads page on the Python Software Foundation website](https://www.python.org/downloads/).

### Running the Files

Once the files have been downloaded to the shared vagrant directory, log into the virtual machine using **vagrant ssh**.  After logging in, cd in to the **/vagrant** shared directory and run each file using the **python** command.  The results of each query will print in the prompt as well as into its own text file.
