# coding:utf-8

import bs4

from data_parser.template import PopulationGroup, PopulationLevel


def parse_population_levels(tags: bs4.Tag) -> list:
    population_levels = []
    for tag in tags:
        population_levels.append(PopulationLevel(tag).values)
    return population_levels


def parse_population_groups(tags: bs4.Tag) -> list:
    population_groups = []
    for tag in tags:
        population_groups.append(PopulationGroup(tag).values)
    return population_groups
