# collectstatic manifest summary

Generated: 2025-11-19

Summary of the most recent collectstatic runs (logs moved into `docs/travelmathlite/ops/logs/`):

- Latest run: `collectstatic-manifest-clear-20251119-114700.log`
- Files copied: 129
- Manifest present: NO

Notes and next steps

- Django's `STATICFILES_STORAGE` is configured as `ManifestStaticFilesStorage` when `USE_MANIFEST_STATIC` is enabled.
- The manifest (`staticfiles.json`) was not generated in `travelmathlite/staticfiles/` during these local runs. This can be caused by unchanged files or by post-processing conditions; see the verbose log in `docs/travelmathlite/ops/logs/collectstatic-manifest-verbose-20251119-114809.log` for details.
- Recommended: run the collectstatic step in CI with `DEBUG=False` and `USE_MANIFEST_STATIC=1`; attach the `collectstatic` transcript and resulting `staticfiles.json` as ADR evidence.

Logs are archived under `docs/travelmathlite/ops/logs/`.
