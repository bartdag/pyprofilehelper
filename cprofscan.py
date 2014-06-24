#!/usr/bin/env python

# -*- coding: utf-8 -*-
"""
Prints time spent in each module.
"""

import argparse
from collections import namedtuple
import os
import pstats
import sys


FunctionStats = namedtuple('FunctionStats', ['calls', 'tottime', 'cumtime',
        'path', 'function_name', 'line_number', 'stat'])


class Node(object):

    def __init__(self, stats=None):
        self.name_part = ""
        self.children = {}
        self.total_calls = 0
        self.total_time = 0.0
        self.function_stats = None
        self.stats = stats

    def add_stats(self, name_parts, function_stats):
        self.total_calls += function_stats.calls
        self.total_time += function_stats.tottime

        if len(name_parts) == 1:
            # This is a leaf
            self.function_stats = function_stats
        else:
            name_part = name_parts[0]
            self.name_part = name_part

            child_name_part = name_parts[1]

            if child_name_part not in self.children:
                self.children[child_name_part] = Node()
            self.children[child_name_part].add_stats(name_parts[1:], function_stats)


def create_parser():
    parser = argparse.ArgumentParser(description='Analyze cprofile .prof files.')
    parser.add_argument('path', metavar='PATH',
            help='the path of the *.prof file')
    parser.add_argument('--prefixes',
            help='virtualenv or python prefixes used to extract package name.')
    parser.add_argument('--filters',
            help='only print packages specified in filter.')
    parser.add_argument('--print-children', action='store_true',
            help='print children of packages')
    return parser


def get_stats(path):
    stats = pstats.Stats(path)
    return stats


def get_name_parts(path, prefixes, function_id):
    for prefix in prefixes:
        if path.startswith(prefix):
            path = path[len(prefix):]
            break

    if not path.startswith('/'):
        path = '/' + path

    path += '/' + function_id

    return path.split('/')


def print_node(key, node, print_children):
    print("Stats for {0}".format(key))
    print("  {0} total calls in {1:.3f} seconds".format(node.total_calls,
        node.total_time))

    if print_children:
        children = sorted(node.children.values(), key=lambda c: c.total_time,
                reverse=True)
        for child in children:
            print("    {0}: {1} total calls in {2:.3f} seconds".format(
                    child.name_part, child.total_calls, child.total_time))


def get_node(tree, node_filter):
    names = node_filter.split(":")
    try:
        node = tree
        for name in names:
            node = node.children[name]
        return node
    except Exception:
        return None


def print_report(tree, filters=None, print_children=False):
    print("Report for {0}\n".format(tree.stats.files[0]))
    print("{0} total calls in {1:.3f} seconds\n".format(tree.stats.total_calls,
            tree.stats.total_tt))
    print("{0} total calls in {1:.3f} seconds recorded in Tree\n".format(
            tree.total_calls, tree.total_time))
    if not filters:
        for key, child in tree.children.items():
            print_node(key, child, print_children)

    else:
        for node_filter in filters:
            node = get_node(tree, node_filter)
            if node:
                print_node(node_filter, node, print_children)


def main(program_args):
    parser = create_parser()
    args = parser.parse_args(program_args)
    stats = get_stats(args.path)

    prefixes = []
    if args.prefixes:
        prefixes = args.prefixes.split(',')
    else:
        # Compute prefixes with sys.path
        for path in sys.path:
            if path:
                prefixes.append(path)
            else:
                prefixes.append(os.getcwd())
        prefixes.sort(key=lambda p: len(p), reverse=True)

    filters = []
    if args.filters:
        filters = args.filters.split(',')

    tree = Node(stats)

    for (function_info, stats_info) in stats.stats.items():
        function_stats = FunctionStats(calls=stats_info[0],
                tottime=stats_info[2], cumtime=stats_info[3],
                path=function_info[0], function_name=function_info[2],
                line_number=function_info[1], stat=(function_info, stats_info))
        function_id = "{0}-{1}".format(function_stats.function_name,
                function_stats.line_number)
        name_parts = get_name_parts(function_info[0], prefixes,
                function_id)
        tree.add_stats(name_parts, function_stats)

    print_report(tree, filters, args.print_children)

    return tree


if __name__ == "__main__":
    main(sys.argv[1:])
