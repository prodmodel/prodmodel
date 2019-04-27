# Build rules

## create_label_encoder(data:model.target.iterable_data_target.IterableDataTarget, columns:List[str]) -> model.target.label_encoder_target.LabelEncoderTarget
Creates a label encoder from the input `data` stream for the specified `columns`.

## data_source(file:str, type:str, dtypes:dict) -> model.target.iterable_data_target.IterableDataTarget
Local data source file. Type has to be one of [csv], dtypes is a type specification for the columns in the file.

## encode_labels(data:model.target.iterable_data_target.IterableDataTarget, label_encoder:model.target.label_encoder_target.LabelEncoderTarget) -> model.target.iterable_data_target.IterableDataTarget
Encodes the label values in `data` with `label_encoder`.

## external_data(file:str, fn:str, args:Dict[str, str]) -> model.target.external_data_target.ExternalDataTarget
Loads an external dataset by calling `fn` in `file` called with `args`.

## requirements(packages:List[str])
List of Python packages used by the project.

## split(data:model.target.iterable_data_target.IterableDataTarget, test_ratio:float, target_column:str, seed:int=0) -> Tuple[model.target.iterable_data_target.IterableDataTarget, model.target.iterable_data_target.IterableDataTarget, model.target.iterable_data_target.IterableDataTarget, model.target.iterable_data_target.IterableDataTarget]
Splits the source data into train X, train y, test X and test y data, respectively.

## test(test_file:str, file_deps:List[str])
Runs the tests in `test_file`. Any module imported in file has to be specified in `file_deps`.

## transform(file:str, fn:str, streams:Dict[str, model.target.iterable_data_target.IterableDataTarget]={}, objects:Dict[str, model.target.data_target.DataTarget]={}, file_deps:List[str]=[]) -> model.target.data_target.DataTarget
Transforms the input data sets into another one. The function `fn` defined in `file` has to have an argument for every key defined in `streams` (passed in as list of dicts) and `objects` (passed in the same format as they are created). Any module imported in file has to be specified in `file_deps`.

## transform_stream(file:str, fn:str, stream:model.target.iterable_data_target.IterableDataTarget, objects:Dict[str, model.target.data_target.DataTarget]={}, file_deps:List[str]=[]) -> model.target.iterable_data_target.IterableDataTarget
Maps the input data stream into another one. The function `fn` defined in `file` has to accept a dict as a first argument and return a dict. The rest of its arguments are coming from `objects`. Any module imported in file has to be specified in `file_deps`.

## copy_to_s3(data:model.target.target.Target, s3_bucket:str, s3_key:str) -> model.target.s3_data_target.S3DataTarget
Copies the result of `data` target to `s3_bucket`/`s3_key`. The S3 credentials come from the AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY env vars.

