"""Module for the PythonLaunchDescriptionSource class."""

from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec
from importlib.util import spec_from_loader
from types import ModuleType
from typing import Text

from launch.launch_description import LaunchDescription
from launch.launch_description_source import LaunchDescriptionSource
from launch.some_substitutions_type import SomeSubstitutionsType


class MOOSMissionFileDescriptionSource(LaunchDescriptionSource):
    """Encapsulation of a Python launch file, which can be loaded during launch."""

    def __init__(
        self,
        mission_file_path: SomeSubstitutionsType,
    ) -> None:
        """
        Create a PythonLaunchDescriptionSource.

        The given file path should be to a ``.moos`` mission file.
        The path should probably be absolute, since the current working
        directory will be wherever the launch file was run from, which might
        change depending on the situation.
        The path can be made up of Substitution instances which are expanded
        when :py:meth:`get_launch_description()` is called.

        :param mission_file_path: the path to the moos mission file
        """
        super().__init__(None, mission_file_path, "interpreted MOOS mission file")

    def _get_launch_description(self, location) -> LaunchDescription:
        """Get the LaunchDescription from location."""
        return get_launch_description_from_python_launch_file(location)


class InvalidPythonLaunchFileError(Exception):
    """Exception raised when the given Python launch file is not valid."""

    ...


def load_python_launch_file_as_module(python_launch_file_path: str) -> ModuleType:
    """Load a given Python launch file (by path) as a Python module."""
    loader = SourceFileLoader("python_launch_file", python_launch_file_path)
    spec = spec_from_loader(loader.name, loader)
    mod = module_from_spec(spec)
    loader.exec_module(mod)
    return mod


def get_launch_description_from_python_launch_file(python_launch_file_path: str):
    """
    Load a given Python launch file (by path), and return the launch description from it.
    Python launch files are expected to have a `.py` extension and must provide
    a function within the module called `generate_launch_description()`.
    This function is called after loading the module to get the single
    :class:`launch.LaunchDescription` class from it.
    The signature of the function should be as follows:
    .. code-block:: python
        def generate_launch_description() -> launch.LaunchDescription:
            ...
    The Python launch file, as much as possible, should avoid side-effects.
    Keep in mind that the reason it is being loaded may be just to introspect
    the launch description and not necessarily to execute the launch itself.
    """
    launch_file_module = load_python_launch_file_as_module(python_launch_file_path)
    if not hasattr(launch_file_module, "generate_launch_description"):
        raise InvalidPythonLaunchFileError(
            "launch file at '{}' does not contain the required function '{}'".format(
                python_launch_file_path, "generate_launch_description()"
            )
        )
    return getattr(launch_file_module, "generate_launch_description")()
