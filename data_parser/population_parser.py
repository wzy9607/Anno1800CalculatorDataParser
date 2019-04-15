# coding:utf-8

import bs4

from data_parser.template import Need, PopulationGroup, PopulationLevel, ProductInStream


def parse_population_levels(tags: bs4.Tag) -> list:
    population_levels = []
    for tag in tags:
        node = tag.Values
        needs = parse_needs(node.PopulationLevel7.PopulationInputs("Item"))
        outputs = parse_outputs(node.PopulationLevel7.PopulationOutputs("Item"))
        population_levels.append(PopulationLevel.parse(node, needs = needs, outputs = outputs))
    return population_levels


def parse_needs(tags: bs4.Tag) -> list:
    needs = []
    for tag in tags:
        node = tag
        needs.append(Need.parse(node))
    return needs


def parse_outputs(tags: bs4.Tag) -> list:
    outputs = []
    for tag in tags:
        node = tag
        outputs.append(ProductInStream.parse(node))
    return outputs


def parse_population_groups(tags: bs4.Tag) -> list:
    population_groups = []
    for tag in tags:
        node = tag.Values
        population_groups.append(PopulationGroup.parse(node))
    return population_groups
