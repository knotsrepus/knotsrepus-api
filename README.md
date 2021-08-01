# knotsrepus-api

An API for retrieving submissions archived by [knotsrepus-archiver](https://github.com/knotsrepus/knotsrepus-archiver).

## Getting Started

### Dependencies

- Python 3.8+
- pip
- An AWS account (required for deployment)

### Installing

```shell
git clone https://github.com/knotsrepus/knotsrepus-api.git
cd knotsrepus-api/
python -m pip install -r requirements.txt
```

### Running

Ensure you have suitable credentials defined in `~/.aws/credentials`.

```shell
lambda invoke -v
```

### Deployment

To deploy the Lambda function, use:

```shell
lambda deploy
```

To set up the API, use the "Import Rest API" wizard in the AWS API Gateway management console.
Select "Import from Swagger or Open API 3" and upload [the API spec file](openapi.yaml).
Note that you will have to manually assign permissions for the API to access the Lambda function.

## Contributors

- KNOTSREPUS (aka [/u/VoxUmbra](https://reddit.com/u/VoxUmbra))

## License

This project is licensed under the Apache License 2.0.
