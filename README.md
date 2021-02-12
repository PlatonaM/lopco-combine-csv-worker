#### Description

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