# -*- coding: utf-8 -*-
from datetime import datetime
import facebook
import parser
import json
import time
import sys

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
        self.all_like_counts = []
        self.delay = 300

    def get_all_posts(self, args={'fields':'id,message,link', 'until':''}):
        # catch exception of GraphAPI
        try:
            posts = self.graph.get_object(self.page_id + "/posts", **args)
        except:
            print "Time to delay, Saving.", len(self.all_posts)
            self.save(datetime.now().strftime("%Y-%m-%d %H:%M:%S.json"))
            time.sleep(self.delay)
            posts = self.graph.get_object(self.page_id + "/posts", **args)

        # iterate posts
        for post in posts['data']:
            try:
                self.all_posts.append({'msg':post['message'], 'time':post['created_time'], 'id':post['id'], 'link':post['link']})
            except KeyError:
                pass

        # return the next page id
        return parser.get_nextpage_id(posts['paging']['next'])

    def get_all_like_counts(self, args={'limit':10000, 'after':''}):

        for post in self.all_posts:
            try:
                likes = self.graph.get_object(post['id'] + )

    def save(self, filename):
        out = open(filename, 'w')
        out.write(json.dumps(self.all_posts, out, ensure_ascii=False).encode('utf8'))
        out.close()
