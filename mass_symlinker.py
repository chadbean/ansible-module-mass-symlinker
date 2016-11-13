#!/usr/bin/python

import os

DOCUMENTATION = '''
---
module: mass_symlinker
version_added: "0.1"
short_description: Takes files from directory A and symlinks to directory B
description: 
  - This takes a source directory "A" and symlinks all files
    from "A" into a destination directory "B". If "A" has sub-directories,
    then we will create those directories in "B" and make the appropriate
    symlinks recursively.
options:
  src:
    description:
      - Source directory which contains the files to symlink
  dest:
    description:
      - Destination directory where the symlinks will be created at from the source directory
  state:
    description:
      - Either 'present' (create) or 'absent' (remove)
    default: present
'''

EXAMPLES = '''
- name: Recursively create symlinks en masse
  mass_symlinker:
    src: /Users/username/.dotfiles
    dest: /Users/username
    state: present

- name: Recursively remove symlinks en masse
  mass_symlinker:
    src: /Users/username/.dotfiles
    dest: /Users/username
    state: absent
'''

def mass_symlinker_present(data, check_mode):
    source = data['src']
    destination = data['dest']
    has_changed = False
    success = True
    errors = []
    created_symlinks = []

    for root, dirnames, filenames in os.walk(source):
        destination_dir = ''.join([destination, root.replace(source, '')])

        for directory in dirnames:
            absolute_directory = os.path.join(destination_dir, directory)
            if not os.path.isdir(absolute_directory):
                if not check_mode:
                    try:
                        os.mkdir(absolute_directory, 0755)
                    except OSError:
                        err = get_exception()
                        errors.append('%s: %s' % (absolute_directory, str(err)))
                        continue
                has_changed = True

        for filename in filenames:
            absolute_source_filename = os.path.join(root, filename)
            absolute_destination_symlink = os.path.join(destination_dir, filename)
            if not os.path.exists(absolute_destination_symlink):
                if not check_mode:
                    try:
                        os.symlink(absolute_source_filename, absolute_destination_symlink)
                        created_symlinks.append(absolute_destination_symlink)
                        has_changed = True
                    except OSError:
                        err = get_exception()
                        errors.append('%s: %s' % (absolute_destination_symlink, str(err)))
                has_changed = True
                created_symlinks.append(absolute_destination_symlink)

    action_key_name = "to_be_created_symlinks" if check_mode else 'created_symlinks'
    results = {
        action_key_name: created_symlinks,
        "errors": errors,
    }

    meta = {"results": results}
    if len(errors) > 0:
        success = False

    return (has_changed, success, meta)

def mass_symlinker_absent(data, check_mode):  
    source = data['src']
    destination = data['dest']
    has_changed = False
    success = True
    errors = []
    deleted_symlinks = []

    for root, dirnames, filenames in os.walk(source, topdown=False):
        destination_dir = ''.join([destination, root.replace(source, '')])
        for filename in filenames:
            absolute_destination_symlink = os.path.join(destination_dir, filename)
            if os.path.exists(absolute_destination_symlink):
                if not check_mode:
                    try:
                        os.remove(absolute_destination_symlink)
                        deleted_symlinks.append(absolute_destination_symlink)
                        has_changed = True
                    except OSError:
                        err = get_exception()
                        errors.append('%s: %s' % (absolute_destination_symlink, str(err)))
                has_changed = True
                deleted_symlinks.append(absolute_destination_symlink)

        for directory in dirnames:
            absolute_directory = os.path.join(destination_dir, directory)
            if os.path.isdir(absolute_directory):
                if not check_mode:
                    try:
                        os.rmdir(absolute_directory)
                    except OSError:
                        err = get_exception()
                        errors.append('%s: %s' % (absolute_directory, str(err)))
                has_changed = True

    action_key_name = "to_be_deleted_symlinks" if check_mode else 'deleted_symlinks'
    results = {
        action_key_name: deleted_symlinks,
        "errors": errors,
    }

    meta = {"results": results}
    if len(errors) > 0:
        success = False

    return (has_changed, success, meta)

def main():
    fields = {
        "src": {"required": True, "type": "str"},
        "dest": {"required": True, "type": "str"},
        "state": {
            "default": "present",
            "choices": ['present', 'absent'],
            "type": 'str',
        },
    }
    choice_map = {
        "present": mass_symlinker_present,
        "absent": mass_symlinker_absent,
    }

    module = AnsibleModule(
        argument_spec=fields,
        supports_check_mode=True
    )
    has_changed, success, result = choice_map.get(module.params['state'])(module.params, module.check_mode)
    if success:
        module.exit_json(changed=has_changed, meta=result)
    else:
        module.fail_json(changed=has_changed, msg=result['results']['errors'])

from ansible.module_utils.basic import *
if __name__ == '__main__':
    main()
