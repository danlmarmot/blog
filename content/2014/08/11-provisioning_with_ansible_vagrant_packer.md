Title: Provisioning with Vagrant, Ansible, and Packer
Date: 2014-08-11 18:55
Tags: ansible, vagrant, packer
Category: Tech
Slug: provisioning-with-vagrant-ansible-packer

One big issue in using servers on cloud providers suck as Amazon Web Services, Rackspace, and Google Compute Engine is dealing with their provisioning and deployment--in other words, how to build them out to begin with.
Sure, you can write lots of Bash scripts, invest in Puppet and Chef training and infrastructure, and script the whole thing out.  I've tried some of those, but generally found them real burdensome and in general they hinder productivity, not improve it.

Ansible is a more recent utility that aims to be simpler to use by developers, and I've found it better integrates with my workflows, and is much less difficult to maintain. Ansible works strictly over SSH and doesn't require you to manage any additional infrastructure such as a server--and I like the fact that you don't have to install agents on the machines you manage, so you don't have the tricky problem of bootstrapping with cloud-init.

This lengthy blog post focuses on using Ansible with Vagrant and Packer, so that we can automate the provisioning of virtual machines for development, QA, CI, and production.  For development, we'll be using Vagrant, and for cloud deployments we'll be using Packer to create machine images for Amazon.

## A few terms first

To get on the same page, here's some terms and conventions I'm using in this article.

###Provisioning

Provisioning is the initial configuration and setup of a machine instance, including installation of all pre-requisite packages and software, creation of user and service accounts, and configuration. It's what you have to do before you install any of your applications. Provisioning also generally includes common monitoring tools and utilities to make sure the machine can update its health status or emit metrics to the operations infrastructure.

###Deployment

Deployment is simply putting one or more applications on the machine. After provisioning, an initial deployment is typically done.  An image is often created as well, before or after the deployment.

###Environment
An environment is a collection of services and machines that depend on each other. Think of the term "environment" as meaning "production environment" or "staging environment" or "local environment". Different development teams use different terms.

###Machine Image
Machine images are snapshots of machine, usually with all software and dependencies installed, and perhaps an initial deployment of up-to-date code. They are provider-specific: Amazon machine images aren't the same as VMware machine images or Digital Ocean machine images, and often have to be created with provider-specific tools.

## Prep Work
This document is really meant to be used by Mac users, and in particular folks running MacOS 10.9. Vagrant/Packer/Ansible are all oriented towards various Unix flavors, and don't fully support Windows. Other operating systems related to Linux are supported, such as Mac OS X, Ubuntu, Centos, Fedora, AmazonLinux, and versions of FreeBSD.  But I'm just using my Mac.

## Step 0 - Clone the Github repository
For this demo, the code's on Github.  You can get it with this command
 
`git clone https://github.com/danlmarmot/demo-ansible-vagrant-packer`

Clone it onto your local Mac--if you need help at this point, see the Github help pages.


## Step 1 - Install Vagrant and VirtualBox
With the source code checked out, change into the checked out git repo with

`cd demo-ansible-vagrant-packer/`

We will not be changing out of this directory, so you're good at this point.

### Install VirtualBox and Vagrant

VirtualBox is available at https://www.virtualbox.org/wiki/Downloads.

Vagrant is at https://www.vagrantup.com/downloads.html

Once you've installed, enter these commands to verify your installation
At a command prompt type the following and ensure there aren't any errors.


`vagrant -v`

### Initialize Vagrant
Look at the Vagrantfile at the root of your checkout. It should look like this if you've checked it out from Git -- if you haven't, make it look like this:

```ruby
Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.network :private_network, ip: "192.168.111.222"
end
```
This just says launch an Ubuntu Trusty 64-bit image (which is Ubuntu 14.04 LTS, released in April 2014).

*A side note: Vagrantfiles are written in Ruby syntax--if you know Ruby, you can add additional logic to them.*

Launch the VM with 'vagrant up':

`vagrant up`


You should see:

```text
Bringing machine 'default' up with 'virtualbox' provider...
==> default: Box 'ubuntu/trusty64' could not be found. Attempting to find and
install...
    default: Box Provider: virtualbox
    default: Box Version: >= 0
==> default: Loading metadata for box 'ubuntu/trusty64'
    default: URL: https://vagrantcloud.com/ubuntu/trusty64
==> default: Adding box 'ubuntu/trusty64' (v14.04) for provider: virtualbox
    default: Downloading:
https://vagrantcloud.com/ubuntu/trusty64/version/1/provider/virtualbox.box
    default: Progress: 33% (Rate: 1274k/s, Estimated time remaining: 0:01:03)
Connect with SSH to the Vagrant VM:
vagrant ssh
Welcome to Ubuntu 14.04 LTS (GNU/Linux 3.13.0-24-generic x86_64)
```

