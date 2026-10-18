from pydantic import BaseModel, Field


class PaginationMeta(BaseModel):
    limit: int = Field(
        ...,
        ge=1,
        description="Number of items returned",
        examples=[10],
    )
    offset: int = Field(
        ...,
        ge=0,
        description="Number of items skipped",
        examples=[0],
    )
    total: int = Field(
        ...,
        ge=0,
        description="Total number of matching items",
        examples=[25],
    )


def make_pagination_links(
    base_path: str,
    limit: int,
    offset: int,
    total: int,
    extra_params: dict[str, str | None] | None = None,
) -> dict[str, str]:
    query_parts = []
    if extra_params:
        for k, v in extra_params.items():
            if v is not None:
                query_parts.append(f"{k}={v}")

    extra_str = ("&" + "&".join(query_parts)) if query_parts else ""
    self_url = f"{base_path}?limit={limit}&offset={offset}{extra_str}"
    links: dict[str, str] = {"self": self_url}

    if offset + limit < total:
        links["next"] = f"{base_path}?limit={limit}&offset={offset + limit}{extra_str}"

    if offset > 0:
        prev_offset = max(0, offset - limit)
        links["prev"] = f"{base_path}?limit={limit}&offset={prev_offset}{extra_str}"

    return links
