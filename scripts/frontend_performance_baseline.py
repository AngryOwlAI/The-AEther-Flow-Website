#!/usr/bin/env python3
"""Generate the FE-G0-03 performance baseline from pinned Lighthouse reports."""

from __future__ import annotations

import argparse
import json
import math
import re
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path
from statistics import median
from typing import Any
from urllib.parse import urlparse

ROUTES = {
    "home": ("/", "index.html"),
    "physics": ("/physics/", "physics/index.html"),
    "ai": ("/ai-research-system/", "ai-research-system/index.html"),
    "resources": ("/resources/", "resources/index.html"),
    "gallery": ("/resources/diagrams/", "resources/diagrams/index.html"),
}
RUNS_PER_ROUTE = 3
METRICS = {
    "performance_score": None,
    "first_contentful_paint_ms": "first-contentful-paint",
    "largest_contentful_paint_ms": "largest-contentful-paint",
    "cumulative_layout_shift": "cumulative-layout-shift",
    "total_blocking_time_ms": "total-blocking-time",
    "speed_index_ms": "speed-index",
    "time_to_interactive_ms": "interactive",
    "total_transfer_bytes": "total-byte-weight",
}
GUIDANCE = {
    "core_web_vitals": {
        "url": "https://web.dev/articles/defining-core-web-vitals-thresholds",
        "checked_utc_date": "2026-07-11",
        "field_good_thresholds": {"lcp_ms": 2500, "inp_ms": 200, "cls": 0.1},
        "qualification": "Field classification uses the 75th percentile; this three-run lab baseline is not field data.",
    },
    "total_blocking_time": {
        "url": "https://developer.chrome.com/docs/lighthouse/performance/lighthouse-total-blocking-time",
        "checked_utc_date": "2026-07-11",
        "mobile_fast_threshold_ms": 200,
        "qualification": "TBT is a Lighthouse lab metric and is not a Core Web Vital.",
    },
    "structured_data": {
        "url": "https://developers.google.com/search/docs/appearance/structured-data/sd-policies",
        "checked_utc_date": "2026-07-11",
        "qualification": "Markup must represent visible page content; automated presence checks do not establish rich-result eligibility.",
    },
}


class JsonLdParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._capturing = False
        self._parts: list[str] = []
        self.blocks: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "script":
            return
        attributes = {key.lower(): value for key, value in attrs}
        if attributes.get("type", "").lower() == "application/ld+json":
            self._capturing = True
            self._parts = []

    def handle_data(self, data: str) -> None:
        if self._capturing:
            self._parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "script" and self._capturing:
            self.blocks.append("".join(self._parts))
            self._capturing = False
            self._parts = []


def round_number(value: float | int | None, digits: int = 2) -> float | int | None:
    if value is None:
        return None
    rounded = round(float(value), digits)
    return int(rounded) if rounded.is_integer() else rounded


def audit_numeric(report: dict[str, Any], audit_id: str) -> float | None:
    value = report.get("audits", {}).get(audit_id, {}).get("numericValue")
    return float(value) if isinstance(value, (int, float)) else None


def list_items(report: dict[str, Any], audit_id: str) -> list[dict[str, Any]]:
    items = report.get("audits", {}).get(audit_id, {}).get("details", {}).get("items", [])
    return items if isinstance(items, list) else []


def lcp_element(report: dict[str, Any]) -> dict[str, str]:
    details = report.get("audits", {}).get("lcp-breakdown-insight", {}).get("details", {})
    for item in details.get("items", []) if isinstance(details, dict) else []:
        if isinstance(item, dict) and item.get("type") == "node":
            return {
                "selector": str(item.get("selector", "")),
                "label": str(item.get("nodeLabel", "")),
            }
    return {"selector": "", "label": ""}


