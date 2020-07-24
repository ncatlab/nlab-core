#!/usr/bin/bash

# It may be possible to remove the following eventually, it is due to some
# incompatibility between client and server versions of MySQL
mysql -h $NLAB_MYSQL_DATABASE_HOST -u $NLAB_MYSQL_DATABASE_USER \
    -p$NLAB_MYSQL_DATABASE_PASSWORD $NLAB_MYSQL_DATABASE_NAME -e "\
    ALTER USER root IDENTIFIED WITH mysql_native_password BY \
    '$NLAB_MYSQL_DATABASE_PASSWORD'"

# A minimal version of the nLab database which allows for some
# single pages to be inserted. Not all columns are included.
mysql -h $NLAB_MYSQL_DATABASE_HOST -u $NLAB_MYSQL_DATABASE_USER \
    -p$NLAB_MYSQL_DATABASE_PASSWORD $NLAB_MYSQL_DATABASE_NAME -e "\
    CREATE TABLE pages (\
        id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,\
        updated_at DATETIME NOT NULL,\
        web_id INT(11) NOT NULL,\
        name VARCHAR(255));
    CREATE TABLE webs (\
        id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,\
        name VARCHAR(60) NOT NULL,\
        address VARCHAR(60) NOT NULL);\
    CREATE TABLE revisions (\
        id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,\
        page_id INT(11) NOT NULL,\
        content MEDIUMTEXT,\
        FOREIGN KEY (page_id) REFERENCES pages(id));\
    CREATE TABLE mathforge_nforum_Discussion (\
        DiscussionID INT(8) NOT NULL AUTO_INCREMENT PRIMARY KEY,\
        Name VARCHAR(100) NOT NULL,\
        DateLastActive DATETIME NOT NULL);\
    CREATE TABLE mathforge_nforum_Comment (\
        CommentID INT(8) NOT NULL AUTO_INCREMENT,\
        DiscussionID INT(8) NOT NULL,
        PRIMARY KEY (CommentID, DiscussionID))"

# Insert a wiki to represent the nLab, a second wiki, and a single page
# in each wiki
mysql -h $NLAB_MYSQL_DATABASE_HOST -u $NLAB_MYSQL_DATABASE_USER \
    -p$NLAB_MYSQL_ROOT_PASSWORD $NLAB_MYSQL_DATABASE_NAME -e "\
    INSERT INTO webs (name, address) VALUES ('nLab', 'nlab');\
    INSERT INTO webs (name, address) VALUES ('Some sub wiki', 'some-sub-wiki');\
    INSERT INTO pages (updated_at, web_id, name) VALUES (\
        '2020-07-22 10:11:55', 1, 'title of test page');\
    INSERT INTO pages (updated_at, web_id, name) VALUES (\
        '2020-07-23 14:11:55', 2, 'title of other test page');\
    INSERT INTO pages (updated_at, web_id, name) VALUES (\
        '2020-07-24 12:11:55', 1, 'title of third test page');\
    INSERT INTO revisions (page_id, content) VALUES (\
        1, '<p>Testing testing</p>');\
    INSERT INTO revisions (page_id, content) VALUES (\
        2, '<p>Testing testing again</p>');\
    INSERT INTO revisions (page_id, content) VALUES (\
        3, '<p>Testing testing a third time</p>');\
    INSERT INTO mathforge_nforum_Discussion (DiscussionID, Name,\
        DateLastActive) VALUES (\
        1, 'title of third test page', '2020-07-24 12:11:55');\
    INSERT INTO mathforge_nforum_Comment (CommentID, DiscussionID) VALUES (\
        1, 1);\
    INSERT INTO mathforge_nforum_Comment (CommentID, DiscussionID) VALUES (\
        2, 1);"


