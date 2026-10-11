#!/usr/bin/env python3
"""Build repeatable audio-encoding and gzip comparisons for 02-beach-waves.html."""
from __future__ import annotations

import base64
import csv
import gzip
import json
import re
import shutil
import subprocess
import zipfile
from pathlib import Path

ROOT = Path.cwd()
SOURCE = ROOT / "Bucket/Html-files/app/calm/journey/02-beach-waves.html"
OUT = ROOT / "output"
TMP = OUT / "_work"
HTML = SOURCE.read_text(encoding="utf-8")
HTML_BYTES = HTML.encode("utf-8")
AUDIO_URI_RE = re.compile(r'data:audio/mpeg;base64,([A-Za-z0-9+/=]+)')
WAV_URI_RE = re.compile(r'data:audio/wav;base64,([A-Za-z0-9+/=]+)')
JPEG_URI_RE = re.compile(r'data:image/jpeg;base64,([A-Za-z0-9+/=]+)')


def run_ffmpeg(src: Path, dst: Path, args: list[str]) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(src), *args, str(dst)],
        check=True,
    )


def ffprobe(path: Path) -> dict:
    raw = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration,size,bit_rate:stream=codec_name,sample_rate,channels,bit_rate",
        "-of", "json", str(path),
    ], text=True)
    obj = json.loads(raw)
    fmt = obj.get("format", {})
    streams = obj.get("streams", [])
    return {
        "duration_seconds": round(float(fmt["duration"]), 3) if fmt.get("duration") else None,
        "container_bytes": int(fmt["size"]) if fmt.get("size") else path.stat().st_size,
        "container_bitrate": int(fmt["bit_rate"]) if fmt.get("bit_rate") else None,
        "streams": [
            {
                "codec": st.get("codec_name"),
                "sample_rate": int(st["sample_rate"]) if st.get("sample_rate") else None,
                "channels": st.get("channels"),
                "bitrate": int(st["bit_rate"]) if st.get("bit_rate") else None,
            } for st in streams
        ],
    }


def b64_uri(mime: str, raw: bytes) -> str:
    return f"data:{mime};base64," + base64.b64encode(raw).decode("ascii")


def replace_narration(html: str, parts: list[bytes], mime: str) -> str:
    matches = list(AUDIO_URI_RE.finditer(html))
    if len(matches) != len(parts):
        raise RuntimeError(f"Expected {len(parts)} narration segments; found {len(matches)}")
    i = 0
    def repl(_m):
        nonlocal i
        value = b64_uri(mime, parts[i])
        i += 1
        return value
    return AUDIO_URI_RE.sub(repl, html)


def replace_ambience(html: str, raw: bytes, mime: str) -> str:
    updated, n = WAV_URI_RE.subn(lambda _m: b64_uri(mime, raw), html, count=1)
    if n != 1:
        raise RuntimeError(f"Expected one embedded WAV ambience; replaced {n}")
    return updated


def replace_ambience_with_external(html: str, uri: str) -> str:
    updated, n = WAV_URI_RE.subn(lambda _m: uri, html, count=1)
    if n != 1:
        raise RuntimeError(f"Expected one embedded WAV ambience; replaced {n}")
    start = updated.find("const b64=AMB.slice(")
    end_marker = "ambCtx.decodeAudioData(bytes.buffer).then(buffer=>{"
    end = updated.find(end_marker, start)
    if start < 0 or end < 0:
        raise RuntimeError("Could not find ambience decoder block in the source HTML")
    end += len(end_marker)
    new = (
        "const ambBytes=AMB.startsWith('data:')?"
        "Promise.resolve((()=>{const b64=AMB.slice(AMB.indexOf(',')+1),binary=atob(b64),"
        "bytes=new Uint8Array(binary.length);for(let i=0;i<binary.length;i++)"
        "bytes[i]=binary.charCodeAt(i);return bytes.buffer;})()):"
        "fetch(AMB).then(r=>{if(!r.ok)throw new Error('ambience fetch failed');return r.arrayBuffer()}); "
        "ambBytes.then(audioBytes=>ambCtx.decodeAudioData(audioBytes)).then(buffer=>{"
    )
    updated = updated[:start] + new + updated[end:]
    return updated


def write_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def percent_saved(source: int, dest: int) -> float:
    return round((source - dest) * 100.0 / source, 2) if source else 0.0


