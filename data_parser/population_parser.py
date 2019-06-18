# coding:utf-8

import bs4

from data_parser.template import PopulationGroup, PopulationLevel


def parse_population_levels(tags: bs4.Tag) -> list:
    population_levels = [PopulationLevel(tag).get_values() for tag in tags]
    return population_levels


def parse_population_groups(tags: bs4.Tag) -> list:
    population_groups = [PopulationGroup(tag).get_values() for tag in tags]
    return population_groups
