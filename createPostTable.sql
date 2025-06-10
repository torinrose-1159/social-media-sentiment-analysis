CREATE TABLE bluesky_post_data (
    post_date TIMESTAMP NOT NULL,
    username VARCHAR(50) NOT NULL,
    handle VARCHAR(50) NOT NULL,
    text_content VARCHAR(300) NOT NULL,
    comments INTEGER NULL,
    reposts INTEGER NULL,
    likes INTEGER NULL,
    sentiment NUMERIC(3, 3) NOT NULL,
    link_headline VARCHAR(500) NULL,
    link_url VARCHAR(1000) NULL,
    quoted_user VARCHAR(50) NULL,
    quoted_text VARCHAR(300) NULL,
    keyword VARCHAR(255) NOT NULL,
    PRIMARY KEY (post_date, username)
)