def main() -> None:
    if not SOURCE.exists():
        raise FileNotFoundError(f"Expected source HTML at {SOURCE}")
    if shutil.which("ffmpeg") is None or shutil.which("ffprobe") is None:
        raise RuntimeError("ffmpeg and ffprobe must be installed before building variants")

    narration_matches = list(AUDIO_URI_RE.finditer(HTML))
    wav_matches = list(WAV_URI_RE.finditer(HTML))
    jpeg_matches = list(JPEG_URI_RE.finditer(HTML))
    if len(narration_matches) != 6:
        raise RuntimeError(f"Expected 6 embedded MP3 narration parts; found {len(narration_matches)}")
    if len(wav_matches) != 1:
        raise RuntimeError(f"Expected 1 embedded WAV ambience; found {len(wav_matches)}")
    if len(jpeg_matches) != 1:
        raise RuntimeError(f"Expected 1 embedded JPEG background; found {len(jpeg_matches)}")

    original_parts = [base64.b64decode(m.group(1)) for m in narration_matches]
    original_amb = base64.b64decode(wav_matches[0].group(1))
    original_jpeg = base64.b64decode(jpeg_matches[0].group(1))

    if OUT.exists():
        shutil.rmtree(OUT)
    TMP.mkdir(parents=True, exist_ok=True)

    original_gz = gzip.compress(HTML_BYTES, compresslevel=9, mtime=0)
    write_bytes(OUT / "02-beach-waves-original.html.gz", original_gz)

    source_dir = TMP / "source"
    source_dir.mkdir(parents=True, exist_ok=True)
    source_audio_paths = []
    for idx, raw in enumerate(original_parts, start=1):
        p = source_dir / f"part-{idx:02d}.mp3"
        write_bytes(p, raw)
        source_audio_paths.append(p)
    source_amb_path = source_dir / "ambience.wav"
    write_bytes(source_amb_path, original_amb)

    source_audio_info = [ffprobe(p) for p in source_audio_paths]
    source_amb_info = ffprobe(source_amb_path)

    profiles = [
        {
            "id": "embedded-mp3-128k",
            "label": "Embedded MP3 128 kb/s",
            "ext": "mp3", "mime": "audio/mpeg", "amb_ext": "mp3", "amb_mime": "audio/mpeg",
            "narration_args": ["-c:a", "libmp3lame", "-b:a", "128k"],
            "ambience_args": ["-c:a", "libmp3lame", "-b:a", "64k"],
        },
        {
            "id": "embedded-aac-96k",
            "label": "Embedded AAC-LC 96 kb/s (M4A/MP4 container)",
            "ext": "m4a", "mime": "audio/mp4", "amb_ext": "m4a", "amb_mime": "audio/mp4",
            "narration_args": ["-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart"],
            "ambience_args": ["-c:a", "aac", "-b:a", "48k", "-movflags", "+faststart"],
        },
        {
            "id": "embedded-opus-64k",
            "label": "Embedded Opus 64 kb/s (Ogg)",
            "ext": "ogg", "mime": "audio/ogg", "amb_ext": "ogg", "amb_mime": "audio/ogg",
            "narration_args": ["-c:a", "libopus", "-b:a", "64k", "-vbr", "on", "-application", "audio"],
            "ambience_args": ["-c:a", "libopus", "-b:a", "32k", "-vbr", "on", "-application", "audio"],
        },
        {
            "id": "embedded-opus-96k",
            "label": "Embedded Opus 96 kb/s (Ogg)",
            "ext": "ogg", "mime": "audio/ogg", "amb_ext": "ogg", "amb_mime": "audio/ogg",
            "narration_args": ["-c:a", "libopus", "-b:a", "96k", "-vbr", "on", "-application", "audio"],
            "ambience_args": ["-c:a", "libopus", "-b:a", "48k", "-vbr", "on", "-application", "audio"],
        },
    ]

    rows = [{
        "variant": "original-html",
        "description": "Original self-contained HTML",
        "html_bytes": len(HTML_BYTES),
        "html_gzip_bytes": len(original_gz),
        "package_bytes": len(HTML_BYTES),
        "savings_vs_original_html_pct": 0.0,
    }, {
        "variant": "original-html-gzip",
        "description": "Original HTML compressed as .gz",
        "html_bytes": len(original_gz),
        "html_gzip_bytes": len(original_gz),
        "package_bytes": len(original_gz),
        "savings_vs_original_html_pct": percent_saved(len(HTML_BYTES), len(original_gz)),
    }]

    for profile in profiles:
        encoded_parts = []
        for idx, source_path in enumerate(source_audio_paths, start=1):
            dst = TMP / profile["id"] / f"part-{idx:02d}.{profile['ext']}"
            run_ffmpeg(source_path, dst, profile["narration_args"])
            encoded_parts.append(dst.read_bytes())
        encoded_amb_path = TMP / profile["id"] / f"ambience.{profile['amb_ext']}"
        run_ffmpeg(source_amb_path, encoded_amb_path, profile["ambience_args"])
        encoded_amb = encoded_amb_path.read_bytes()

        variant_html = replace_narration(HTML, encoded_parts, profile["mime"])
        variant_html = replace_ambience(variant_html, encoded_amb, profile["amb_mime"])
        out_html = OUT / f"02-beach-waves-{profile['id']}.html"
        write_bytes(out_html, variant_html.encode("utf-8"))

        rows.append({
            "variant": profile["id"],
            "description": profile["label"],
            "html_bytes": out_html.stat().st_size,
            "html_gzip_bytes": len(gzip.compress(out_html.read_bytes(), compresslevel=9, mtime=0)),
            "package_bytes": out_html.stat().st_size,
            "narration_audio_bytes": sum(len(x) for x in encoded_parts),
            "ambience_audio_bytes": len(encoded_amb),
            "savings_vs_original_html_pct": percent_saved(len(HTML_BYTES), out_html.stat().st_size),
        })

    # This variant moves the original media into sidecars, preserving their bytes.
    ext_dir = OUT / "external-assets-original-audio"
    media_dir = ext_dir / "media"
    media_dir.mkdir(parents=True, exist_ok=True)
    for idx, raw in enumerate(original_parts, start=1):
        write_bytes(media_dir / f"part-{idx:02d}.mp3", raw)
    write_bytes(media_dir / "ambience.wav", original_amb)

    ext_counter = 0
    def ext_repl(_m):
        nonlocal ext_counter
        ext_counter += 1
        return f"media/part-{ext_counter:02d}.mp3"
    ext_html = AUDIO_URI_RE.sub(ext_repl, HTML)
    if ext_counter != 6:
        raise RuntimeError(f"External audio replacement count was {ext_counter}, not 6")
    ext_html = replace_ambience_with_external(ext_html, "media/ambience.wav")
    ext_html_path = ext_dir / "02-beach-waves.html"
    write_bytes(ext_html_path, ext_html.encode("utf-8"))
    external_total = ext_html_path.stat().st_size + sum(p.stat().st_size for p in media_dir.iterdir())
    external_media_total = sum(p.stat().st_size for p in media_dir.iterdir())
    rows.append({
        "variant": "external-assets-original-audio",
        "description": "External MP3/WAV sidecars; source audio bytes unchanged",
        "html_bytes": ext_html_path.stat().st_size,
        "html_gzip_bytes": len(gzip.compress(ext_html_path.read_bytes(), compresslevel=9, mtime=0)),
        "package_bytes": external_total,
        "external_media_bytes": external_media_total,
        "savings_vs_original_html_pct": percent_saved(len(HTML_BYTES), ext_html_path.stat().st_size),
    })

    report = {
        "source": str(SOURCE.relative_to(ROOT)),
        "source_sha": "ac8ee77ab7f1d39116385fdce64143cbc25d2b08",
        "original_html_bytes": len(HTML_BYTES),
        "original_html_gzip_bytes": len(original_gz),
        "original_html_gzip_saved_pct": percent_saved(len(HTML_BYTES), len(original_gz)),
        "embedded_assets": {
            "background_jpeg": {"base64_characters": len(jpeg_matches[0].group(1)), "decoded_bytes": len(original_jpeg)},
            "narration_mp3_parts": {
                "count": len(original_parts),
                "base64_characters": sum(len(m.group(1)) for m in narration_matches),
                "decoded_bytes": sum(map(len, original_parts)),
                "parts": [
                    {"part": i, "bytes": len(raw), **info}
                    for i, (raw, info) in enumerate(zip(original_parts, source_audio_info), start=1)
                ],
            },
            "ambience_wav": {
                "base64_characters": len(wav_matches[0].group(1)),
                "decoded_bytes": len(original_amb),
                **source_amb_info,
            },
        },
        "variants": rows,
        "quality_notes": [
            "The embedded MP3/AAC/Opus samples are lossy re-encodes, not bit-identical to the original MP3.",
            "The external-assets example preserves all narration MP3s and the ambience WAV byte-for-byte, but requires HTML and media to be hosted together over HTTP(S) or loaded by the app WebView.",
            "The .gz file is a transport artifact. A web server should serve it with Content-Encoding: gzip and Content-Type: text/html; opening a .html.gz URL directly may download it rather than render it.",
            "Test audio codec support in the exact Android System WebView build used by the app; older WebView versions may not support every container/codec combination."
        ],
    }
    write_bytes(OUT / "comparison-report.json", json.dumps(report, ensure_ascii=False, indent=2).encode("utf-8"))

    md = [
        "# Beach Waves HTML/audio size comparison",
        "",
        f"Source: {report['source']}",
        f"Original HTML: **{len(HTML_BYTES):,} bytes ({len(HTML_BYTES)/1024/1024:.2f} MiB)**",
        f"GZIP of original HTML: **{len(original_gz):,} bytes ({len(original_gz)/1024/1024:.2f} MiB)**",
        f"Reduction from GZIP: **{percent_saved(len(HTML_BYTES), len(original_gz)):.2f}%**",
        "",
        "## Embedded assets",
        "",
        f"Background JPEG: {len(original_jpeg):,} decoded bytes",
        f"Six original MP3 parts: {sum(map(len, original_parts)):,} decoded bytes; {sum(len(m.group(1)) for m in narration_matches):,} Base64 characters",
        f"Original ambience WAV: {len(original_amb):,} decoded bytes; {len(wav_matches[0].group(1)):,} Base64 characters",
        "",
        "## Results",
        "",
        "| Variant | HTML bytes | GZIP bytes | Full package bytes | HTML saving vs original |",
        "|---|---:|---:|---:|---:|",
    ]
    for row in rows:
        md.append(
            f"| {row['variant']} | {row['html_bytes']:,} | {row['html_gzip_bytes']:,} | "
            f"{row['package_bytes']:,} | {row['savings_vs_original_html_pct']:.2f}% |"
        )
    md += ["", "## Audio source inspection", ""]
    for idx, info in enumerate(source_audio_info, start=1):
        st = info["streams"][0] if info["streams"] else {}
        md.append(
            f"Part {idx}: {st.get('codec')} / {st.get('sample_rate')} Hz / "
            f"{st.get('channels')} channel(s) / {info.get('duration_seconds')} s / "
            f"{info.get('container_bytes'):,} bytes"
        )
    md += [
        "",
        "## Interpretation",
        "",
        "GZIP reduces the HTML text/Base64 representation, but the file remains one large monolithic document and must be decompressed before parsing.",
        "MP3 128 kb/s is a conservative podcast-oriented comparison; AAC 96 kb/s and Opus 64/96 kb/s test more efficient lossy encodings. Listen for artifacts before choosing.",
        "The external-assets example avoids re-encoding narration: it cuts HTML size dramatically while preserving original audio payloads byte-for-byte. The full package still includes the media files.",
        "Do not treat .html.gz as a normal page unless the server sets the correct gzip Content-Encoding header.",
        "",
        "## Compatibility notes",
        "",
        "Test Ogg/Opus in the exact Android System WebView used by the app. If compatibility is uncertain, external MP3 assets are the conservative quality-preserving baseline.",
        "",
    ]
    write_bytes(OUT / "comparison-report.md", "\n".join(md).encode("utf-8"))

    with (OUT / "comparison-report.csv").open("w", newline="", encoding="utf-8-sig") as f:
        cols = sorted({key for row in rows for key in row.keys()})
        writer = csv.DictWriter(f, fieldnames=cols)
        writer.writeheader()
        writer.writerows(rows)

    zip_path = OUT / "beach-waves-audio-comparison.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for path in sorted(OUT.rglob("*")):
            if not path.is_file() or path == zip_path or TMP in path.parents:
                continue
            z.write(path, path.relative_to(OUT).as_posix())

    print(json.dumps({
        "source_bytes": len(HTML_BYTES),
        "gzip_bytes": len(original_gz),
        "gzip_saved_pct": percent_saved(len(HTML_BYTES), len(original_gz)),
        "narration_payload_bytes": sum(map(len, original_parts)),
        "ambience_payload_bytes": len(original_amb),
        "external_html_bytes": ext_html_path.stat().st_size,
        "external_total_bytes": external_total,
        "zip_bytes": zip_path.stat().st_size,
        "rows": rows,
        "report": str((OUT / "comparison-report.md").relative_to(ROOT)),
        "zip": str(zip_path.relative_to(ROOT)),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