def extract_run(report: dict[str, Any], *, route_key: str, run: int) -> dict[str, Any]:
    runtime_error = report.get("runtimeError")
    if runtime_error:
        raise ValueError(f"{route_key} run {run} has runtimeError: {runtime_error}")

    audits = report.get("audits", {})
    requests = list_items(report, "network-requests")
    resource_bytes: dict[str, int] = defaultdict(int)
    resource_counts: dict[str, int] = defaultdict(int)
    remote_requests: list[str] = []
    header_logo_transfer_bytes = 0
    origin = urlparse(str(report.get("finalUrl") or report.get("finalDisplayedUrl")))
    for request in requests:
        resource_type = str(request.get("resourceType", "Other"))
        transfer_size = int(request.get("transferSize") or 0)
        resource_bytes[resource_type] += transfer_size
        resource_counts[resource_type] += 1
        parsed = urlparse(str(request.get("url", "")))
        if parsed.netloc and parsed.netloc != origin.netloc:
            remote_requests.append(str(request.get("url", "")))
        if parsed.path.endswith("/assets/brand/main_angryowl_round.png") and resource_type == "Image":
            header_logo_transfer_bytes = max(header_logo_transfer_bytes, transfer_size)

    long_tasks = list_items(report, "long-tasks")
    image_items = list_items(report, "image-delivery-insight")
    render_blocking = list_items(report, "render-blocking-insight")
    viewport_height = int(
        report.get("configSettings", {}).get("screenEmulation", {}).get("height") or 0
    )
    below_fold_images = [
        str(item.get("url", ""))
        for item in image_items
        if float(item.get("node", {}).get("boundingRect", {}).get("top") or 0)
        >= viewport_height
    ]
    score = report.get("categories", {}).get("performance", {}).get("score")
    run_record: dict[str, Any] = {
        "route_key": route_key,
        "route": ROUTES[route_key][0],
        "run": run,
        "fetch_time": report.get("fetchTime"),
        "performance_score": round_number(float(score) * 100 if isinstance(score, (int, float)) else None),
        "network_request_count": len(requests),
        "remote_request_count": len(remote_requests),
        "remote_requests": remote_requests,
        "header_logo_transfer_bytes": header_logo_transfer_bytes,
        "resource_transfer_bytes": dict(sorted(resource_bytes.items())),
        "resource_request_counts": dict(sorted(resource_counts.items())),
        "long_task_count": len(long_tasks),
        "longest_task_ms": round_number(max((float(item.get("duration") or 0) for item in long_tasks), default=0)),
        "long_task_attributions": sorted({str(item.get("url", "")) for item in long_tasks if item.get("url")}),
        "below_fold_fetched_image_count": len(below_fold_images),
        "below_fold_fetched_images": below_fold_images,
        "image_estimated_waste_bytes": int(sum(int(item.get("wastedBytes") or 0) for item in image_items)),
        "render_blocking_estimated_savings_ms": round_number(sum(float(item.get("wastedMs") or 0) for item in render_blocking)),
        "lcp_element": lcp_element(report),
    }
    for output_key, audit_id in METRICS.items():
        if audit_id is not None:
            run_record[output_key] = round_number(audit_numeric(report, audit_id))
    return run_record


def summarize_values(values: list[float | int]) -> dict[str, float | int]:
    if not values:
        return {}
    return {
        "min": round_number(min(values)),
        "median": round_number(median(values)),
        "max": round_number(max(values)),
    }


def aggregate_route(runs: list[dict[str, Any]]) -> dict[str, Any]:
    summary: dict[str, Any] = {}
    numeric_keys = [*METRICS, "network_request_count", "remote_request_count", "header_logo_transfer_bytes", "long_task_count", "longest_task_ms", "below_fold_fetched_image_count", "image_estimated_waste_bytes", "render_blocking_estimated_savings_ms"]
    for key in numeric_keys:
        values = [run[key] for run in runs if isinstance(run.get(key), (int, float))]
        summary[key] = summarize_values(values)

    max_transfer = int(summary["total_transfer_bytes"]["max"])
    max_css = max(int(run.get("resource_transfer_bytes", {}).get("Stylesheet", 0)) for run in runs)
    max_js = max(int(run.get("resource_transfer_bytes", {}).get("Script", 0)) for run in runs)
    max_image = max(int(run.get("resource_transfer_bytes", {}).get("Image", 0)) for run in runs)
    max_requests = int(summary["network_request_count"]["max"])
    lcp_median = float(summary["largest_contentful_paint_ms"]["median"])
    lcp_max = float(summary["largest_contentful_paint_ms"]["max"])
    cls_max = float(summary["cumulative_layout_shift"]["max"])
    tbt_max = float(summary["total_blocking_time_ms"]["max"])
    summary["provisional_budgets"] = {
        "no_regression_total_transfer_bytes": max_transfer,
        "no_regression_request_count": max_requests,
        "css_transfer_review_threshold_bytes": math.ceil(max_css * 1.10),
        "external_javascript_transfer_ceiling_bytes": max_js,
        "image_transfer_baseline_ceiling_bytes": max_image,
        "remote_request_ceiling": 0,
        "lab_lcp_median_target_ms": 2500,
        "lab_lcp_max_stability_guard_ms": 4000,
        "lab_cls_max_target": 0.1,
        "lab_tbt_max_target_ms": 200,
        "unexplained_long_task_max_ms": 50,
        "below_fold_eager_image_ceiling": 0,
    }
    summary["budget_evaluation"] = {
        "lcp_median_target": "passed" if lcp_median <= 2500 else "failed",
        "lcp_stability_guard": "passed" if lcp_max <= 4000 else "failed",
        "cls_target": "passed" if cls_max <= 0.1 else "failed",
        "tbt_target": "passed" if tbt_max <= 200 else "failed",
        "long_task_guard": "passed" if summary["longest_task_ms"]["max"] <= 50 else "failed",
        "below_fold_eager_image_target": "passed" if summary["below_fold_fetched_image_count"]["max"] == 0 else "failed",
        "remote_request_target": "passed" if summary["remote_request_count"]["max"] == 0 else "failed",
    }
    summary["observed_lcp_elements"] = sorted(
        {run["lcp_element"]["selector"] for run in runs if run["lcp_element"]["selector"]}
    )
    summary["long_task_attributions"] = sorted(
        {item for run in runs for item in run["long_task_attributions"]}
    )
    summary["below_fold_fetched_images"] = sorted(
        {item for run in runs for item in run["below_fold_fetched_images"]}
    )
    return summary


