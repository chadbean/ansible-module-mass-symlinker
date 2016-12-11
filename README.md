mass_symlinker
==============

An Ansible module to recursively symlink files from one directory to another.

Originally created so that I could take a directory with all of my dotfiles and symlink to my home directory.

Why not use the the "link" state option in the Ansible `file` module? This would symlink the whole dotfiles directory which may not be ideal as there likely secrets and other configuration in $HOME that should not wind up symlinked in a dotfiles repo. With this module, we will create subdirectories in $HOME to match the dotfiles repo structure and then link the contents from the dotfiles repo into those directories.

Requirements
------------

- ansible (tested against 2.2.0.0)
- python (tested against 2.7)

Installation
------------

Place the `mass_symlinker.py` file into your Ansible project's `library/` or the path shown in your `ANSIBLE_LIBRARY` directory.

Usage
-----

```
---
- hosts: localhost
  connection: local

    - name: Create symlinks
      mass_symlinker:
        src: /Users/chad/.dotfiles
        dest: /Users/chad/tmp
        state: present

    - name: Remove symlinks
      mass_symlinker:
        src: /Users/username/.dotfiles
        dest: /Users/username
        state: absent
```

License
-------

MIT
