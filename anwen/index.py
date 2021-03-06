# -*- coding:utf-8 -*-

import markdown2
import time
from utils.fliter import filter_tags
from utils.avatar import get_avatar
from base import BaseHandler
import options
from db import User, Share, Tag
from pymongo import DESCENDING  # ASCENDING


class IndexHandler(BaseHandler):
    def get(self):
        page = self.get_argument("page", 1)
        share_res = Share.find().sort(
            '_id', DESCENDING).limit(10).skip((int(page) - 1) * 10)

        pagesum = (share_res.count() + 9) / 10
        shares = []
        for share in share_res:
            user = User.by_sid(share.user_id)
            share.name = user.user_name
            share.published = time.strftime(
                '%Y-%m-%d %H:%M:%S', time.localtime(share.published))
            share.domain = user.user_domain
            share.markdown = filter_tags(
                markdown2.markdown(share.markdown))[:100]
            share.gravatar = get_avatar(user.user_email, 16)
            shares.append(share)
        members = User.find().sort('_id', DESCENDING).limit(20)  # ASCENDING
        members_dict = []
        for member in members:
            member.gravatar = get_avatar(member.user_email, 25)
            members_dict.append(member)
        node = 'home'
        node_about = options.node_about[node]
        self.render(
            "node.html", shares=shares, members=members_dict,
            pagesum=pagesum, page=page, node=node, node_about=node_about)


class NodeHandler(BaseHandler):
    def get(self, node):
        page = self.get_argument("page", 1)
        share_res = Share.find({'sharetype': node}).sort(
            '_id', DESCENDING).limit(10).skip((int(page) - 1) * 10)
        pagesum = (share_res.count() + 9) / 10

        shares = []
        for share in share_res:
            user = User.by_sid(share.user_id)
            share.name = user.user_name
            share.published = time.strftime(
                '%Y-%m-%d %H:%M:%S', time.localtime(share.published))
            share.domain = user.user_domain
            share.markdown = filter_tags(
                markdown2.markdown(share.markdown))[:100]
            share.gravatar = get_avatar(user.user_email, 16)
            shares.append(share)
        members = User.find().sort('_id', DESCENDING).limit(20)
        members_dict = []
        for member in members:
            member.gravatar = get_avatar(member.user_email, 25)
            members_dict.append(member)
        node_about = options.node_about[node]
        self.render(
            "node.html", shares=shares, members=members_dict,
            pagesum=pagesum, page=page, node=node, node_about=node_about)


class TagHandler(BaseHandler):

    def get(self, name=None):
        if not name:
            tags = Tag.find()
            self.render("tag.html", tags=tags)
        else:
            tag = Tag.find_one({'name': name})
            shares = []
            for i in tag.share_ids.split(' '):
                share = Share.by_sid(i)

                user = User.by_sid(share.user_id)
                share.name = user.user_name
                share.published = time.strftime(
                    '%Y-%m-%d %H:%M:%S', time.localtime(share.published))
                share.domain = user.user_domain
                share.markdown = filter_tags(
                    markdown2.markdown(share.markdown))[:100]
                share.gravatar = get_avatar(user.user_email, 16)

                shares.append(share)
            self.render("tage.html", name=name, shares=shares)
