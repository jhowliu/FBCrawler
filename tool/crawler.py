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
        self.delay = 300

    def get_all_posts(self, args={'fields':'id,message,link', 'until':''}):
        # catch exception of GraphAPI
        try:
            posts = self.graph.get_object(self.page_id + "/posts", **args)
        except:
            print "Time to delay, Saving. (5 Mins)", len(self.all_posts)
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

    def get_like_counts(self, args={'limit':10000, 'after':''}):
        for post in self.all_posts:
            like_count = 0
            print post['id']

            while True:
                try:
                    likes = self.graph.get_object(post['id'] + '/likes', **args)
                    like_count = like_count + len(likes['data'])
                except:
                    print "Time to delay. (5 Mins)"
                    time.sleep(self.delay)
                    likes = self.graph.get_object(post['id'] + '/likes', **args)
                # get the id of next page
                try:
                    args['after'] = likes['paging']['cursors']['after']
                except:
                    print "Like count: %d" % like_count
                    post['like_count'] = like_count
                    args['after'] = ''
                    break

    def save(self, filename=None):
        if not filename:
            filename = datetime.now().strftime("%Y-%m-%d %H:%M:%S.json")
        out = open(filename, 'w')
        json.dump(self.all_posts, out, encoding='utf8')
        out.close()
