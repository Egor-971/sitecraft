# Contributing

Use a concrete failure or use case to improve Sitecraft. A new rule should change a useful decision without imposing an unrelated style or workflow on every project. Keep skill descriptions focused, and place conditional detail in the relevant reference. Preserve implicit discovery and explicit user authorization.

Follow the [Code of Conduct](CODE_OF_CONDUCT.md). Use the issue forms for bugs, feature requests and accessibility barriers. Report vulnerabilities through the private channel in [SECURITY.md](SECURITY.md), rather than public issues. See [ACCESSIBILITY.md](ACCESSIBILITY.md) for scope and current limits.

## A useful report

Include the plugin version, skill invocation, goal, relevant stack, observed result and expected behavior. Distinguish the initial implementation from internal fixes and final delivery. For UI issues, include the affected state and viewport, accessible screenshots, input steps and any relevant runtime error. Redact credentials, private account data and client material. Do not upload a full private conversation.

## Validation

Run the package validator and unit tests after relevant changes. Strict validation requires the dependencies in `requirements-dev.txt`; it uses the official schema or an explicit saved schema with `--schema`.

```sh
python3 scripts/validate_plugin.py
python3 -m unittest discover -s tests -v
python3 scripts/build_release.py --output-dir dist
```

Validate behavioral changes on a realistic isolated task. Record what actually ran and was viewed. Do not pass an evaluation merely because the instructions contain a phrase, an image was saved, or a build succeeded. A browser limitation belongs in the result. Keep external accounts and transactions outside disposable trials.

Update both manifests together, describe the final change in `CHANGELOG.md`, and keep `docs/VALIDATION.md` accurate. New screenshots and assets need appropriate rights. Publication and profile changes are separate from source validation.
