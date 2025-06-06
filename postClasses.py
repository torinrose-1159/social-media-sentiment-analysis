class SkeetData:
    link_headline = None
    link_url = None
    quoted_user = None
    quoted_text = None

    def __init__(
            self,
            post_date,
            username,
            handle,
            text_content,
            comments,
            reposts,
            likes,
            sentiment
    ):
        self.post_date = post_date
        self.username = username
        self.handle = handle
        self.text_content = text_content
        self.comments = comments
        self.reposts = reposts
        self.likes = likes
        self.sentiment = sentiment