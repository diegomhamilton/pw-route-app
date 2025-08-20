# Copilot Custom Instructions for this Repository

Scope: These rules apply to all assistant responses proposing or making code changes in this repo.

1) Communicate small changes succinctly
- After any change, output a numbered list of changes. Each item must be max 2 lines and include 1–2 representative changed lines for quick overview. Do not paste full diffs or entire files.

2) One change per commit
- Propose changes so they can be committed independently. Avoid batching unrelated edits.

3) Always request testing before merging
- Explicitly ask the user: "Please test this change locally before merging."

4) Pre-fill commit message for the user
- Provide a ready commit message for copy/paste on each change, using the format below. Do not run git commands; the user will commit.

5) Merge/commit message format
- Line 1: Summary of change (exactly 1 line, max 52 characters)
- Line 2: Blank line
- Following lines: Description of change (can have multiple lines, be succinct, each line should have max 72 characters)


6) Style of responses
- Keep answers short and impersonal; prefer bullet lists. Avoid verbosity.
- Include file paths and symbols in backticks when referenced.
- Do not show entire file contents; only 1–2 representative lines for each change.

Template to include in responses for each change:

Commit message:
<summary up to 52 chars>

<description up to 72 chars per line, multiple lines allowed>

Example:
- Change summary (numbered):
  1) `route_map.py`: Set default zoom True -> False to <describe user impact>
     `zoom = st.sidebar.checkbox("Zoom Route View", value=False)`
- Commit message:
  Add default Zoom off in sidebar
  Change default Zoom checkbox to False for clearer initial view
