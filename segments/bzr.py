import os
import subprocess

def get_bzr_status():
    has_modified_files = False
    has_untracked_files = False
    has_missing_files = False
    output = subprocess.Popen(['bzr', 'status', '--no-pending', '-S'],
            stdout=subprocess.PIPE).communicate()[0]
    if '? ' in output:
        has_untracked_files = True
    elif any(i in output for i in (' D ', '!', 'C  ')):
        has_missing_files = True
    elif any(i in output for i in (' M ', '+', 'R  ')):
        has_modified_files = True
    return has_modified_files, has_untracked_files, has_missing_files

def add_bzr_segment():
    child = subprocess.Popen(['bzr', 'revno'], stdout=subprocess.PIPE)
    streamdata = child.communicate()[0]
    if child.returncode != 0:
        return False

    branch = '(bzr)'
    filename = '.bzr/branch/location'
    for base_path in ('.', '..', '../..'):
        file_path = os.path.join(base_path, filename)
        if not os.path.isfile(file_path):
            continue
        with open(file_path) as f:
            branch = os.path.basename(f.read().rstrip('/'))

    bg = Color.REPO_CLEAN_BG
    fg = Color.REPO_CLEAN_FG
    has_modified_files, has_untracked_files, has_missing_files = get_bzr_status()
    if has_modified_files or has_untracked_files or has_missing_files:
        bg = Color.REPO_DIRTY_BG
        fg = Color.REPO_DIRTY_FG
        extra = ''
        if has_untracked_files:
            extra += '+'
        if has_missing_files:
            extra += '!'
        branch += (' ' + extra if extra != '' else '')
    return powerline.append(' %s ' % branch, fg, bg)

add_bzr_segment()