Now you've got a Vagrant-managed VM to work with! Exit the SSH prompt with:


`exit`



### Step 2 - Add Ansible to manage the Vagrant VM

We'll be using Ansible, which works over SSH to configure the VM, reading from YAML files to drive the configuration. Ansible doesn't require any software to be installed on the VM (it's agentless).  I put my Ansible YAML files are checked into source control alongside the Vagrantfile into a directory called provision.

This Ansible YAML document describing the steps to perform is called a playbook. Vagrant knows how to use Ansible to provision the instance, with a reference to that YAML file in the the Vagrantfile.

To make sure things all work, we're going to do a really simple task: create the directory /tmp/foo on the Vagrant VMVM.


#### Resources
There are a lot of resources on the web that describe these steps.  These are the ones I found handy are handy when you get done with walking through this guide:

[http://docs.ansible.com/guide_vagrant.html](http://docs.ansible.com/guide_vagrant.html)

[http://docs.vagrantup.com/v2/provisioning/ansible.html](http://docs.vagrantup.com/v2/provisioning/ansible.html)

[https://www.digitalocean.com/community/articles/how-to-create-ansible-playbooks-to-automate-system-configuration-on-ubuntu](https://www.digitalocean.com/community/articles/how-to-create-ansible-playbooks-to-automate-system-configuration-on-ubuntu)

### Install Ansible
First, we need to install Ansible, which is a Python package.  Mac OS X 10.9 has Python 2.7 pre-installed.

We will install Ansible globally, and not in a virtual environment–it's not a heavy installation, and doesn't require any other software dependencies apart from a few other Python packages. One of these Python packages for SSH will need to be compiled with XCode, so you'll need the XCode (available from the App Store) and the XCode command line tools installed.

Run these two commands to install Ansible. The first ensures pip is installed (the standard Python package manager), then the next installs or upgrades Ansible if you've previously installed it.

`sudo easy_install pip; sudo pip install ansible --upgrade`

### An Important XCode Gotcha
On MacOS X with some versions of XCode, if you get an error about "-Wno-error=unused-command-line-argument-hard-error-in-future" you can supress the warning by installing Ansible with this ugly command.

`sudo ARCHFLAGS=-Wno-error=unused-command-line-argument-hard-error-in-future pip install ansible --upgrade`


Side note: This is a tedious warning, and if you install other Python packages or Ruby gems that require compiling you'll hit this over and over. You can add this your your ~/.bash_profile on your Mac to get around this.

`echo export ARCHFLAGS=-Wno-error=unused-command-line-argument-hard-error-in-future >>
~/.bash_profile; source ~/.bash_profile`


### Update the source code to step 2

`git checkout -f tags/step2`

### Add an Ansible playbook
This playbook will be at the top of our directory, and we'll name it "playbook.yml".

You can write this out yourself, or just look at what Git checked out.

```text
---
- name: Verify ansible works
  hosts: all
  user: vagrant
  sudo: yes
  gather_facts: false
  tasks:
    - name: Create /tmp/foo
      file: path=/tmp/foo state=directory
```

### Update the Vagrantfile with Ansible provisioning
Now let's add the Ansible provisioner to the Vagrantfile--that's the file that tells Vagrant to use Ansible to build out the VM. That entire file should look like this.

```ruby
VAGRANTFILE_API_VERSION = "2"
Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.network :private_network, ip: "192.168.111.222"
  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "playbook.yml"
    ansible.extra_vars = { ansible_ssh_user: 'vagrant' }
    ansible.verbose = "vv"
  end
end
```

###Provision the VM
This is where the magic happens. Run it from a command prompt with

`vagrant provision`

If everything's setup correctly, you'll see output similar to this:

```text
==> default: Running provisioner: ansible...
ANSIBLE_FORCE_COLOR=true ANSIBLE_HOST_KEY_CHECKING=false PYTHONUNBUFFERED=1 ansible-playbook --private-key=/Users/Marmot/.vagrant.d/insecure_private_key --user=vagrant --limit='default' --inventory-file=/Users/Marmot/dev/bb-danlmarmot/demo-ansible-vagrant-packer/.vagrant/provisioners/ansible/inventory --extra-vars={"ansible_ssh_user":"vagrant"} -vv playbook.yml

PLAY [Verify ansible works] ***************************************************

TASK: [Create /tmp/foo] *******************************************************
<127.0.0.1> REMOTE_MODULE file path=/tmp/foo state=directory
changed: [default] => {"changed": true, "gid": 0, "group": "root", "mode": "0755", "owner": "root", "path": "/tmp/foo", "size": 4096, "state": "directory", "uid": 0}

PLAY RECAP ********************************************************************
default                    : ok=1    changed=1    unreachable=0    failed=0
```

At this point Ansible and Vagrant are working with each other. That's a big win, and now we can start doing more complicated things.

####Troubleshooting "vagrant provision"

#####Error: "VM not created"

If you get a message similar to this:

```text
vagrant provision
==> default: VM not created. Moving on...
```

Fix it by:

`vagrant up`

This is just simply because the Vagrant VM isn't running, so it can't receive the `vagrant provision` command

###Verify that the provisioning worked

Now let's verify this worked by SSH-ing into the Vagrant VM.

```text
vagrant ssh
vagrant@vagrant-ubuntu-trusty-64:~$ ls /tmp
foo
```

Exit out of the SSH session

```text
vagrant@vagrant-ubuntu-trusty-64:~$ exit
```
### Destroy the Vagrant VM

We won't be using this simple VM in the following steps--it was good to verify that Ansible is setup correctly--so we'll destroy it.

```text
vagrant destroy
    default: Are you sure you want to destroy the 'default' VM? [y/N] y
==> default: Forcing shutdown of VM...
==> default: Destroying VM and associated drives...
==> default: Running cleanup tasks for 'ansible' provisioner...

```


##Step 3 - Using Ansible to provision nginx

Ansible can be used for quite a bit more than create directories from a single playbook file, and can manipulate a fair number of resources from system settings (users, groups, cronjobs, package repositories) to applications (Apache httpd, ntpd) to cloud assets (AWS EC2 instances, OpenStack storage).  For a full list visit http://docs.ansible.com/modules_by_category.html

This is also when we'll start using more typical Ansible conventions.

###Resources

[http://docs.ansible.com/playbooks_best_practices.html](http://docs.ansible.com/playbooks_best_practices.html) has a good walk-through of a non-trivial site layout involving a few different types of servers in a few different server locations.

### Update source

In that same directory, update the source code to step 3

`git checkout -f tags/step3`


###Create the provisioning directory for nginx
Ansible has a recommended convention for laying out a directory. The docs are here, [http://docs.ansible.com/playbooks_best_practices.html](http://docs.ansible.com/playbooks_best_practices.html), and they're a good walk-through of a non-trivial layout.


The following steps show what you'll have to do manually--if you haven't checked out step3 from git, do these manually. First, create a directory to hold our Ansible provisioning files.

`mkdir provision`

Create the nginx role in Ansible

Now, add an Ansible role to install nginx:

`ansible-galaxy init roles/nginx`


And let's edit some files. Note that each file should start with the three dashes, which indicates it's a YAML file.  (Ansible isn't all that picky on those three dashes, though) The entire contents of all the file are listed below:

####roles/nginx/tasks/main.yml
This is the main list of tasks that Ansible performs when it's provisioning the nginx role. These tasks are performed sequentially, there's no "convergence" phase at runtime as there are in other tools.


```text
---
 - name: add nginx ppa repository
   apt_repository: repo='ppa:nginx/stable'

 - name: install nginx
   apt: pkg=nginx state=installed

 - name: remove default site
   file: path=/etc/nginx/sites-enabled/default state=absent
   notify: restart nginx  

 - name: add our nginx.conf
   copy: src=nginx.conf dest=/etc/nginx/nginx.conf owner=root group=root mode=644
   notify: restart nginx  

 - name: add static directory
   file: path=/opt/static state=directory

 - name: add static site index.htm file
   copy: src=index.html dest=/opt/static/index.html owner=root group=root mode=644
   notify: restart nginx  

 - name: add nginx config file for static site
   copy: src=static.conf dest=/etc/nginx/conf.d/static.conf owner=root group=root mode=644
   notify: restart nginx  

 - name: start nginx
   service: name=nginx state=started
```

####nginx/tasks/handlers.yml
Handlers are actions that are triggered when task does something.  With this nginx example, we'll want to restart nginx if we change the config files for nginx or the static site we're serving.

We have two handlers to do this.  The 'restart nginx' handler (which is called whenever a file changes through the task list above), and the 'verify nginx' handler to make sure nginx still works. The first 'restart nginx' handler calls the second handler with the notify statement.

That second handler just performs a "curl" command to make sure nginx is working.

```text
---
 - name: restart nginx
   service: name=nginx state=restarted
   notify: verify nginx

 - name: verify nginx
   shell: curl 127.0.0.1:8080
```

####roles/nginx/files/nginx.conf
The nginx.conf file.  This is just a plain text file.  Ansible supports templates, but we're not using them in this walk-through.

```text
user www-data;
worker_processes 4;
pid /run/nginx.pid;

events {
	worker_connections 768;
}

http {
	include /etc/nginx/mime.types;
	default_type application/octet-stream;

	access_log /var/log/nginx/access.log;
	error_log /var/log/nginx/error.log;

	include /etc/nginx/conf.d/*.conf;
}
```

####roles/nginx/files/static.conf
This text file just says where the static files live. We're putting them in /opt/static (many people put them in somewhere in /var, but I prefer to serve sites and web applications out of /opt/*)

```text
server {
	listen 8080;
	location / {
		root /opt/static;
		index index.html index.htm;
	}
}
```

####roles/nginx/files/index.html
A static webpage that's served by nginx.

```text
 <html>
 <h2>Hey nginx works!</h2>
 </html>
```

####webserver.yml
This is an Ansible playbook to build out a webserver in our Vagrant environment.

```text
---
# file: webserver.yml
- hosts: all
  user: vagrant
  sudo: yes
  gather_facts: false
  roles:
    - nginx
```


####site.yml

This describes the site.  There's just the one server type in there now.


```text
---
# file: site.yml
- include: webserver.yml
```

###A bit of explanation--how Ansible describes the site
Now that you've done all that... what's all that mean?


With Ansible, the overall site is typically described by site.yml. It's a file that describes the entire site, and often it's pretty short and just includes other files, usually instances/servers/boxes by what they do, such as "web server" or "database server".

With Ansible terminology the term "role" refers to a fairly specific package or software component, like nginx or MySQL.

Ansible ends up having a tree of site components:


- The overall site in site.yml. This lists all the server types like "web_server" or "database_server". Sites can also be described by location, such as "oregon_servers" or "dublin_servers"

- Server classes defined in <server>.yml file. This defines what roles are applied to each server type. Web servers might get nginx; database servers might get Postgres.

- Roles in a <rolename> directory. Roles are encapuslated components, like redis or Apache web server, or a custom Java app in a Tomcat container.  The role directory has subdirectories inside where Ansible knows where to look, and the ones we use here are "files", "handlers", and "tasks".


###Update the Vagrantfile
We'll update the Vagrantfile to point to the new playbook, and refactor it a bit so it's easier to add new server types.

We'll also expose port 8080, so we can open up a web browser on our Mac to see nginx serving pages.

```ruby
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.define "webserver" do |webserver|
    webserver.vm.box = "ubuntu/trusty64"
    webserver.vm.network :private_network, ip: "192.168.111.222"
    webserver.vm.network :forwarded_port, guest: 8080, host: 8080
    webserver.vm.provision "ansible" do |ansible|
      ansible.extra_vars = { ansible_ssh_user: 'vagrant' }
      ansible.verbose = "vv"
      ansible.playbook = "webserver.yml"
    end
  end
end
```

Launch this new Vagrant instance with

`vagrant up webserver`

Ansible will startup the new instance, install nginx and our single-page static site, and verify it's working with the curl command--look in the console output for the HTML.

###Verify
You should also verify this works from your Mac--just visit [http://localhost:8080](http://localhost:8080), and you should see the "Hey nginx works!"

### Reprovisioning
When you're developing with Ansible and Vagrant, you'll be tweaking your playbooks and task lists and files over and over, and you'll need a way to quickly rerun your work.  It takes a fairly long time to reimport a virtual machine from scratch, but Vagrant can reprovision your box with a simple command.

Let's try that now: edit the index.html file inside roles/nginx/files/index.html to say "Heyyyyy nginx works", and save the file away.

Now, rerun the provisioning on your Vagrant VM with

`vagrant provision`

You'll see that the index.htm file is changed:

```text
TASK: [nginx | add static site index.htm file] ********************************
changed: [webserver] => {"changed": true, "dest": "/opt/static/index.html", "gid": 0, "group": "root", "md5sum": "02f40bd936f4d308a679c0fa636e317d", "mode": "0644", "owner": "root", "size": 46, "src": "/home/vagrant/.ansible/tmp/ansible-tmp-1407855909.5-223798276574238/source", "state": "file", "uid": 0}
```

Because there is a notification handler on that file, nginx will be restarted and verified with curl:

```text
NOTIFIED: [nginx | restart nginx] *********************************************
<127.0.0.1> REMOTE_MODULE service name=nginx state=restarted
changed: [webserver] => {"changed": true, "name": "nginx", "state": "started"}

NOTIFIED: [nginx | verify nginx] **********************************************
<127.0.0.1> REMOTE_MODULE command curl 127.0.0.1:8080 #USE_SHELL
changed: [webserver] => {"changed": true, "cmd": "curl 127.0.0.1:8080 ", "delta": "0:00:00.009759", "end": "2014-08-12 15:07:03.461307", "rc": 0, "start": "2014-08-12 15:07:03.451548", "stderr": "  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current\n                                 Dload  Upload   Total   Spent    Left  Speed\n\r  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0\r100    44  100    44    0     0  17908      0 --:--:-- --:--:-- --:--:-- 22000", "stdout": "<html>\n<h2>Heyyyyy nginx works!!</h2>\n</html>"}
```

You can (and should!) verify from your Mac's web browser by visiting [http://localhost:8080](http://localhost:8080)


d