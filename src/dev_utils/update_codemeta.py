"""Shallow wrapper around codemetapy to use it with pre-commit."""
import importlib.resources
import json
from pathlib import Path
from typing import List

import rdflib
import rdflib.compare
import typer
from codemeta.codemeta import build
from codemeta.serializers.jsonld import serialize_to_jsonld

# ----
# Replicate basic codemetapy behavior (based on codemeta.codemeta.main module)


def _gen_codemeta(sources, *, with_entrypoints: bool = False):
    """Run codemeta file generation using Python API.

    Returns JSON-LD dict.
    """
    supp_inputs = set(["codemeta.json", "pyproject.toml"])
    req_inputs = supp_inputs.intersection(set(sources))
    eff_inputs = [p for p in req_inputs if Path(p).is_file()]
    print(Path(".").absolute())
    print(Path("pyproject.toml").absolute())
    print(Path("pyproject.toml").absolute().is_file())
    print("req", req_inputs)
    print("eff", eff_inputs)

    g, res, args, _ = build(
        inputsources=eff_inputs,
        output="json",
        with_entrypoints=with_entrypoints,
    )
    return serialize_to_jsonld(g, res, args)


def _serialize_codemeta(cm) -> str:
    """Convert JSON Dict to str (using settings like codemetapy)."""
    # using settings like in codemetapy
    return json.dumps(cm, indent=4, ensure_ascii=False, sort_keys=True)


# ----
# Helpers to work around issue with non-deterministic serialization

# expected URLs
_codemeta_context = set(
    [
        "https://doi.org/10.5063/schema/codemeta-2.0",
        "https://w3id.org/software-iodata",
        "https://raw.githubusercontent.com/jantman/repostatus.org/"
        "master/badges/latest/ontology.jsonld",
        "https://schema.org",
        "https://w3id.org/software-types",
    ]
)

# assembled context (manually downloaded and combined in a JSON array)
_context_file = "codemeta_context_2023-04-19.json"

with importlib.resources.open_text(__package__, _context_file) as c:
    cached_context = json.load(c)


def _localize_codemeta_context(json):
    """Prevent rdflib external context resolution by adding it from a file."""
    ctx = set(json.get("@context") or [])
    if not ctx:
        return json  # probably empty or not codemeta, nothing to do
    if ctx != _codemeta_context:
        raise RuntimeError(f"Unexpected codemeta context: {json['@context']}")
    ret = dict(json)
    ret.update({"@context": cached_context})
    return ret


# ----
# Wrapper CLI app

app = typer.Typer()

trg_arg = typer.Argument(
    ...,
    file_okay=True,
    dir_okay=False,
)

src_arg = typer.Argument(
    ..., exists=True, file_okay=True, dir_okay=False, readable=True
)


@app.command(
    help="""
Create or update the target codemeta file (first argument)
by running codemetapy with all the other passed arguments.
If the output is the same as before, will keep file unchanged.
"""
)
def update_codemeta(
    target: Path = trg_arg,
    sources: List[str] = src_arg,
):
    """Entry point of CLI application.

    Runs codemetapy on the passed sources,
    compares resulting graph with target file (if it exists).

    Only writes to the output if the metadata is not equivalent.
    The equivalence is checked on graph level using `rdflib`.

    Args:
        target: Output file (usually `codemeta.json`)
        sources: Metadata input files (such as `pyproject.toml`)
    """
    # load old codemeta graph (if any)
    old_metadata = rdflib.Graph()
    if target.is_file():
        with open(target, "r") as f:
            dat = json.dumps(_localize_codemeta_context(json.load(f)))
        old_metadata.parse(data=dat, format="json-ld")

    # generate new codemeta graph
    cm = _gen_codemeta(sources)
    original = _serialize_codemeta(cm)

    # only write result to file if the graph changed
    expanded = _serialize_codemeta(_localize_codemeta_context(cm))
    new_metadata = rdflib.Graph()
    new_metadata.parse(data=expanded, format="json-ld")
    if not rdflib.compare.isomorphic(old_metadata, new_metadata):
        typer.echo(f"Project metadata changed, writing {target} ...")
        with open(target, "w") as f:
            f.write(original)
