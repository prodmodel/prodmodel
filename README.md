# Prodmodel

Prodmodel is a [build system](https://en.wikipedia.org/wiki/List_of_build_automation_software) for data science pipelines.

## Concepts

A build system is a [DAG](https://en.wikipedia.org/wiki/Directed_acyclic_graph) of `rule`s (transformations), `input`s and `output`s.
In Prodmodel your `input`s can be
 * data,
 * any Python code,
 * and configuration.

A `rule` is transforming any of the above to an output (which can in turn be depended on by other rules). Therefore rules need to be
re-executed (and their outputs re-created) if any of their dependencies change. Prodmodel keeps track of these dependencies instead of you.

Prodmodel therefore ensures
 * correctness by executing every code (feature transformation, model building, tests) which can potentially be affected by a change,
 * performance by executing only the necessary code, saving time compared to rerunning the whole pipeline.

Partial results are also version controlled and cached.

### Rules

Every rule is a statically typed function, where the inputs are references to other rules, data, or configs. The execution of
a rule outputs some data (e.g. a different feature set or a model), which can be used in other rules.

In order to use Prodmodel your code has to be structured as functions which the rules can call into.

## Installation

Prodmodel requires at least Python3.6. Use [pip](https://pip.pypa.io/en/stable/) to install prodmodel.

```bash
pip install prodmodel --user
```

## Usage

Create a `build.py` file in your data science folder. The build file contains references to your inputs and the build rules you can execute.

```python
import rules

csv_data = rules.data_source(file='data.csv', type='csv', dtypes={...})

my_model = rules.transform(objects={'data': csv_data}, file='kmeans.py', fn='compute_kmeans')
```

Now you can build your model by running `prodmodel my_model` from the directory of your code,
or `prodmodel <path_to_my_directory>:my_model` from any directory.

Check out a complete [example project](https://github.com/prodmodel/prodmodel/tree/master/example) for more clarification.

The complete list of build rules can be found [here](https://github.com/prodmodel/prodmodel/blob/master/doc/api_doc.md).

### Arguments

 * `--force_external`: Some data sources are remote (e.g. an SQL server), therefore tracking changes is not always feasible.
   This argument gives the user manual control over when to reload these data sources.
 * `--cache_data`: Cache local data files if changed. This can be useful for debugging / reproducibility by making sure every
   data source used for a specific build is saved.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[Apache 2.0](https://github.com/prodmodel/prodmodel/blob/master/LICENCE)
