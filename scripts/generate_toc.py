import os

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
        title = os.path.splitext(md_file)[0].replace("_", " ").title()
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

if __name__ == "__main__":
    # Example usage: Generate TOC for all subdirectories in src
    base_dir = os.path.join(os.getcwd(), "src")
    for subdir in os.listdir(base_dir):
        subdir_path = os.path.join(base_dir, subdir)
        if os.path.isdir(subdir_path):
            generate_toc(subdir_path)