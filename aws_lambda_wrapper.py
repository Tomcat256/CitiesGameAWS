import json

class AWSLambdaWrapper:

    @staticmethod
    def request_to_event(request_body: object) -> object:
        event = {
            "body": json.dumps(request_body)
        }

        return event

    @staticmethod
    def parse_api_response(response_object: object) -> object:
        response_body = json.loads(response_object["body"])
        return response_body
