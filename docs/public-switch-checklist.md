# Public Release Checklist

Use this checklist for updates to the public CryoCore repository.

- Select reusable source, tests, and public examples.
- Keep the existing public Git history.
- Check documentation links and refresh bundled skill references.
- Record tool versions, source revisions, checkpoint identities, and applicable terms.
- Run `make release-check REQUIRE_GITLEAKS=1`.
- Run the optional adapter tests with NumPy and mrcfile installed.
- Inspect filenames, comments, figures, examples, and packaged reports for local details.
- Open a pull request and verify CI before merging.
- For a versioned release, tag the reviewed commit and run `--publish-ready`.

The [release procedure](../PUBLIC_RELEASE.md) gives the commands. Publish the
allowlisted report produced by `--public-summary`; retain full diagnostics
with the local review.
