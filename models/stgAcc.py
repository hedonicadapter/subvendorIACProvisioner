from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class Info:
    title: str
    version: str

@dataclass
class Schema:
    pass

@dataclass
class MediaType:
    schema: Dict[str, Any]

@dataclass
class Content:
    application_json: MediaType

    @staticmethod
    def from_dict(d: Dict[str, Any]):
        return Content(
            application_json=MediaType(schema=d.get("application/json", {}).get("schema", {}))
        )

@dataclass
class RequestBody:
    content: Content

    @staticmethod
    def from_dict(d: Dict[str, Any]):
        return RequestBody(
            content=Content.from_dict(d.get("content", {}))
        )

@dataclass
class Post:
    summary: str
    requestBody: RequestBody

    @staticmethod
    def from_dict(d: Dict[str, Any]):
        return Post(
            summary=d.get("summary", ""),
            requestBody=RequestBody.from_dict(d.get("requestBody", {}))
        )

@dataclass
class PathItem:
    post: Post

    @staticmethod
    def from_dict(d: Dict[str, Any]):
        return PathItem(
            post=Post.from_dict(d.get("post", {}))
        )

@dataclass
class Response:
    description: str

@dataclass
class RootRequestBody:
    openapi: str
    info: Info
    paths: Dict[str, PathItem]
    responses: Dict[str, Response]

    @staticmethod
    def from_dict(d: Dict[str, Any]):
        return RootRequestBody(
            openapi=d["openapi"],
            info=Info(**d["info"]),
            paths={k: PathItem.from_dict(v) for k, v in d.get("paths", {}).items()},
            responses={k: Response(**v) for k, v in d.get("responses", {}).items()}
        )
