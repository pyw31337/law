#!/usr/bin/env python3
"""Collect the UK legislation public feed and publish run-level evidence."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
now = datetime.now(timezone.utc)
source_url = "https://www.legislation.gov.uk/ukpga/data.feed"
request = Request(source_url, headers={"Accept": "application/atom+xml", "User-Agent": "LetsLaw observability"})
with urlopen(request, timeout=30) as response:
    xml_bytes = response.read()
root = ElementTree.fromstring(xml_bytes)
ns = {"atom": "http://www.w3.org/2005/Atom"}
records = [{"id": entry.findtext("atom:id", default="", namespaces=ns), "title": entry.findtext("atom:title", default="", namespaces=ns), "updated": entry.findtext("atom:updated", default="", namespaces=ns)} for entry in root.findall("atom:entry", ns)]
records = [record for record in records if record["id"] and record["title"]]
if not records:
    raise RuntimeError("Legislation feed has no valid entries")
raw = {"source": "legislation.gov.uk", "source_url": source_url, "observed_at": now.isoformat(), "records": records}
raw_bytes = json.dumps(raw, ensure_ascii=False, sort_keys=True).encode("utf-8")
raw_path = ROOT / "data" / "raw" / "uk_legislation_feed.json"
raw_path.parent.mkdir(parents=True, exist_ok=True)
raw_path.write_bytes(raw_bytes + b"\n")
out = ROOT / "data" / "observability" / "latest.json"
prev_records = None
if out.exists():
    try:
        prev_records = (json.loads(out.read_text(encoding="utf-8")).get("counts") or {}).get("records")
    except (OSError, json.JSONDecodeError):
        pass
increment = max(0, len(records) - int(prev_records)) if isinstance(prev_records, (int, float)) else 0
payload = {
    "schema": "lets_observability_v1",
    "run_id": f"law-{now.strftime('%Y%m%dT%H%M%SZ')}",
    "observed_at": now.isoformat(),
    "service_id": "law",
    "source": "uk_legislation_feed",
    "stages": {
        "collect": {"status": "success", "ok": len(records), "artifact": True},
        "analyze": {"status": "not_started", "ok": None},
        "quality": {"status": "success", "quality_issue_count": 0, "detail": "Atom entry identifiers"},
        "publish": {"status": "success", "artifact": True},
    },
    "counts": {"records": len(records), "increment": increment},
    "artifacts": {"raw": hashlib.sha256(raw_bytes).hexdigest()},
    "note": "UK legislation public Atom feed snapshot.",
}
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Legislation entries observed: {len(records)}")
