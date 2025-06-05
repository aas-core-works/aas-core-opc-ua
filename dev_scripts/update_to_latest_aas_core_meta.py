"""Fetch the latest models from aas-core-meta repository and re-generate the nodesets."""

import os.path
import pathlib
import shlex
import subprocess
import sys
import xml.etree.ElementTree as ET

import requests


def main() -> int:
    """Execute the main routine."""
    repo = "aas-core-works/aas-core-meta"
    branch = "main"
    rel_paths = [pathlib.Path("aas_core_meta/v3.py")]

    repo_dir = pathlib.Path(os.path.realpath(__file__)).parent.parent
    dev_scripts_dir = repo_dir / "dev_scripts"
    aas_metamodels_dir = repo_dir / "dev_scripts" / "aas_metamodels"

    # Get the Atom feed and extract the latest commit SHA
    feed_url = f"https://github.com/{repo}/commits/{branch}.atom"
    print(f"Fetching Atom feed: {feed_url}")
    try:
        response = requests.get(feed_url, timeout=30)
        response.raise_for_status()
    except Exception as e:
        print(f"Failed to fetch Atom feed: {e}", file=sys.stderr)
        return 1

    try:
        root = ET.fromstring(response.content)
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        first_entry = root.find("atom:entry", ns)
        if first_entry is None:
            print("No entry found in Atom feed", file=sys.stderr)
            return 1

        id_text = first_entry.findtext("atom:id", default="", namespaces=ns)
        prefix = "tag:github.com,2008:Grit::Commit/"
        if not id_text.startswith(prefix):
            print(f"Unexpected ID format: {id_text}", file=sys.stderr)
            return 1

        revision = id_text[len(prefix) :]
        print(f"Latest commit SHA: {revision}")
    except Exception as e:
        print(f"Failed to parse Atom feed: {e}", file=sys.stderr)
        return 1

    # Download each file and prepend comment
    aas_metamodels_dir.mkdir(parents=True, exist_ok=True)

    for rel_path in rel_paths:
        raw_url = (
            f"https://raw.githubusercontent.com/{repo}/{revision}/{rel_path.as_posix()}"
        )
        print(f"Downloading: {raw_url}")
        response = requests.get(raw_url, timeout=30)
        response.raise_for_status()
        content = response.text

        comment = f"# Downloaded from: {raw_url}\n# Revision: {revision[:7]}\n\n"
        full_content = comment + content

        aas_metamodel_file = aas_metamodels_dir / rel_path.name
        aas_metamodel_file.write_text(full_content, encoding="utf-8")

    print("AAS meta-models updated.")

    for rel_path in rel_paths:
        aas_metamodel_file = aas_metamodels_dir / rel_path.name

        snippets_dir = dev_scripts_dir / "snippets" / rel_path.stem

        output_dir = repo_dir / "nodesets" / rel_path.stem

        print(
            f"Generating the OPC UA nodeset for {rel_path} ...\n"
            f"  with snippets: {snippets_dir}\n"
            f"  and model: {aas_metamodel_file}\n"
            f"  to: {output_dir}"
        )

        cmd = [
            sys.executable,
            "-m",
            "aas_core_codegen",
            "--model",
            str(aas_metamodel_file),
            "--snippets",
            str(snippets_dir),
            "--target",
            "opcua",
            "--output_dir",
            str(output_dir),
        ]

        completed_process = subprocess.run(cmd, cwd=str(dev_scripts_dir), check=False)
        if completed_process.returncode != 0:
            cmd_joined = " ".join(shlex.quote(arg) for arg in cmd)
            print(f"Command failed: {cmd_joined}", file=sys.stderr)
            sys.exit(1)

    return 0


if __name__ == "__main__":
    sys.exit(main())
