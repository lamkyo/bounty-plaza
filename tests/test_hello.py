import pytest
from django.test import Client
from django.urls import reverse


@pytest.fixture
def client() -> Client:
    return Client()


def test_root_returns_hello_world(client: Client) -> None:
    response = client.get(reverse("hello:hello-world"))

    assert response.status_code == 200
    assert response.content == b"Hello, world!"
    assert response["Content-Type"] == "text/plain; charset=utf-8"


def test_root_rejects_post_requests(client: Client) -> None:
    response = client.post(reverse("hello:hello-world"))

    assert response.status_code == 405


def test_root_does_not_redirect(client: Client) -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert "Location" not in response


def test_root_handles_query_strings_without_changing_greeting(client: Client) -> None:
    response = client.get("/?name=Codex")

    assert response.status_code == 200
    assert response.content == b"Hello, world!"


def test_root_rejects_put_requests(client: Client) -> None:
    response = client.put(reverse("hello:hello-world"), data="payload", content_type="text/plain")

    assert response.status_code == 405


def test_unknown_path_returns_not_found(client: Client) -> None:
    response = client.get("/does-not-exist/")

    assert response.status_code == 404
