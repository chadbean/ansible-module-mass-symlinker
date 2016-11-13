mass_symlinker
==============

An Ansible module to recursively symlink files from one directory to another.

Originally created so that I could take a directory with all of my dotfiles and symlink to my home directory.

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
