"""
CDN Browser — admin view for managing files on DigitalOcean Spaces.
"""

import mimetypes
from datetime import datetime

import boto3
from botocore.exceptions import ClientError
from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.views.decorators.http import require_http_methods


def _get_s3_client():
    return boto3.client(
        "s3",
        region_name=settings.DO_SPACES_REGION,
        endpoint_url=settings.DO_SPACES_ENDPOINT,
        aws_access_key_id=settings.DO_SPACES_KEY,
        aws_secret_access_key=settings.DO_SPACES_SECRET,
    )


def _human_size(nbytes):
    for unit in ("B", "KB", "MB", "GB"):
        if abs(nbytes) < 1024:
            return f"{nbytes:.1f} {unit}"
        nbytes /= 1024
    return f"{nbytes:.1f} TB"


def _build_breadcrumbs(prefix, base_prefix):
    """Build breadcrumb list from a prefix path."""
    crumbs = [{"name": base_prefix.rstrip("/"), "path": base_prefix}]
    if prefix == base_prefix:
        return crumbs

    relative = prefix[len(base_prefix):]
    parts = [p for p in relative.split("/") if p]
    accumulated = base_prefix
    for part in parts:
        accumulated += part + "/"
        crumbs.append({"name": part, "path": accumulated})
    return crumbs


def _is_image(key):
    mime, _ = mimetypes.guess_type(key)
    return mime and mime.startswith("image/")


@staff_member_required
@require_http_methods(["GET", "POST"])
def cdn_browser(request):
    bucket = settings.DO_SPACES_BUCKET
    base_prefix = settings.DO_SPACES_LOCATION + "/"
    cdn_domain = settings.DO_SPACES_CDN_ENDPOINT

    # Current path from query string
    path = request.GET.get("path", base_prefix)
    if not path.startswith(base_prefix):
        path = base_prefix
    if not path.endswith("/"):
        path += "/"

    s3 = _get_s3_client()

    # Handle POST actions
    if request.method == "POST":
        action = request.POST.get("action")

        if action == "upload":
            uploaded = request.FILES.getlist("files")
            if not uploaded:
                messages.warning(request, "No files selected.")
            else:
                for f in uploaded:
                    key = path + f.name
                    content_type = f.content_type or "application/octet-stream"
                    try:
                        s3.upload_fileobj(
                            f,
                            bucket,
                            key,
                            ExtraArgs={
                                "ACL": "public-read",
                                "ContentType": content_type,
                                "CacheControl": "max-age=86400",
                            },
                        )
                        messages.success(request, f"Uploaded {f.name}")
                    except ClientError as e:
                        messages.error(request, f"Upload failed for {f.name}: {e}")

        elif action == "delete":
            key = request.POST.get("key", "")
            if key and key.startswith(base_prefix):
                try:
                    s3.delete_object(Bucket=bucket, Key=key)
                    messages.success(request, f"Deleted {key.split('/')[-1]}")
                except ClientError as e:
                    messages.error(request, f"Delete failed: {e}")

        elif action == "mkdir":
            folder_name = request.POST.get("folder_name", "").strip()
            folder_name = folder_name.strip("/")
            if folder_name:
                key = path + folder_name + "/"
                try:
                    s3.put_object(
                        Bucket=bucket,
                        Key=key,
                        Body=b"",
                        ACL="public-read",
                    )
                    messages.success(request, f"Created folder {folder_name}/")
                except ClientError as e:
                    messages.error(request, f"Failed to create folder: {e}")
            else:
                messages.warning(request, "Folder name cannot be empty.")

        return redirect(f"{request.path}?path={path}")

    # GET — list objects
    folders = []
    files = []
    try:
        paginator = s3.get_paginator("list_objects_v2")
        pages = paginator.paginate(
            Bucket=bucket,
            Prefix=path,
            Delimiter="/",
        )
        for page in pages:
            for cp in page.get("CommonPrefixes", []):
                prefix_path = cp["Prefix"]
                name = prefix_path[len(path):].rstrip("/")
                if name:
                    folders.append({"name": name, "path": prefix_path})

            for obj in page.get("Contents", []):
                key = obj["Key"]
                name = key[len(path):]
                if not name or name.endswith("/"):
                    continue
                files.append({
                    "name": name,
                    "key": key,
                    "size": _human_size(obj["Size"]),
                    "size_bytes": obj["Size"],
                    "modified": obj["LastModified"],
                    "url": f"{cdn_domain}/{key}",
                    "is_image": _is_image(key),
                })

    except ClientError as e:
        messages.error(request, f"Could not list files: {e}")

    breadcrumbs = _build_breadcrumbs(path, base_prefix)

    # Compute parent path
    parent_path = None
    if path != base_prefix:
        trimmed = path.rstrip("/")
        parent_path = trimmed.rsplit("/", 1)[0] + "/"

    context = {
        **(request.admin_site.each_context(request) if hasattr(request, "admin_site") else {}),
        "title": "CDN Browser",
        "folders": sorted(folders, key=lambda f: f["name"].lower()),
        "files": sorted(files, key=lambda f: f["name"].lower()),
        "current_path": path,
        "base_prefix": base_prefix,
        "breadcrumbs": breadcrumbs,
        "parent_path": parent_path,
        "cdn_domain": cdn_domain,
        "has_permission": True,
    }
    return TemplateResponse(request, "admin/cdn_browser.html", context)
