import requests
import json
from process_request import ResponseCode
from process_request import lambda_handler

from aws_lambda_wrapper import AWSLambdaWrapper


API_ENDPOINT = "https://qnv2n0vzhc.execute-api.us-east-2.amazonaws.com/default/CitiesGame_ProcessRequest"


def test_aws_api():
    # TODO: write this code properly
    req = stub_request("")
    res = requests.post(API_ENDPOINT, data=req)

    print(res)


def test_local():
    req = stub_request(None)

    while req:
        response = lambda_handler(req, None)

        stub_response(response)
        req = stub_request(response)


def stub_request(response_object: object) -> object:
    if not response_object:
        city = input(f"Начинаем игру. Введите любой город: ")
    else:
        response_body = json.loads(response_object["body"])
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
    if response_body["isCorrect"]:
        print(f"Мой город - {response_body['CityName']}")


if __name__ == "__main__":
    test_local()
