# Metadata API

A simple API to extract metadata from any website.

Live API:
https://metadata-api-gae5.onrender.com

Docs:
https://metadata-api-gae5.onrender.com/docs

---

## Features

- Extract page title
- Extract description
- Extract preview image
- Extract favicon
- Extract site name
- Extract domain
- Batch metadata extraction

---

## Example Request

GET request:

```
https://metadata-api-gae5.onrender.com/metadata?url=https://github.com
```

---

## Example Response

```json
{
  "status": "success",
  "title": "GitHub · Change is constant. GitHub keeps you ahead.",
  "description": "Join the world's most widely adopted developer platform...",
  "image": "...",
  "favicon": "https://github.com/fluidicon.png",
  "site_name": "GitHub",
  "domain": "github.com",
  "url": "https://github.com"
}
```

---

## Batch Metadata

POST request:

```
/batch-metadata
```

Example body:

```json
{
  "urls": [
    "https://github.com",
    "https://wikipedia.org",
    "https://example.com"
  ]
}
```

---

## Built With

- FastAPI
- BeautifulSoup
- Requests

---

## Deployment

Hosted on Render.