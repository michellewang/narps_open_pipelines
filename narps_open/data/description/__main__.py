#!/usr/bin/python
# coding: utf-8

""" Provide a command-line interface for the package narps_open.data.description """

from argparse import ArgumentParser
from json import dumps

from narps_open.data.description import TeamDescription

# Parse arguments
parser = ArgumentParser(description='Get description of a NARPS pipeline.')
parser.add_argument('-t', '--team', type=str, required=True,
    help='the team ID')
parser.add_argument('-d', '--dictionary', type=str, required=False,
    choices=[
        'general',
        'exclusions',
        'preprocessing',
        'analysis',
        'categorized_for_analysis',
        'derived'
        ],
    help='the sub dictionary of team description')
arguments = parser.parse_args()

# Initialize a TeamDescription
information = TeamDescription(team_id = arguments.team)

if arguments.dictionary == 'general':
    print(dumps(information.general, indent = 4))
elif arguments.dictionary == 'exclusions':
    print(dumps(information.exclusions, indent = 4))
elif arguments.dictionary == 'preprocessing':
    print(dumps(information.preprocessing, indent = 4))
elif arguments.dictionary == 'analysis':
    print(dumps(information.analysis, indent = 4))
elif arguments.dictionary == 'categorized_for_analysis':
    print(dumps(information.categorized_for_analysis, indent = 4))
elif arguments.dictionary == 'derived':
    print(dumps(information.derived, indent = 4))
else:
    print(dumps(information, indent = 4))
