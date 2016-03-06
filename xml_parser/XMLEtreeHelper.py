# -*- coding: utf-8 -*-
from lxml import etree

__author__ = 'xiaolong'


class XMLEtreeHelper:
    def __init__(self):
        pass

    @classmethod
    def create_node(cls, parent_node, node_name, node_text):
        node = etree.SubElement(parent_node, node_name)
        node.text = node_text
        return node
