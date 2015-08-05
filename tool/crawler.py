# -*- coding: utf-8 -*-
import facebook
import json
import time
import sys
import re

class Crawler:
    '''
    all_posts: Json object
    args: Some parameters of facebook page. for example: {'fields': 'like, message'}
    '''

    def __init__(self, token, page_id):
        self.graph = facebook.GraphAPI(token)
        self.page_id = page_id
        self.token = token
        self.all_posts = []
        self.delay = 300

    def get_all_posts(self, args={'fields':'id,message,likes,comments,link'}):
        posts = self.graph.get_object(self.page_id + "/posts", **args)

        for post in posts['data']:
            try:
                self.all_posts.append({'msg':post['message'], 'time':post['created_time'], 'id':post['id'], 'link':post['link']})
            except KeyError:
                self.all_posts.append({'time':post['created_time'], 'id':post['id']})

    def save(self, filename):
        out = open(filename, 'w')
        out.write(json.dumps(self.all_posts, out, ensure_ascii=False, indent=2).encode('utf8'))
        out.close()

