# launch_moos

[![License](https://img.shields.io/pypi/l/launch_moos)][license]

[![Read the documentation at https://launch_moos.readthedocs.io/](https://img.shields.io/readthedocs/launch_moos/latest.svg?label=Read%20the%20Docs)][read the docs]
[![Tests](https://github.com/russkel/launch_moos/workflows/Tests/badge.svg)][tests]

[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[read the docs]: https://launch_moos.readthedocs.io/
[tests]: https://github.com/russkel/launch_moos/actions?workflow=Tests
[black]: https://github.com/psf/black

## Features

- Use ROS2 `launch` tooling to bring up MOOS communities using your existing MOOS files.
- Convert `.moos` mission files into Python based launch files.
- Proper logging of `stderr` and `stdout` using `launch` logging.
- No more antiquated `pAntler`! 

## Requirements

- ROS2 launch
- MOOS-IvP

## Installation

You can install _launch.moos_ via [pip] from [PyPI]:

```console
$ pip install launch_moos
```

## Usage

Please see the [Command-line Reference] for details.

## Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide].

## License

Distributed under the terms of the [MIT license][license],
_launch.moos_ is free and open source software.

## Issues

If you encounter any problems,
please [file an issue] along with a detailed description.

[file an issue]: https://github.com/russkel/launch_moos/issues
[pip]: https://pip.pypa.io/

<!-- github-only -->

[license]: https://github.com/russkel/launch_moos/blob/main/LICENSE
[contributor guide]: https://github.com/russkel/launch_moos/blob/main/CONTRIBUTING.md
[command-line reference]: https://launch_moos.readthedocs.io/en/latest/usage.html
