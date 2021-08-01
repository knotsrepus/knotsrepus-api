# -*- coding: utf-8 -*-
import json
import os

import api_controller
import rest


def get_api_controller():
    bucket_name = os.environ.get("BUCKET_NAME")
    region_name = os.environ.get("REGION_NAME")

    return api_controller.ApiController(bucket_name, region_name)


def format_response(status_code, content_type, body):
    is_binary = any(prefix in content_type for prefix in ["image", "video", "audio"])

    return {
        "statusCode": status_code,
        "headers": {"Content-Type": content_type},
        "isBase64Encoded": is_binary,
        "body": body if is_binary else json.dumps(body)
    }


def dispatch_event_to_api_controller(event):
    resource = event.get("resource")

    if not rest.route_is_defined(resource):
        return format_response(400,
                               "application/json",
                               {"message": f"No controller function defined to handle resource '{resource}'"})

    api = get_api_controller()
    path_params = event.get("pathParameters") or dict()

    (content_type, body) = rest.dispatch(resource, api, **path_params)

    return format_response(200, content_type, body)


def handler(event, context):
    return dispatch_event_to_api_controller(event)


if __name__ == "__main__":
    print("This lambda function cannot be executed directly. Please use the 'lambda invoke' command to run this "
          "function.")
