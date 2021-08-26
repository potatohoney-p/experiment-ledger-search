# Experiment Ledger Search

Record local experiment parameters, metric steps, and artifact digests in a searchable SQLite ledger.

## Run locally

Use a currently supported Python 3 interpreter. No third-party packages, credentials, downloads, or network access are required.

```sh
python -m unittest discover -s tests -v
python demo.py
```

Run from the repository directory. The demo reads `examples/input.json`; inputs are reproducible, authored examples.

## Scope and behavior

Metric steps are immutable and duplicate writes fail. Ranking compares the latest metric step of finished runs only; a failed or running run cannot win. Artifact SHA-256 hashes identify bytes without executing or deserializing model files. This local teaching ledger has no service, distributed locking protocol, or MLflow dependency. Demo metrics are authored numbers, not measured model results.

## Layout

- `core.py`: primary algorithm or storage contract.
- `features.py`: pipeline or integration layer.
- `tests/`: independent behavioral assertions, failure cases, and regressions.
- `demo.py` and `examples/input.json`: repeatable end-to-end example.

## Example output

```json
{
  "best": [
    "run-a",
    0.2
  ],
  "runs": [
    {
      "id": "run-a",
      "params": {
        "model": "linear",
        "rate": 0.1
      },
      "status": "finished"
    },
    {
      "id": "run-b",
      "params": {
        "model": "linear",
        "rate": 0.01
      },
      "status": "finished"
    }
  ]
}
```

## Compatibility and license

The implementation uses language features and standard-library APIs available in [Python 3.4](https://docs.python.org/3.4/library/index.html), released in [March 2014](https://www.python.org/downloads/release/python-340/). Use a supported runtime; an old interpreter is not required. Compatibility with a historical runtime is not certified by current-runtime tests.

MIT licensed. No third-party source code or datasets are bundled.
