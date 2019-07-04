![Prodmodel](https://github.com/prodmodel/prodmodel/blob/master/logo.png)

Prodmodel is a [build system](https://en.wikipedia.org/wiki/List_of_build_automation_software) for data science pipelines.
Users, testers, contributors are welcome!

<p align="center">
  <a href="https://pypi.org/project/prodmodel">
    <img src="https://img.shields.io/pypi/v/prodmodel.svg"></img></a>
  <a href="https://pypi.org/project/prodmodel" alt="Downloads">
    <img src="https://img.shields.io/pypi/dd/prodmodel.svg" /></a>
  <a href="https://github.com/prodmodel/prodmodel/graphs/contributors" alt="Contributors">
    <img src="https://img.shields.io/github/contributors/prodmodel/prodmodel.svg" /></a>
  <a href="https://github.com/prodmodel/prodmodel/pulse" alt="Activity">
    <img src="https://img.shields.io/github/commit-activity/m/prodmodel/prodmodel.svg" /></a>
  <a href="https://github.com/prodmodel/prodmodel/issues" alt="Issues">
    <img src="https://img.shields.io/github/issues/prodmodel/prodmodel.svg" /></a>
  <a href="https://github.com/prodmodel/prodmodel/issues?utf8=%E2%9C%93&q=is%3Aissue+is%3Aclosed" alt="Closed issues">
    <img src="https://img.shields.io/github/issues-closed/prodmodel/prodmodel.svg" /></a>
  <a href="https://github.com/prodmodel/prodmodel/pulls" alt="Pulls">
    <img src="https://img.shields.io/github/issues-pr/prodmodel/prodmodel.svg" /></a>
</p>

<h3 align="center">
  <a href="#motivation">Motivation</a>
  <span> · </span>
  <a href="#concepts">Concepts</a>
  <span> · </span>
  <a href="#installation">Installation</a>
  <span> · </span>
  <a href="#usage">Usage</a>
  <span> · </span>
  <a href="#contributing">Contributing</a>
  <span> · </span>
  <a href="#contact">Contact</a>
  <span> · </span>
  <a href="#licence">Licence</a>
</h3>

## Motivation

 * Performance. No need to rerun things, everything is cached, switching between multiple versions is super easy. Prodmodel can
   **figure out if a particular partial code path has already been executed using a particular piece of data** and just use the cached output.
 * Easy debugging. Every single dependency - code or data - is version controlled and tracked.
 * Deploy to production. Models are more than just a file. Prodmodel makes sure that the correct version of label encoders,
   feature transformation code and data and model files are all packaged together.

## Concepts

A build system is a [DAG](https://en.wikipedia.org/wiki/Directed_acyclic_graph) of `rules` (transformations), `inputs` and `targets`.
In Prodmodel `inputs` can be
 * data,
 * Python code,
 * and configuration.

A `rule` is transforming any of the above to an output (which can in turn be depended on by other rules). Therefore rules need to be
re-executed (and their outputs re-created) if any of their dependencies change. Prodmodel keeps track all of these dependencies.

The outputs of the `rules` are `targets`. Every `target` corresponds to an output (e.g. a model or a dataset). These outputs
are cached and version controlled.

Prodmodel therefore ensures
 * correctness, by executing every code (e.g. feature transformation, model building, tests) which can potentially be affected by a change, and
 * performance, by executing only the necessary code, saving time compared to rerunning the whole pipeline.

### Rules

Every rule is a statically typed function, where the inputs are targets, data, or configs. The execution of
a rule outputs some data (e.g. a different feature set or a model), which can be used in other rules.

In order to use Prodmodel your code has to be structured as functions which the rules can call into.

### Targets

Targets are created by rule functions. Targets can be executed to generate output files. `IterableDataTarget` is a special target
which can be used as an iterable of `dicts` to make iterating over datasets easier. Regular `DataTargets` can represent any
Python object.

## Installation

Prodmodel requires at least Python3.6. Use [pip](https://pip.pypa.io/en/stable/) to install prodmodel.

```bash
pip install prodmodel --user
```

## Usage

Create a `build.py` file in your data science folder. The build file contains references to your inputs and the build rules you can execute.

```python
from prodmodel.rules import rules

csv_data = rules.data_source(file='data.csv', type='csv', dtypes={...})

my_model = rules.transform(objects={'data': csv_data}, file='kmeans.py', fn='compute_kmeans')
```

Now you can build your model by running `prodmodel my_model` from the directory of `build.py`,
or `prodmodel <path_to_my_directory>:my_model` from any directory.

Prodmodel creates a `.prodmodel` directory under the home directory of the user to store log and config files.

### Documentation

Check out a complete [example project](https://github.com/prodmodel/prodmodel/tree/master/example) for more examples.

The complete list of build rules can be found [here](https://github.com/prodmodel/prodmodel/blob/master/doc/api_doc.md).

Prodmodel searches for a config file under `<user home dir>/.prodmodel/config`. The config file can be created manually
based on this [template](https://github.com/prodmodel/prodmodel/blob/master/doc/config).

### Arguments

 * `--force_external`: Some data sources are remote (e.g. an SQL server), therefore tracking changes is not always feasible.
   This argument gives the user manual control over when to reload these data sources.
 * `--cache_data`: Cache local data files if changed. This can be useful for debugging / reproducibility by making sure every
   data source used for a specific build is saved.
 * `--output_format`: One of `none`, `str`, `bytes` and `log`. The output format of the data produced by the build target
   written to stdout.

### List targets in build file

 * Run `prodmodel ls <path_to_build>` to list targets in a build file where `<path_to_build>` to the build file or its directory.

### Cleaning old cache files

 * Run `prodmodel clean <target> --cutoff_date=<cutoff datetime>` to delete output cache files of a target created before
   the cutoff datetime, which has to be in `%Y-%m-%dT%H:%M%S` (`YYYY-mm-ddTHH:MM:SS`) format.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Contact
Feel free to email me at gergely.svigruha@prodmodel.com if you have any question, need help or would like to contribute to the code.

## Licence
[Apache 2.0](https://github.com/prodmodel/prodmodel/blob/master/LICENCE)
