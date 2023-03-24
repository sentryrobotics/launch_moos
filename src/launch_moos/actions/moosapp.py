import pathlib
from tempfile import NamedTemporaryFile
from typing import Dict
from typing import Iterable
from typing import List
from typing import Optional
from typing import Text  # noqa: F401
from typing import Tuple  # noqa: F401

from launch.action import Action
from launch.actions import ExecuteProcess
from launch.frontend import Entity
from launch.frontend import Parser
from launch.frontend import expose_action
from launch.launch_context import LaunchContext
from launch.some_substitutions_type import SomeSubstitutionsType
from launch.substitutions import LocalSubstitution

from ..moosfile_generator import evaluate_template


@expose_action("moosapp")
class MOOSApp(ExecuteProcess):
    """Action that executes a MOOS App."""

    def __init__(
        self,
        *,
        executable: SomeSubstitutionsType,
        name: Optional[SomeSubstitutionsType] = None,
        alias: Optional[SomeSubstitutionsType] = None,
        arguments: Optional[Iterable[SomeSubstitutionsType]] = None,
        mission_file: Optional[SomeSubstitutionsType] = None,
        global_config: Optional[List[Tuple[str, SomeSubstitutionsType]]] = None,
        config: Optional[List[Tuple[str, SomeSubstitutionsType]]] = None,
        **kwargs
    ) -> None:
        """
        Construct a MOOS Application action.

        Many arguments are passed eventually to
        :class:`launch.actions.ExecuteProcess`, so see the documentation of
        that class for additional details.
        However, the `cmd` is not meant to be used, instead use the
        `executable` and `arguments` keyword arguments to this function.

        This action, once executed, delegates most work to the
        :class:`launch.actions.ExecuteProcess`, but it also converts some ROS
        specific arguments into generic command line arguments.

        If the name is not given (or is None) then no name is passed to
        the MOOS App on creation and instead the default name specified within the
        code of the app is used instead.

        :param: executable the name of the MOOS App to run.
        :param: name the label used to represent the process. Defaults to the basename of the MOOS App.
        :param: alias the alias passed to the MOOS App.
        :param: arguments list of extra arguments for the node
        :param: mission_file path to the MOOS mission file that is passed to the app
        :param: config list of configuration lines for the app
        :param: global_config list of configuration lines for the app
        """
        cmd = [executable]
        cmd += [LocalSubstitution("mission_file", description="MOOS App Mission File")]

        if alias:
            cmd += [LocalSubstitution("alias", description="MOOS App Alias")]

        cmd += arguments or []

        kwargs["name"] = name
        super().__init__(cmd=cmd, **kwargs)

        self.alias = alias
        self.mission_file = mission_file

        self.__app_executable = executable
        # self.__parameters = [] if parameters is None else normalized_params
        self.__arguments = arguments

        self.__global_config = global_config
        self.__config = config

        self.__expanded_parameter_arguments = (
            None
        )  # type: Optional[List[Tuple[Text, bool]]]
        self.__substitutions_performed = False

    @classmethod
    def parse(cls, entity: Entity, parser: Parser):
        """Parse node."""
        # See parse method of `ExecuteProcess`
        _, kwargs = super().parse(entity, parser, ignore=["cmd"])
        args = entity.get_attr("args", optional=True)
        if args is not None:
            kwargs["arguments"] = super()._parse_cmdline(args, parser)

        alias = entity.get_attr("alias", optional=True)
        if alias is not None:
            kwargs["alias"] = parser.parse_substitution(alias)

        node_name = entity.get_attr("name", optional=True)
        if node_name is not None:
            kwargs["name"] = parser.parse_substitution(node_name)

        executable = entity.get_attr("executable", optional=True)
        if executable is not None:
            kwargs["executable"] = parser.parse_substitution(executable)

        kwargs["executable"] = parser.parse_substitution(entity.get_attr("exec"))

        # parameters = entity.get_attr('param', data_type=List[Entity], optional=True)
        # if parameters is not None:
        #     kwargs['parameters'] = cls.parse_nested_parameters(parameters, parser)

        return cls, kwargs

    @staticmethod
    def Create_moos_file(
        process_name: str,
        config: List[Tuple[str, str]],
        global_config: List[Tuple[str, str]] = None,
    ) -> str:
        with NamedTemporaryFile(
            mode="w", prefix="launch_moos_", suffix=".moos", delete=False
        ) as h:
            param_file_path = h.name
            h.write(
                evaluate_template(
                    {
                        "process_name": process_name,
                        "global_variables": global_config or [],
                        "process_variables": config or [],
                    }
                )
            )
            return param_file_path

    def _perform_substitutions(self, context: LaunchContext) -> None:
        if self.__substitutions_performed:
            # This function may have already been called by a subclass' `execute`, for example.
            return
        self.__substitutions_performed = True
        # if self.__node_name is not None:
        #     self.__expanded_node_name = perform_substitutions(
        #         context, normalize_to_list_of_substitutions(self.__node_name))
        #     validate_node_name(self.__expanded_node_name)
        # self.__expanded_node_name.lstrip('/')

        # Expand global parameters first,
        # so they can be overridden with specific parameters of this Node
        # The params_container list is expected to contain name-value pairs (tuples)
        # and/or strings representing paths to parameter files.
        params_container = context.launch_configurations.get("global_params", None)

        # if any(x is not None for x in (params_container, self.__parameters)):
        #     self.__expanded_parameter_arguments = []

        # if params_container is not None:
        #     for param in params_container:
        #         if isinstance(param, tuple):
        #             name, value = param
        #             cmd_extension = ['-p', f'{name}:={value}']
        #             self.cmd.extend([normalize_to_list_of_substitutions(x) for x in cmd_extension])
        #         else:
        #             param_file_path = os.path.abspath(param)
        #             self.__expanded_parameter_arguments.append((param_file_path, True))
        #             cmd_extension = ['--params-file', f'{param_file_path}']
        #             assert os.path.isfile(param_file_path)
        #             self.cmd.extend([normalize_to_list_of_substitutions(x) for x in cmd_extension])

        # expand parameters too
        # if self.__parameters is not None:
        #     evaluated_parameters = evaluate_parameters(context, self.__parameters)
        #     for params in evaluated_parameters:
        #         is_file = False
        #         if isinstance(params, dict):
        #             param_argument = self._create_params_file_from_dict(params)
        #             is_file = True
        #             assert os.path.isfile(param_argument)
        #         elif isinstance(params, pathlib.Path):
        #             param_argument = str(params)
        #             is_file = True
        #         elif isinstance(params, Parameter):
        #             param_argument = self._get_parameter_rule(params, context)
        #         else:
        #             raise RuntimeError('invalid normalized parameters {}'.format(repr(params)))
        #         if is_file and not os.path.isfile(param_argument):
        #             self.__logger.warning(
        #                 'Parameter file path is not a file: {}'.format(param_argument),
        #             )
        #             continue
        #         self.__expanded_parameter_arguments.append((param_argument, is_file))
        #         cmd_extension = ['--params-file' if is_file else '-p', f'{param_argument}']
        #         self.cmd.extend([normalize_to_list_of_substitutions(x) for x in cmd_extension])

    def execute(self, context: LaunchContext) -> Optional[List[Action]]:
        """
        Execute the action.

        Delegated to :meth:`launch.actions.ExecuteProcess.execute`.
        """
        # self._perform_substitutions(context)

        # Prepare the ros_specific_arguments list and add it to the context so that the
        # LocalSubstitution placeholders added to the the cmd can be expanded using the contents.
        # ros_specific_arguments: Dict[str, Union[str, List[str]]] = {}
        # if self.__node_name is not None:
        #     ros_specific_arguments['name'] = '__node:={}'.format(self.__expanded_node_name)

        if self.mission_file is None:
            # then we need to generate the moos file
            self.mission_file = MOOSApp.Create_moos_file(
                self.__app_executable, self.__config, self.__global_config
            )

        context.extend_locals({"alias": self.alias, "mission_file": self.mission_file})

        ret = super().execute(context)

        # if self.is_node_name_fully_specified():
        #     add_node_name(context, self.node_name)
        #     node_name_count = get_node_name_count(context, self.node_name)
        #     if node_name_count > 1:
        #         execute_process_logger = launch.logging.get_logger(self.name)
        #         execute_process_logger.warning(
        #             'there are now at least {} nodes with the name {} created within this '
        #             'launch context'.format(node_name_count, self.node_name)
        #         )

        return ret
