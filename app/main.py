from urllib.parse import urlparse

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse

from .models import (
    BatchMetadataRequest,
    BatchMetadataResponse,
    MetadataResponse,
)
from .services import extract_metadata

app = FastAPI(title="Metadata API")


@app.get("/", response_class=HTMLResponse)
def homepage():
    return """
    <html>
        <head>
            <title>Website Metadata API</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    max-width: 760px;
                    margin: 60px auto;
                    line-height: 1.6;
                    color: #333;
                    padding: 0 20px;
                }
                h1 {
                    font-size: 36px;
                    margin-bottom: 10px;
                }
                code, pre {
                    background: #f4f4f4;
                    border-radius: 6px;
                }
                code {
                    padding: 4px 6px;
                }
                pre {
                    padding: 14px;
                    overflow-x: auto;
                }
                .box {
                    background: #f9f9f9;
                    padding: 18px;
                    border-radius: 8px;
                    margin-top: 20px;
                    border: 1px solid #eee;
                }
                a {
                    color: #2563eb;
                    text-decoration: none;
                }
                a:hover {
                    text-decoration: underline;
                }
            </style>
        </head>
        <body>

            <h1>Website Metadata API</h1>

            <p>
                Extract titles, descriptions, preview images, favicons, and social metadata from any website.
            </p>

            <div class="box">
                <strong>Single URL request</strong>
                <pre>GET /metadata?url=https://example.com</pre>
            </div>

            <div class="box">
                <strong>Preview request</strong>
                <pre>GET /preview?url=https://example.com</pre>
            </div>

            <div class="box">
                <strong>Batch request</strong>
                <pre>
POST /batch-metadata

{
  "urls": [
    "https://github.com",
    "https://wikipedia.org",
    "https://example.com"
  ]
}
                </pre>
            </div>

            <div class="box">
                <strong>Example response</strong>
                <pre>{
  "status": "success",
  "title": "Example Domain",
  "description": null,
  "image": null,
  "favicon": "https://example.com/favicon.ico",
  "site_name": null,
  "domain": "example.com",
  "url": "https://example.com",
  "error": null,
  "og_title": null,
  "twitter_title": null,
  "og_type": null
}</pre>
            </div>

            <div class="box">
                <strong>Project Links</strong>
                <pre>
API:
https://metadata-api-gae5.onrender.com

Docs:
https://metadata-api-gae5.onrender.com/docs

GitHub:
https://github.com/riyashah0913-prog/metadata-api
                </pre>
            </div>

            <p>
                Test the API here:
                <a href="/docs">API Documentation</a>
            </p>

        </body>
    </html>
    """


def validate_url(url: str):
    if not url.startswith("http"):
        raise HTTPException(status_code=400, detail="URL must start with http or https")


def add_domain_field(metadata: dict) -> dict:
    parsed = urlparse(metadata["url"])
    metadata["domain"] = parsed.netloc
    return metadata


@app.get("/metadata", response_model=MetadataResponse)
def get_metadata(url: str = Query(..., description="The URL to extract metadata from")):
    validate_url(url)

    try:
        metadata = extract_metadata(url)
        metadata = add_domain_field(metadata)
        metadata["status"] = "success"
        metadata["error"] = None
        return metadata
    except Exception:
        raise HTTPException(status_code=400, detail="Could not fetch metadata")


@app.get("/preview")
def preview(url: str = Query(..., description="The URL to generate a clean preview from")):
    validate_url(url)

    try:
        data = extract_metadata(url)
        data = add_domain_field(data)

        return {
            "title": data.get("og_title") or data.get("twitter_title") or data.get("title"),
            "description": data.get("description"),
            "image": data.get("image"),
            "url": data.get("url"),
            "site": data.get("site_name"),
            "domain": data.get("domain"),
        }
    except Exception:
        raise HTTPException(status_code=400, detail="Could not generate preview")


@app.post("/batch-metadata", response_model=BatchMetadataResponse)
def get_batch_metadata(request: BatchMetadataRequest):
    if not request.urls:
        raise HTTPException(status_code=400, detail="Please provide at least one URL")

    if len(request.urls) > 10:
        raise HTTPException(status_code=400, detail="Maximum of 10 URLs per request")

    results = []

    for url in request.urls:
        if not url.startswith("http"):
            results.append({
                "status": "error",
                "title": None,
                "description": None,
                "image": None,
                "favicon": None,
                "site_name": None,
                "domain": None,
                "url": url,
                "error": "URL must start with http or https",
                "og_title": None,
                "twitter_title": None,
                "og_type": None
            })
            continue

        try:
            metadata = extract_metadata(url)
            metadata = add_domain_field(metadata)
            metadata["status"] = "success"
            metadata["error"] = None
            results.append(metadata)
        except Exception:
            results.append({
                "status": "error",
                "title": None,
                "description": None,
                "image": None,
                "favicon": None,
                "site_name": None,
                "domain": None,
                "url": url,
                "error": "Could not fetch metadata",
                "og_title": None,
                "twitter_title": None,
                "og_type": None
            })

    return {"results": results}