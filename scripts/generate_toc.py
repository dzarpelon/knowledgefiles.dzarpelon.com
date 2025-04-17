import os

def get_first_line(file_path):
    """Get the first non-empty line from a markdown file."""
    with open(file_path, "r") as file:
        for line in file:
            stripped_line = line.strip()
            if stripped_line:  # Skip empty lines
                return stripped_line.lstrip("# ").strip()  # Remove leading '#' for titles
    return "Untitled"

def generate_toc(directory):
    readme_path = os.path.join(directory, "README.md")
    if not os.path.exists(readme_path):
        print(f"No README.md found in {directory}")
        return

    # List all markdown files in the directory, excluding README.md
    markdown_files = [
        f for f in os.listdir(directory)
        if f.endswith(".md") and f != "README.md"
    ]

    # Sort files alphabetically
    markdown_files.sort()

    # Generate TOC content
    toc_lines = ["# Table of Contents\n"]
    for md_file in markdown_files:
        file_path = os.path.join(directory, md_file)
        title = get_first_line(file_path)
        toc_lines.append(f"- [{title}]({md_file})")

    # Read the existing README.md content
    with open(readme_path, "r") as readme_file:
        readme_content = readme_file.readlines()

    # Find the TOC section or append it if not found
    with open(readme_path, "w") as readme_file:
        toc_started = False
        for line in readme_content:
            if line.strip() == "# Table of Contents":
                toc_started = True
            if not toc_started:
                readme_file.write(line)
            elif line.strip() == "" and toc_started:
                break
        # Write the new TOC
        readme_file.write("\n".join(toc_lines) + "\n")

def generate_index_toc(base_dir, index_file):
    """Generate a TOC for the root index.html file with folder names."""
    folders = [
        f for f in os.listdir(base_dir)
        if os.path.isdir(os.path.join(base_dir, f))
    ]

    # Sort folders alphabetically
    folders.sort()

    # Generate TOC content
    toc_lines = ["<ul>"]
    for folder in folders:
        toc_lines.append(f'<li><a href="{folder}/index.html">{folder}</a></li>')
    toc_lines.append("</ul>")

    # Write the TOC to the index.html file
    with open(index_file, "r") as index:
        index_content = index.readlines()

    with open(index_file, "w") as index:
        for line in index_content:
            index.write(line)
            if "<body>" in line:  # Insert TOC after the opening <body> tag
                index.write("\n".join(toc_lines) + "\n")
                break

def extract_first_level_entries(summary_file):
    """Extract first-level entries from SUMMARY.md."""
    entries = []
    with open(summary_file, "r") as file:
        for line in file:
            stripped_line = line.strip()
            if stripped_line.startswith("* ") and stripped_line.count(" ") == 1:
                # Extract the link and title
                start = stripped_line.find("[") + 1
                end = stripped_line.find("]")
                title = stripped_line[start:end]

                start_link = stripped_line.find("(") + 1
                end_link = stripped_line.find(")")
                link = stripped_line[start_link:end_link]

                entries.append((title, link))
    return entries

def generate_index_toc_from_summary(summary_file, index_file):
    """Generate a TOC for the root index.html file using SUMMARY.md."""
    if not os.path.exists(summary_file):
        print(f"SUMMARY.md not found at {summary_file}")
        return

    entries = extract_first_level_entries(summary_file)

    # Generate TOC content
    toc_lines = ["<ul>"]
    for title, link in entries:
        toc_lines.append(f'<li><a href="{link}">{title}</a></li>')
    toc_lines.append("</ul>")

    # Write the TOC to the index.html file
    with open(index_file, "r") as index:
        index_content = index.readlines()

    with open(index_file, "w") as index:
        for line in index_content:
            index.write(line)
            if "<body>" in line:  # Insert TOC after the opening <body> tag
                index.write("\n".join(toc_lines) + "\n")
                break

if __name__ == "__main__":
    # Example usage: Generate TOC for all subdirectories in src
    base_dir = os.path.join(os.getcwd(), "src")
    for subdir in os.listdir(base_dir):
        subdir_path = os.path.join(base_dir, subdir)
        if os.path.isdir(subdir_path):
            generate_toc(subdir_path)

    # Generate TOC for the root index.html using SUMMARY.md
    book_dir = os.path.join(os.getcwd(), "book")
    summary_file = os.path.join(os.getcwd(), "src", "SUMMARY.md")
    index_file = os.path.join(book_dir, "index.html")
    generate_index_toc_from_summary(summary_file, index_file)