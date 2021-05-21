import re, os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """

    # filenames = os.listdir(os.path.join(BASE_DIR, "entries"))
    filenames = os.listdir("./entries")

    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    # filename = os.path.join(BASE_DIR, f"entries/{title}.md")
    filename = f"./entries/{title}.md"

    tmp = open(filename, 'w')
    tmp.write(content)
    tmp.close()

def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """

    #filename = os.path.join(BASE_DIR, f"entries/{title}.md")
    filename = f"./entries/{title}.md"

    try:
        tmp = open(filename, 'r')
        content = tmp.read()
        tmp.close()
        return content
    except FileNotFoundError:
        return None
