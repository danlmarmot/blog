Title: Passing AWS Credentials to Vagrant in Ansible
Tags: ansible, aws
Category: Tech
comments: enabled
Slug: aws-creds-to-vagrant-with-ansible
Summary: Sometimes you need your Vagrant instances to have the same AWS creds as your host machine.  This is how I do it with Ansible.

I needed my Vagrant instance to have AWS credentials to access an S3 bucket, but didn't want to hardcode them anywhere.  I simple wanted to pass the values of the environment variables to Vagrant, and have it use those.

Since I was going to use Boto to get at that S3 bucket, I figured I just needed a way to set the variables in /etc/boto.conf on the Vagrant instance.

### The Vagrantfile

```ruby
VAGRANTFILE_API_VERSION = "2"
Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  config.vm.define "web" do |web|
    web.vm.box = "ubuntu/trusty64"
    web.vm.provision "ansible" do |ansible|
      ansible.extra_vars = "@group_vars/vagrant"
      ansible.groups = {
        "vagrant" => ["web"]
      }     
      ansible.playbook = "web-vagrant.yml"
    end
  end
  
end
```

### The Ansible group variables

The variables for Ansible are defined in group_vars/vagrant, which pulls them in from the two environment variables set on my Mac.

```text
group_name: vagrant
ansible_ssh_user: vagrant

# AWS keys for Vagrant are read from the Vagrant host and passed to the VM
aws_access_key: "{{ lookup('env','AWS_ACCESS_KEY_ID') }}"
aws_secret_key: "{{ lookup('env','AWS_SECRET_ACCESS_KEY') }}"
```
### The Ansible playbook

The playbook at web-vagrant.yml that defines Anisble tasks has this section in it.  Note it doesn't have:

```text
- name: Copy AWS creds from Vagrant host to Vagrant VM
  hosts: all
  user: "{{ ansible_ssh_user }}"
  sudo: yes
  gather_facts: false

  tasks:
  - name: Create the boto config file
    template: >
      src=vagrant/templates/boto.cfg.j2
      dest=/etc/boto.cfg
    when: group_name == "vagrant"
```
### The boto template
And that boto template is just this small file, placed in vagrant/templates/boto.cfg.j2

```ini
[Credentials]
aws_access_key_id = {{ aws_access_key }}
aws_secret_access_key = {{ aws_secret_key }}
```

## Testing this out
With Ansible, Vagrant, and Virtualbox installled, create these four files and put them in their correct places.  The directory structure should look like this:

```text
.
├── Vagrantfile
├── group_vars
│   └── vagrant
├── vagrant
│   └── templates
│       └── boto.cfg.j2
└── web-vagrant.yml

```

Open a command prompt, and type these commands:

```text
vagrant up
vagrant ssh
cat /etc/boto.cfg
```

The AWS keys from your Mac should be now inserted into boto.cfg.

To reprovision the Vagrant box, use "vagrant provision" to rerun the Ansible playbook.

When you're done, dispose of the Vagrant VM with

```text
vagrant destroy
```


## Going further

You could also do the same to create a config file for the [AWS CLI tool](http://aws.amazon.com/cli/) if you're looking for something at the command line

I didn't need this--in production, Boto will use the credentials taken from the instance's IAM role that it was launched with.
