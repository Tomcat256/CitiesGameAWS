import requests
import json
from process_request import ResponseCode
from process_request import lambda_handler

from aws_lambda_wrapper import AWSLambdaWrapper


API_ENDPOINT = "https://qnv2n0vzhc.execute-api.us-east-2.amazonaws.com/default/cities"
API_KEY = "XqF141eQuP5G06ZrpvbQb5dd4nmJuijH67lURjDo"


def request_aws_lambda(request_body: object) -> object:

    response_raw = requests.post(API_ENDPOINT, json=request_body)

    res = response_raw.json()

    return res


def request_local_code(request: object) -> object:
    return lambda_handler(request, None)


def main():
    req = client_interaction_stub(None)

    while req:
        # response = request_local_code(req)
        response = request_aws_lambda(req)

        stub_response(response)
        req = client_interaction_stub(response)


def client_interaction_stub(response_object: object) -> object:
    if not response_object:
        city = input(f"Начинаем игру. Введите любой город: ")
    else:
        response_body = response_object
        if response_body["ResponseCode"] == ResponseCode.GAME_OVER.name:
            return None
        city = input(f"Введите город на букву '{response_body['LastLetter']}': ")

    stub_request_object = {
        "userSessionId": "g9af097c17a8aac6",
        "requestText": city
    }

    return AWSLambdaWrapper.request_to_event(stub_request_object)


def stub_response(response_object: object):
    response_body = AWSLambdaWrapper.parse_api_response(response_object)
    print(response_body["ResponseCode"])

    if response_body["ResponseCode"] == ResponseCode.ANSWER_TO_USER.name:
        print(f"Мой город - {response_body['CityName']}")


if __name__ == "__main__":
    main()
