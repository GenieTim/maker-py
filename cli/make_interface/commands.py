import errno
import os

import click

from utils import clean_variable_name as cvn


@click.command()
@click.option(
    '--classname',
    required=True,
    type=str,
    prompt=True
)
@click.option(
    '--functions',
    required=False,
    type=str,
    prompt=True,
    multiple=True
)
def make_interface(classname, functions):
    namespaces = classname.split('.')
    class_str = "class " + \
        namespaces[len(namespaces)].capitalize() + "(object):\n"
    # ugly workaround from https://github.com/pallets/click/issues/218
    functions = ''.join(functions).split(' ') if all(
        len(x) == 1 for x in functions) else functions
    # make sure they do not contain special characters
    functions = map(cvn.clean_variable_name, functions)
    for function_name in functions:
        class_str += "\n"
        class_str += "  @property\n"
        class_str += "  def " + function_name + "(self):\n"
        class_str += "    raise NotImplementedError(\"Should have implemented this\")\n"
    filename = "/".join(namespaces) + ".py"
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    with open(filename, "w") as f:
        f.write(class_str)