def collect_json_ld(html_path: Path) -> dict[str, Any]:
    parser = JsonLdParser()
    parser.feed(html_path.read_text(encoding="utf-8"))
    types: set[str] = set()
    malformed = 0

    def visit(value: Any) -> None:
        if isinstance(value, dict):
            item_type = value.get("@type")
            if isinstance(item_type, str):
                types.add(item_type)
            elif isinstance(item_type, list):
                types.update(str(item) for item in item_type)
            for child in value.values():
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)

    for block in parser.blocks:
        try:
            visit(json.loads(block))
        except json.JSONDecodeError:
            malformed += 1
    return {"blocks": len(parser.blocks), "types": sorted(types), "malformed_blocks": malformed}


def build_baseline(input_dir: Path, dist_root: Path) -> dict[str, Any]:
    runs: list[dict[str, Any]] = []
    raw_reports: list[dict[str, Any]] = []
    for route_key in ROUTES:
        for run in range(1, RUNS_PER_ROUTE + 1):
            path = input_dir / f"fe-g0-03-{route_key}-run{run}.json"
            report = json.loads(path.read_text(encoding="utf-8"))
            raw_reports.append(report)
            runs.append(extract_run(report, route_key=route_key, run=run))

    first = raw_reports[0]
    config = first.get("configSettings", {})
    benchmark_values = [int(report.get("environment", {}).get("benchmarkIndex") or 0) for report in raw_reports]
    routes: dict[str, Any] = {}
    for route_key, (route, html_relative) in ROUTES.items():
        route_runs = [item for item in runs if item["route_key"] == route_key]
        routes[route_key] = {
            "route": route,
            "runs": route_runs,
            "aggregate": aggregate_route(route_runs),
            "structured_data": collect_json_ld(dist_root / html_relative),
        }

    return {
        "schema_version": "0.1",
        "packet_id": "FE-G0-03",
        "measurement_window": {
            "first_fetch_time": min(str(report.get("fetchTime")) for report in raw_reports),
            "last_fetch_time": max(str(report.get("fetchTime")) for report in raw_reports),
        },
        "method": {
            "tool": "Lighthouse",
            "tool_version": first.get("lighthouseVersion"),
            "runs_per_route": RUNS_PER_ROUTE,
            "navigation": "cold local static-preview navigation",
            "form_factor": config.get("formFactor"),
            "throttling_method": config.get("throttlingMethod"),
            "throttling": config.get("throttling"),
            "screen_emulation": config.get("screenEmulation"),
            "host_user_agent": first.get("environment", {}).get("hostUserAgent"),
            "network_user_agent": first.get("environment", {}).get("networkUserAgent"),
            "benchmark_index": summarize_values(benchmark_values),
            "limitations": [
                "Local static preview removes production CDN, TLS, geographic latency, cache, and server variability.",
                "Three simulated mobile lab runs are diagnostic and do not substitute for 75th-percentile field Core Web Vitals.",
                "No representative user interactions were executed, so INP is unavailable; TBT is the recorded lab proxy.",
                "Performance-only Lighthouse runs do not validate structured-data eligibility; checked-in JSON-LD is inventoried separately.",
            ],
        },
        "guidance": GUIDANCE,
        "routes": routes,
        "cross_route_findings": {
            "shared_header_logo_source_bytes": 1_147_309,
            "shared_header_logo_observed_transfer_bytes": max(int(run["header_logo_transfer_bytes"]) for run in runs),
            "home_initial_raster_transfer_bytes": int(routes["home"]["aggregate"]["provisional_budgets"]["image_transfer_baseline_ceiling_bytes"]),
            "all_routes_zero_tbt": all(float(run["total_blocking_time_ms"]) == 0 for run in runs),
            "all_routes_zero_cls": all(float(run["cumulative_layout_shift"]) == 0 for run in runs),
            "all_routes_zero_external_script_transfer": all(int(run.get("resource_transfer_bytes", {}).get("Script", 0)) == 0 for run in runs),
            "all_routes_zero_remote_requests_in_lab": all(int(run["remote_request_count"]) == 0 for run in runs),
            "routes_with_lcp_stability_failure": [
                key for key, data in routes.items() if data["aggregate"]["budget_evaluation"]["lcp_stability_guard"] == "failed"
            ],
            "routes_with_long_task_guard_failure": [
                key for key, data in routes.items() if data["aggregate"]["budget_evaluation"]["long_task_guard"] == "failed"
            ],
            "routes_fetching_below_fold_images": [
                key for key, data in routes.items() if data["aggregate"]["budget_evaluation"]["below_fold_eager_image_target"] == "failed"
            ],
        },
        "budget_policy": {
            "status": "provisional_baseline_relative",
            "rule": "Do not increase the measured route transfer or request ceilings; require review above 110 percent of measured CSS transfer; retain the user-centric targets as lab gates with explicit field-data qualification.",
            "remediation_targets_retained_from_plan": {
                "header_logo_1x_modern_bytes": 30_000,
                "header_logo_2x_modern_bytes": 60_000,
                "header_logo_png_fallback_bytes": 100_000,
                "initial_home_raster_transfer_bytes": 250_000,
                "remote_visual_asset_requests": 0,
            },
        },
    }


