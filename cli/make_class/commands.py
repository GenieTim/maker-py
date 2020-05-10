import errno
import os

import click

from utils import clean_variable_name as cvn


@click.command()
@click.option(
    '--classname',
    required=True,
    type=click.STRING,
    prompt=True
)
@click.option(
    '--properties',
    required=False,
    type=click.STRING,
    prompt=True,
    multiple=True
)
def make_class(classname, properties):
    namespaces = classname.split('.')
    class_str = "class " + \
        namespaces[len(namespaces)-1].capitalize() + "(object):\n"
    # ugly workaround from https://github.com/pallets/click/issues/218
    properties = ''.join(properties).split(' ') if all(
        len(x) == 1 for x in properties) else properties
    # make sure they do not contain special characters
    properties = [cvn.clean_variable_name(x) for x in properties]
    # overloaded constructor
    class_str += "  def __init__(self, " + \
        "=None, ".join(properties) + "=None):\n"
    for property_name in properties:
        class_str += "    if " + property_name + " is None:\n"
        class_str += "      # TODO: set default value\n"
        class_str += "      self._" + property_name + " = None\n"
        class_str += "    else:\n"
        class_str += "      self._" + property_name + " = " + property_name + "\n"
    # getter & setter
    for property_name in properties:
        class_str += "\n"
        # getter
        class_str += "  @property\n"
        class_str += "  def " + property_name + "(self):\n"
        class_str += "    return self._" + property_name + "\n"
        # setter
        class_str += "\n"
        class_str += "  @" + property_name + ".setter\n"
        class_str += "  def " + property_name + "(self, value):\n"
        class_str += "    self._" + property_name + " = value\n"
    filename = "/".join(namespaces) + ".py"
    if os.path.dirname(filename) != "" and not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    with open(filename, "w") as f:
        f.write(class_str)

    print("Wrote file: {}".format(filename))
