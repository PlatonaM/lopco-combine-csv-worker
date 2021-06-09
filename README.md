## lopco-combine-csv-worker

Combine multiple CSV files into one CSV file.

### Configuration

`delimiter`: Delimiter used in the CSV file.

`time_column`: Name of column containing timestamps.

### Inputs

Type: multiple

_(dynamic)_ `source_file` / _(user defined via GUI)_ `_{number}_source_file`: CSV file to be added to result CSV file.

### Outputs

Type: single

`output_csv`: Result CSV file.

### Description

    {
        "name": "Combine CSV",
        "image": "platonam/lopco-combine-csv-worker:latest",
        "data_cache_path": "/data_cache",
        "description": "Combine multiple Comma-Separated Values files.",
        "configs": {
            "delimiter": null,
            "time_column": null
        },
        "input": {
            "type": "multiple",
            "fields": [
                {
                    "name": "source_file",
                    "media_type": "text/csv",
                    "is_file": true
                }
            ]
        },
        "output": {
            "type": "single",
            "fields": [
                {
                    "name": "output_csv",
                    "media_type": "text/csv",
                    "is_file": true
                }
            ]
        }
    }