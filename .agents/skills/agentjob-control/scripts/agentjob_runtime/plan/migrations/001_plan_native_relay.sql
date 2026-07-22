PRAGMA foreign_keys = ON;

CREATE TABLE schema_metadata (
    singleton INTEGER PRIMARY KEY CHECK (singleton = 1),
    schema_version TEXT NOT NULL,
    relay_profile TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE relay_runs (
    run_id TEXT PRIMARY KEY,
    plan_id TEXT NOT NULL,
    plan_sha256 TEXT NOT NULL CHECK (length(plan_sha256) = 64),
    plan_json TEXT NOT NULL CHECK (json_valid(plan_json)),
    acceptance_sha256 TEXT NOT NULL CHECK (length(acceptance_sha256) = 64),
    repository_binding_json TEXT NOT NULL CHECK (json_valid(repository_binding_json)),
    repository_binding_sha256 TEXT NOT NULL CHECK (length(repository_binding_sha256) = 64),
    repository_fingerprint TEXT NOT NULL,
    control_fingerprint TEXT NOT NULL,
    relay_profile TEXT NOT NULL CHECK (relay_profile = 'recursive_chain_v1'),
    relay_topology TEXT NOT NULL CHECK (relay_topology = 'recursive_chain_v1'),
    launcher_thread_id TEXT NOT NULL,
    requested_effort TEXT NOT NULL,
    revision INTEGER NOT NULL CHECK (revision > 0),
    status TEXT NOT NULL CHECK (status IN (
        'active', 'human_gate', 'integrity_stop', 'validation_failed',
        'capability_blocked', 'invocation_unknown', 'cancelled', 'plan_complete'
    )),
    current_generation INTEGER NOT NULL CHECK (current_generation > 0),
    completion_report_sha256 TEXT,
    cancellation_reason TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    UNIQUE (plan_id, plan_sha256, repository_fingerprint)
);

CREATE TABLE relay_generations (
    run_id TEXT NOT NULL REFERENCES relay_runs(run_id),
    generation INTEGER NOT NULL CHECK (generation > 0),
    task_id TEXT NOT NULL,
    task_sha256 TEXT NOT NULL CHECK (length(task_sha256) = 64),
    predecessor_thread_id TEXT NOT NULL,
    predecessor_receipt_sha256 TEXT,
    worker_thread_id TEXT,
    requested_effort TEXT NOT NULL,
    effective_effort TEXT,
    status TEXT NOT NULL CHECK (status IN (
        'dispatch_pending', 'reserved', 'claimed', 'consumed', 'returned',
        'invocation_unknown', 'receipt_finalized', 'successor_reserved',
        'human_gate', 'integrity_stop', 'validation_failed',
        'capability_blocked', 'cancelled'
    )),
    handoff_token_sha256 TEXT NOT NULL CHECK (length(handoff_token_sha256) = 64),
    envelope_sha256 TEXT NOT NULL CHECK (length(envelope_sha256) = 64),
    invocation_count INTEGER NOT NULL DEFAULT 0 CHECK (invocation_count IN (0, 1)),
    result_json TEXT CHECK (result_json IS NULL OR json_valid(result_json)),
    result_sha256 TEXT,
    receipt_sha256 TEXT,
    successor_generation INTEGER,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    PRIMARY KEY (run_id, generation),
    UNIQUE (run_id, task_id)
);

CREATE UNIQUE INDEX relay_one_active_generation
ON relay_generations(run_id)
WHERE status IN ('dispatch_pending', 'reserved', 'claimed', 'consumed', 'returned');

CREATE TABLE task_envelopes (
    run_id TEXT NOT NULL,
    generation INTEGER NOT NULL,
    envelope_json TEXT NOT NULL CHECK (json_valid(envelope_json)),
    envelope_sha256 TEXT NOT NULL UNIQUE CHECK (length(envelope_sha256) = 64),
    PRIMARY KEY (run_id, generation),
    FOREIGN KEY (run_id, generation) REFERENCES relay_generations(run_id, generation)
);

CREATE TABLE dispatch_intents (
    intent_id TEXT PRIMARY KEY,
    run_id TEXT NOT NULL,
    generation INTEGER NOT NULL,
    idempotency_key TEXT NOT NULL UNIQUE,
    create_budget INTEGER NOT NULL CHECK (create_budget = 1),
    attempt_count INTEGER NOT NULL CHECK (attempt_count IN (0, 1)),
    status TEXT NOT NULL CHECK (status IN (
        'pending', 'creating', 'returned', 'recorded', 'ambiguous',
        'failed_before_create', 'human_gate'
    )),
    requested_effort TEXT NOT NULL,
    child_thread_id TEXT,
    provider_response_json TEXT CHECK (provider_response_json IS NULL OR json_valid(provider_response_json)),
    provider_response_sha256 TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    UNIQUE (run_id, generation),
    FOREIGN KEY (run_id, generation) REFERENCES relay_generations(run_id, generation)
);

CREATE TABLE task_receipts (
    receipt_id TEXT PRIMARY KEY,
    run_id TEXT NOT NULL,
    generation INTEGER NOT NULL,
    receipt_json TEXT NOT NULL CHECK (json_valid(receipt_json)),
    receipt_sha256 TEXT NOT NULL UNIQUE CHECK (length(receipt_sha256) = 64),
    created_at TEXT NOT NULL,
    UNIQUE (run_id, generation),
    FOREIGN KEY (run_id, generation) REFERENCES relay_generations(run_id, generation)
);

CREATE TABLE relay_leases (
    run_id TEXT PRIMARY KEY REFERENCES relay_runs(run_id),
    repository_fingerprint TEXT NOT NULL UNIQUE,
    holder_kind TEXT NOT NULL CHECK (holder_kind IN ('launcher', 'worker', 'successor_reserved', 'quarantined')),
    holder_generation INTEGER,
    holder_thread_id TEXT NOT NULL,
    holder_token_sha256 TEXT NOT NULL CHECK (length(holder_token_sha256) = 64),
    heartbeat_at TEXT NOT NULL,
    expires_at TEXT NOT NULL,
    released_at TEXT
);

CREATE UNIQUE INDEX relay_one_active_repository_lease
ON relay_leases(repository_fingerprint)
WHERE released_at IS NULL;

CREATE TABLE completion_reports (
    run_id TEXT PRIMARY KEY REFERENCES relay_runs(run_id),
    report_json TEXT NOT NULL CHECK (json_valid(report_json)),
    report_sha256 TEXT NOT NULL UNIQUE CHECK (length(report_sha256) = 64),
    created_at TEXT NOT NULL
);

CREATE TABLE goal_mirrors (
    run_id TEXT PRIMARY KEY REFERENCES relay_runs(run_id),
    mirror_id TEXT NOT NULL,
    may_mark_complete INTEGER NOT NULL CHECK (may_mark_complete = 0),
    projection_json TEXT NOT NULL CHECK (json_valid(projection_json)),
    projection_sha256 TEXT NOT NULL CHECK (length(projection_sha256) = 64),
    last_error TEXT,
    updated_at TEXT NOT NULL
);

CREATE TABLE relay_journal (
    run_id TEXT NOT NULL REFERENCES relay_runs(run_id),
    sequence INTEGER NOT NULL CHECK (sequence > 0),
    kind TEXT NOT NULL,
    payload_json TEXT NOT NULL CHECK (json_valid(payload_json)),
    payload_sha256 TEXT NOT NULL CHECK (length(payload_sha256) = 64),
    prior_entry_sha256 TEXT,
    entry_sha256 TEXT NOT NULL UNIQUE CHECK (length(entry_sha256) = 64),
    created_at TEXT NOT NULL,
    PRIMARY KEY (run_id, sequence)
);

CREATE TRIGGER task_envelopes_no_update BEFORE UPDATE ON task_envelopes
BEGIN SELECT RAISE(ABORT, 'task envelopes are immutable'); END;
CREATE TRIGGER task_envelopes_no_delete BEFORE DELETE ON task_envelopes
BEGIN SELECT RAISE(ABORT, 'task envelopes are immutable'); END;
CREATE TRIGGER task_receipts_no_update BEFORE UPDATE ON task_receipts
BEGIN SELECT RAISE(ABORT, 'task receipts are immutable'); END;
CREATE TRIGGER task_receipts_no_delete BEFORE DELETE ON task_receipts
BEGIN SELECT RAISE(ABORT, 'task receipts are immutable'); END;
CREATE TRIGGER completion_reports_no_update BEFORE UPDATE ON completion_reports
BEGIN SELECT RAISE(ABORT, 'completion reports are immutable'); END;
CREATE TRIGGER completion_reports_no_delete BEFORE DELETE ON completion_reports
BEGIN SELECT RAISE(ABORT, 'completion reports are immutable'); END;
CREATE TRIGGER relay_journal_no_update BEFORE UPDATE ON relay_journal
BEGIN SELECT RAISE(ABORT, 'relay journal is append-only'); END;
CREATE TRIGGER relay_journal_no_delete BEFORE DELETE ON relay_journal
BEGIN SELECT RAISE(ABORT, 'relay journal is append-only'); END;