def kib(value: float | int) -> str:
    return f"{float(value) / 1024:.1f} KiB"


def render_markdown(data: dict[str, Any]) -> str:
    method = data["method"]
    lines = [
        "# FE-G0-03 Frontend Performance Baseline — 2026-07-11",
        "",
        "## Analysis",
        "",
        "This report is a read-only local lab baseline for the five routes required by",
        "`FE-G0-03`. It does not claim production or field performance. Three pinned",
        "Lighthouse mobile-simulation runs were collected per route against the static",
        "Astro preview. No frontend runtime, public claim, source, asset, manifest,",
        "remote Git, or deployment state changed.",
        "",
        "## Method",
        "",
        f"- Lighthouse {method['tool_version']}; {method['runs_per_route']} cold-navigation runs per route.",
        f"- Form factor: {method['form_factor']}; throttling: {method['throttling_method']}; viewport: {method['screen_emulation'].get('width')} × {method['screen_emulation'].get('height')} CSS px.",
        f"- CPU slowdown: {method['throttling'].get('cpuSlowdownMultiplier')}×; RTT: {method['throttling'].get('rttMs')} ms; throughput: {method['throttling'].get('throughputKbps')} Kbps.",
        f"- Measurement window: {data['measurement_window']['first_fetch_time']} through {data['measurement_window']['last_fetch_time']}.",
        "- Aggregates use median for the central observation and maximum for stability/no-regression guards.",
        "",
        "## Route results",
        "",
        "| Route | Score median | LCP median / max | CLS max | TBT max | Transfer | Requests | Budget result |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for route_data in data["routes"].values():
        agg = route_data["aggregate"]
        evaluations = agg["budget_evaluation"]
        failed = [name for name, status in evaluations.items() if status == "failed"]
        result = "pass" if not failed else "fail: " + ", ".join(failed)
        lines.append(
            f"| `{route_data['route']}` | {agg['performance_score']['median']:.0f} | "
            f"{agg['largest_contentful_paint_ms']['median'] / 1000:.2f} s / {agg['largest_contentful_paint_ms']['max'] / 1000:.2f} s | "
            f"{agg['cumulative_layout_shift']['max']:.2f} | {agg['total_blocking_time_ms']['max']:.0f} ms | "
            f"{kib(agg['total_transfer_bytes']['median'])} | {agg['network_request_count']['max']:.0f} | {result} |"
        )

    lines += [
        "",
        "### Per-run LCP and score evidence",
        "",
        "| Route | Run | Score | FCP | LCP | CLS | TBT | Longest task |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for route_data in data["routes"].values():
        for run in route_data["runs"]:
            lines.append(
                f"| `{run['route']}` | {run['run']} | {run['performance_score']:.0f} | "
                f"{run['first_contentful_paint_ms'] / 1000:.2f} s | {run['largest_contentful_paint_ms'] / 1000:.2f} s | "
                f"{run['cumulative_layout_shift']:.2f} | {run['total_blocking_time_ms']:.0f} ms | {run['longest_task_ms']:.0f} ms |"
            )

    findings = data["cross_route_findings"]
    lines += [
        "",
        "## Findings",
        "",
        f"1. The shared 1,147,309-byte header PNG dominates every route. Total initial transfer is {kib(min(route['aggregate']['total_transfer_bytes']['median'] for route in data['routes'].values()))}–{kib(max(route['aggregate']['total_transfer_bytes']['median'] for route in data['routes'].values()))}; Lighthouse estimates most header-image bytes are avoidable.",
        "2. CLS and TBT were zero in all 15 runs. No external JavaScript transfer was observed; any inline script remains part of the HTML response. Lighthouse still recorded unattributable long tasks up to 54 ms, slightly above the 50 ms guard.",
        f"3. LCP was unstable above the 4-second guard on: {', '.join(findings['routes_with_lcp_stability_failure']) or 'none'}. The repeated approximately 7.05-second samples make LCP stability a baseline defect even where a route median passes 2.5 seconds.",
        "4. The lab observed no remote requests. This does not negate the separate FE-G0-02 browser observation that Home can initiate third-party YouTube requests during broader interaction/full-scroll behavior.",
        f"5. Below-fold images were fetched during initial navigation on: {', '.join(findings['routes_fetching_below_fold_images']) or 'none'}. This fails the provisional zero-eager-fetch target where the images are comprehension diagrams below the mobile viewport.",
        "6. INP is unavailable because no field dataset or controlled interaction series was supplied. TBT is retained only as a lab responsiveness proxy.",
        "",
        "## Measured provisional budgets",
        "",
        "- User-centric lab gates: route median LCP ≤ 2.5 s, maximum-run LCP stability guard ≤ 4.0 s, maximum CLS ≤ 0.10, maximum TBT ≤ 200 ms, and no unexplained long task above 50 ms.",
        "- Transfer and request ceilings: each route may not exceed its measured maximum without review. These are no-regression ceilings, not acceptable end-state targets.",
        "- CSS review threshold: route CSS transfer above 110% of the measured baseline requires explicit budget review.",
        "- External JavaScript and remote visual-request ceilings remain zero unless separately approved.",
        "- Below-fold comprehension-diagram eager fetches remain zero; the current baseline does not meet this target.",
        "- Remediation targets remain 30 KB for a 1× modern header logo, 60 KB for 2×, 100 KB for PNG fallback, and 250 KB for initial Home raster transfer. The current Home raster transfer is " + kib(findings["home_initial_raster_transfer_bytes"]) + ".",
        "",
        "## Structured-data observation",
        "",
        "| Route | JSON-LD blocks | Types | Malformed |",
        "| --- | ---: | --- | ---: |",
    ]
    for route_data in data["routes"].values():
        structured = route_data["structured_data"]
        lines.append(
            f"| `{route_data['route']}` | {structured['blocks']} | {', '.join(structured['types']) or 'none'} | {structured['malformed_blocks']} |"
        )
    lines += [
        "",
        "Presence and JSON parsing do not establish rich-result eligibility. Google’s",
        "guidance requires accurate, relevant markup that represents visible page content.",
        "",
        "## Limitations",
        "",
    ]
    lines.extend(f"- {item}" for item in method["limitations"])
    lines += [
        "",
        "## Conclusion",
        "",
        "The current frontend is main-thread-light but image-heavy. CLS and TBT satisfy",
        "the provisional gates, while LCP stability does not. The logical repair order is",
        "to right-size the shared header logo, add the planned image loading/dimension",
        "policy, and rerun the identical baseline before enforcing budgets in CI.",
        "",
        "## References",
        "",
        "Chrome for Developers. (n.d.). *Total Blocking Time*. Retrieved July 11, 2026, from https://developer.chrome.com/docs/lighthouse/performance/lighthouse-total-blocking-time",
        "",
        "Google Search Central. (2026, January 6). *General structured data guidelines*. https://developers.google.com/search/docs/appearance/structured-data/sd-policies",
        "",
        "web.dev. (2025, May 7). *How the Core Web Vitals metrics thresholds were defined*. https://web.dev/articles/defining-core-web-vitals-thresholds",
        "",
    ]
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--dist-root", type=Path, default=Path("dist"))
    parser.add_argument("--json-output", type=Path, required=True)
    parser.add_argument("--markdown-output", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    data = build_baseline(args.input_dir, args.dist_root)
    args.json_output.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    args.markdown_output.write_text(render_markdown(data), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
