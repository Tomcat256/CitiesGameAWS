import json

class AWSLambdaWrapper:

    @staticmethod
    def request_to_event(request_body: object) -> object:
        # event = {
        #     "body": json.dumps(request_body)
        # }

        return request_body

    @staticmethod
    def parse_api_response(response_object: object) -> object:
        return response_object
