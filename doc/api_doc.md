# Build rules

## create_label_encoder

`create_label_encoder(data: IterableDataTarget, columns: List[str]) -> LabelEncoderTarget`<br/>

Creates a label encoder from the input `data` stream for the specified `columns`.<br>


## data_file

`data_file(file: str) -> DataTarget`<br/>

Local binary data source `file`.<br>


## data_stream

`data_stream(file: str, data_type: str, dtypes: dict, output_format: str) -> IterableDataTarget`<br/>

Local data source `file`; `data_type` has to be one of [csv, json], `dtypes` is a type specification for the columns in the file.<br>

The output of the target is specified by `output_format`:<br>

 * `pickle` (default): a numpy array of arrays (serialized with pickle),<br>

 * `json`: a list of dicts (serialzed as JSON).<br>


## deploy_target

`deploy_target(data: Target, deploy_path: str) -> DeployTarget`<br/>

Deploys the output of `data` to `deploy_path`.<br>


## encode_labels

`encode_labels(data: IterableDataTarget, label_encoder: LabelEncoderTarget, output_format: str) -> IterableDataTarget`<br/>

Encodes the label values in `data` with `label_encoder`.<br>

The output of the target is specified by `output_format`:<br>

 * `pickle` (default): a numpy array of arrays (serialized with pickle),<br>

 * `json`: a list of dicts (serialzed as JSON).<br>


## external_data

`external_data(file: str, fn: str, args: Dict[str, str], file_deps: List[str]) -> DataTarget`<br/>

Loads an external dataset by calling `fn` in `file` called with `args`.<br>

Any local imported module has to be specified in `file_deps`, except for the packages coming from requirements.<br>


## requirements

`requirements(packages: List[str])`<br/>

List of Python `packages` used by the project.<br>


## split

`split(data: IterableDataTarget, test_ratio: float, target_column: str, seed: int, output_format: str) -> Tuple[IterableDataTarget, IterableDataTarget, IterableDataTarget, IterableDataTarget]`<br/>

Splits the source `data` into train X, train y, test X and test y data, respectively. Params:<br>

 * `test_ratio`: [0, 1], the ratio of the test dataset (1 - test_ratio for the train dataset),<br>

 * `target_column`: the name of the target variable included only in the test set,<br>

 * `seed`: random seed for the sampling.<br>

The output of the target is specified by `output_format`:<br>

 * `pickle` (default): a numpy array of arrays (serialized with pickle),<br>

 * `json`: a list of dicts (serialzed as JSON).<br>


## test

`test(test_file: str, file_deps: List[str]) -> TestTarget`<br/>

Runs the tests in `test_file`.<br>

Any local imported module has to be specified in `file_deps`, except for the packages coming from requirements.<br>


## transform

`transform(file: str, fn: str, streams: Dict[str, IterableDataTarget], objects: Dict[str, DataTarget], file_deps: List[str]) -> DataTarget`<br/>

Transforms the input data sets into another one. The function `fn` defined in `file` has to have an argument for every key defined in `streams` (list of dicts) and `objects` (the outputs of the dict value targets).<br>

Any local imported module has to be specified in `file_deps`, except for the packages coming from requirements.<br>


## transform_stream

`transform_stream(file: str, fn: str, stream: IterableDataTarget, objects: Dict[str, DataTarget], file_deps: List[str], output_format: str) -> IterableDataTarget`<br/>

Maps the input data `stream` into another one. The function `fn` defined in `file` has to accept a dict as a first argument and return a dict. The rest of its arguments have to be the keys of `objects` - the outputs of the dict value targets will be substituted at runtime.<br>

Any local imported module has to be specified in `file_deps`, except for the packages coming from requirements.<br>

The output of the target is specified by `output_format`:<br>

 * `pickle` (default): a numpy array of arrays (serialized with pickle),<br>

 * `json`: a list of dicts (serialzed as JSON).<br>


## copy_to_s3

`copy_to_s3(data: Target, s3_bucket: str, s3_key: str) -> S3DataTarget`<br/>

Copies the result of `data` target to `s3_bucket`/`s3_key`. The S3 credentials come from the AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY env vars.<br>


