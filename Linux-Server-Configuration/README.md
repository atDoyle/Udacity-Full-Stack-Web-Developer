# Linux Server

## Getting Started

This repository contains instructions to access and use the Linux server running on an AWS Lightsail instance.  The server is running Ubuntu and uses Apache2 to host the website created for the Item Catalog project in this course, utilizing a PostgreSQL database.  The IP address of this server is 18.221.54.126:80.

### Security

This Ubuntu server is running on an AWS Lightsail instance and can be accessed via a secure shell client, like PuTTY.  In order to access via SSH, the default Lightsail key was downloaded via the Lightsail console and moved to ~/.ssh, and the ssh port on the server was changed from *22* to *2200* in /etc/ssh/sshd_config.  From there, the server can be accessed via a SSH client by running **ssh ubuntu@18.221.54.126 -p 2200 -i ~/.ssh/LightsailDefaultPrivateKey-us-east-2.pem**.

Once the server can be accessed via SSH, the user *grader* was added and given sudo permission.  In order for the user *grader* to be able to login via ssh, a key pair needs to be generated for the user.  Once generated, the private key needs to be saved in the directory **/home/grader/.ssh/authorized_keys**.  The server can now be accessed with the public key by entering **ssh grader@18.221.54.126 -p 2200 -i ~/.ssh/grader**.

The final step in setting up the server prior to implementing the web server is to set the firewall settings.  This is done by enter *ufw allow [port]*.  Only ports 2200, 123 and 80 are currenty allowed through the firewall.  The firewall was then activated by entering *ufw enable*.

### Web Server

Apache2 is used in conjunction with the mod_wsgi package to run the web server from the relevent Python files, constructed using the Flask framework.

The .wsgi that is called when the request is made in the browser should call the primary *project.py* file which runs the web server, and the .conf configuration file needs to be modified to point to the newly created .wsgi file.  Additionally, the server name is changed to 18.221.54.126.xip.io, to provide a domain name that can use the Google OAuth2 client.

All of the relevent packages need to be installed in order for the Flask application to run properly, including Flask, SQLAlachemy, PostgreSQL, and Oauth2Client.  THese packages can be installed by entering *sudo apt-get install python-[package]*.

The client_secrets.json file needs to be reconfigured to be used on the Apache2 server.  In the Google Developer console, the domain name needs to be entered into the app information and the new client_secrets.json file downloaded.

Finally, the references to storage locations of other files (including /static/images, /static/css, /templates, and client_secrets.json) need to be update to reflect their relevent storage locations on the server.

### Using the site

To access the site, in the browser navigate to http://18.221.54.126.xip.io/.  From there the user can view the items on the website as well as login using their Google+ or Facebook account to add and modify items of their own.
