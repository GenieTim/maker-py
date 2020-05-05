import errno
import os

import click


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
    print(properties)
    for property_name in properties:
        class_str += "\n"
        # getter
        class_str += "  @property\n"
        class_str += "  def " + property_name + "(self):\n"
        class_str += "    return self._" + property_name + "\n"
        # setter
        class_str += "\n"
        class_str += "  @" + property_name + ".setter\n"
        class_str += "  def " + property_name + "(self):\n"
        class_str += "    self._" + property_name + " = value\n"
    filename = "/".join(namespaces) + ".py"
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    with open(filename, "w") as f:
        f.write(class_str)


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


@click.group()
def entry_point():
    pass


entry_point.add_command(make_class)
entry_point.add_command(make_interface)

if __name__ == '__main__':
    entry_point()
