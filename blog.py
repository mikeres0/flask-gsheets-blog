class Blog(object):
    blogid = -1
    datecreated = ""
    title = ""
    description = ""
    content = ""
    contenttype = ""
    author = ""
    tags = ""

    def __init__(self, blogid, datecreated, title, description, content, contenttype, author, tags):
        self.blogid = blogid,
        self.datecreated = datecreated,
        self.title = title,
        self.description = description,
        self.content = content,
        self.contenttype = contenttype,
        self.author = author,
        self.tags = tags
