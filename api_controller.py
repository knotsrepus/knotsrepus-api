import base64
import json
import mimetypes
import os

import boto3

import rest


class ApiController:
    def __init__(self, bucket_name, region_name):
        self.bucket_name = bucket_name
        self.session = boto3.Session(region_name=region_name)

    @rest.route(path="/submission")
    def get_all_submissions(self, **kwargs):
        s3 = self.session.client("s3")
        paginator = s3.get_paginator("list_objects")
        results = paginator.paginate(Bucket=self.bucket_name, Delimiter="/")

        return "application/json", [result["Prefix"].replace("/", "") for result in results.search("CommonPrefixes")]

    @rest.route(path="/submission/{submission_id}")
    def get_submission(self, submission_id, **kwargs):
        s3 = self.session.resource("s3")
        data = self.__get_object_data(s3, f"{submission_id}/post.json")

        if data is not None:
            return "application/json", json.loads(data)

        return None

    @rest.route(path="/submission/{submission_id}/comments")
    def get_comments(self, submission_id, **kwargs):
        s3 = self.session.resource("s3")
        data = self.__get_object_data(s3, f"{submission_id}/comments.json")

        if data is not None:
            return "application/json", json.loads(data)

        return None

    @rest.route(path="/submission/{submission_id}/media")
    def get_media_list(self, submission_id, **kwargs):
        s3 = self.session.client("s3")
        paginator = s3.get_paginator("list_objects")
        results = paginator.paginate(Bucket=self.bucket_name, Delimiter="/", Prefix=f"{submission_id}/")

        return "application/json", [
            os.path.basename(result["Key"])
            for result in results.search("Contents")
            if result["Key"].endswith(".json") is False
        ]

    @rest.route(path="/submission/{submission_id}/media/{filename}")
    def get_media_object(self, submission_id, filename, **kwargs):
        s3 = self.session.resource("s3")
        data = self.__get_object_data(s3, f"{submission_id}/{filename}")

        if data is not None:
            content_type, _ = mimetypes.guess_type(filename)
            return content_type, base64.b64encode(data).decode("utf-8")

        return None

    def __get_object_data(self, s3, key):
        obj = s3.Object(self.bucket_name, key)

        if obj.last_modified is None:
            return None

        return obj.get()["Body"].read()
