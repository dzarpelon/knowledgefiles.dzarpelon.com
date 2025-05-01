import os

def get_title(md_path):
    with open(md_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('#'):
                return line.lstrip('#').strip()
    return os.path.splitext(os.path.basename(md_path))[0]

def walk_dir(base, rel=''):
    entries = []
    full_path = os.path.join(base, rel)
    for name in sorted(os.listdir(full_path)):
        if name == 'SUMMARY.md':
            continue  # Skip SUMMARY.md itself
        path = os.path.join(full_path, name)
        rel_path = os.path.join(rel, name)
        if os.path.isdir(path):
            readme = os.path.join(path, 'README.md')
            if os.path.exists(readme):
                # Use the first title from the folder's README.md as the link text
                entries.append((get_title(readme), os.path.join(rel_path, 'README.md'), walk_dir(base, rel_path)))
            else:
                sub_entries = walk_dir(base, rel_path)
                if sub_entries:
                    entries.append((name, None, sub_entries))
        elif name.endswith('.md') and name.lower() != 'readme.md':
            entries.append((get_title(path), rel_path, []))
    return entries

def write_summary(entries, f, indent=0):
    for title, path, children in entries:
        if path:
            f.write('  ' * indent + f'- [{title}]({path})\n')
        else:
            f.write('  ' * indent + f'- {title}\n')
        if children:
            write_summary(children, f, indent + 1)

if __name__ == '__main__':
    src_dir = 'src'
    summary_path = os.path.join(src_dir, 'SUMMARY.md')
    entries = walk_dir(src_dir)
    with open(summary_path, 'w') as f:
        f.write('# Summary\n\n')
        # Always add the Welcome page first
        f.write('- [Welcome](' + 'README.md' + ')\n')
        write_summary(entries, f)
