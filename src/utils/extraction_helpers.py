import re

def extract_markdown_links(text):
    result = []

    links = re.findall(r"(?<!!)\[.*?\]\(.*?\)", text)

    for link in links:
        anchor_text = extract_contents_of_square_brackets(link)
        href = extract_contents_of_regular_brackets(link)


        result.append((anchor_text, href))

    return result
def extract_contents_of_square_brackets(text):
        inner_text = re.search(r'\[(.*?)\]', text)
        if inner_text:
            inner_text = inner_text.group(1)
        else:
            raise Exception("something seriously wrong's gone on here")
        return inner_text


def extract_contents_of_regular_brackets(text):
        inner_text = re.search(r'\((.*?)\)', text)
        if inner_text:
            inner_text = inner_text.group(1)
        else:
            raise Exception("something seriously wrong's gone on here")
        return inner_text
