import click

from make_class import commands as group1
from make_interface import commands as group2


@click.group()
def entry_point():
    pass


entry_point.add_command(group1.make_class)
entry_point.add_command(group2.make_interface)

if __name__ == '__main__':
    entry_point()
