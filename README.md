# About

This is my repository of the roles I use to manage most of my infrastructure and other things. The idea is I would use event driven ansible to perform automatic configuration upon provisioning of whatever I set up just by making a web call with curl or something to it.

* [Ansible EDA on Galaxy](https://galaxy.ansible.com/ui/repo/published/ansible/eda/)
* [Ansible Rulebook Documentation](https://ansible.readthedocs.io/projects/rulebook/en/latest/)
* [Red Hat Event-Driven Ansible](https://www.redhat.com/en/technologies/management/ansible/event-driven-ansible)

# Event Driven Ansible Config and Setup

1. mkdir hosts.
2. Add your inventory files to hosts/.
3. Create your own vars/private_config.yml from vars/private_config_example.yml.
4. Modify the private_key_file variable in ansible.cfg to point to the correct path for your SSH private key.
5. Run: ansible-rulebook -r rulebook.yml -i hosts/ -vv
    1. If you are using a directory for your inventory, you have to put a "/" at the end to indicate it is a directory.
6. On a test host, run: curl http://ansible-eda:6000 -d '{"host": "test-host-1", "cloud-init-setup": true}'

# How to install ansible with pipx

```
pipx install ansible-core
pipx inject --include-apps ansible-core dnspython
pipx inject --include-apps ansible-core jmespath
pipx inject --include-apps ansible-core netaddr
pipx inject --include-apps --include-deps ansible-core requests
pipx inject --include-apps ansible-core pyVim
pipx inject --include-apps ansible-core PyVmomi
pipx inject --include-apps --include-deps --force ansible-core selinux
```

# Ansible Galaxy Needs

```
ansible-galaxy collection install --upgrade ansible.posix ansible.utils cloud.common community.general containers.podman community.vmware vmware.vmware_rest kubernetes.core
```

# How to upgrade ansible with pipx

```
pipx upgrade-all --include-injected
```

# How to install the ansible dev tools with pipx

```
pipx inject --include-apps ansible-core ansible-dev-tools
```
