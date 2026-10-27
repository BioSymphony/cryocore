# Public Releases

Release CryoCore updates through a branch and pull request in the public
repository. Keep its public history when adding reviewed tools, examples,
and documentation.

## Prepare An Update

1. Select the reusable source files, tests, and examples for the change.
2. Update the tool registry and usage guides. Preserve each source-review date.
3. Refresh bundled skill references from the public documents.
4. Run the release checks with Gitleaks installed:

   ```bash
   make release-check REQUIRE_GITLEAKS=1
   ```

5. Inspect the complete diff, including examples, images, comments, and workflow
   artifacts. Commit the reviewed files and open a pull request.
6. Merge after the required CI checks pass.

The release check covers documentation links, contracts, tool records, tests,
public-content checks, and secret scanning. The optional adapter CI job also
runs MRC tests with their scientific dependencies.

## Create A Versioned Release

1. Tag the reviewed public commit with a `v*` tag.
2. Check the tagged checkout:

   ```bash
   python3 scripts/cryocore/public_release_report.py \
     --repo-root . --publish-ready --json
   ```

3. Push the tag and verify the release workflow. It creates a source archive,
   checksums, and a public summary containing check results and the commit ID.

Use `--public-summary` when saving a report for distribution. Full diagnostic
reports remain local. Keep runtime data, credentials, downloaded models, and
operator records outside release packages.

See the [release checklist](docs/public-switch-checklist.md) and
[contributing guide](CONTRIBUTING.md) for individual checks.
