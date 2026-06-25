# Logic Prototype

Use this branch when the question is about business logic, state transitions,
content/data shape, manifest behavior, validation behavior, or workflow rules.
The prototype should let the user drive cases that are hard to reason about on
paper.

If the question is "what should this look like?", use `UI.md` instead.

## Good fit

- "Does this state model handle the edge case where X then Y?"
- "Does this manifest shape represent source provenance clearly?"
- "What should this validation workflow accept and reject?"
- "I want to feel out an API before production code."
- Any case where the user should press keys or run commands and watch state
  change.

## Process

### 1. State the question

Before writing code, write one paragraph at the top of the prototype or in a
nearby `README.md` / `NOTES.md`:

- the state model or data shape being explored;
- the question being answered;
- why this is a prototype rather than production code.

### 2. Pick the runtime

Use the host project's existing runtime:

- TypeScript/Node for frontend-adjacent website behavior.
- Python for manifest, asset, validation, or source-ingestion behavior when it
  matches existing scripts.
- Bash only for thin orchestration around existing commands.

Do not add a new package manager or runtime for the prototype.

### 3. Isolate the logic in a portable module

Put the logic being tested behind a small, pure interface that could be lifted
into real code later. The terminal shell or command wrapper is disposable; the
logic module should remain easy to extract.

Useful shapes:

- A reducer: `(state, action) => state`.
- A state machine with explicit states and transitions.
- Pure functions over plain data.
- A small class or module with a clear method surface when internal state is
  genuinely part of the question.

Keep the logic free of terminal I/O. The shell imports it and calls it.

### 4. Build the smallest interactive shell

For terminal interaction, re-render the full frame after every action instead of
appending endless scrollback.

Each frame should show:

1. Current state, formatted one field per line or as readable JSON.
2. Keyboard shortcuts or commands at the bottom.

Basic behavior:

1. Initialize one in-memory state object.
2. Render the first frame.
3. Read one keystroke or line at a time.
4. Dispatch to a handler.
5. Re-render the full frame.
6. Loop until quit.

The whole frame should fit on one screen.

### 5. Make it runnable in one command

Use existing entry points such as `npm run <script>`, `make <target>`, or
`.venv/bin/python <path>`. If no task-runner entry is justified, put the exact
command at the top of the prototype file or local `README.md`.

### 6. Hand it over

Give the user the run command and the specific question the prototype answers.
If the user requests new actions, add them while keeping the prototype focused.

### 7. Capture the answer

When the prototype has done its job, ask what it taught or write a short
`NOTES.md` beside it. Then delete the shell or fold the validated logic into
production code with normal quality checks.

## Anti-patterns

- Do not add tests for the prototype shell.
- Do not connect to production services or the authoritative source repository
  unless the user explicitly approved that boundary.
- Do not generalize beyond the one question.
- Do not mix terminal code into the portable logic module.
- Do not ship the prototype shell as production code.
