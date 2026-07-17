CREATE TABLE schema_migrations (
    version INTEGER PRIMARY KEY CHECK (version > 0),
    name TEXT NOT NULL UNIQUE,
    checksum TEXT NOT NULL CHECK (length(checksum) = 64),
    applied_at TEXT NOT NULL
);

CREATE TABLE goals (
    goal_id TEXT PRIMARY KEY,
    schema_version TEXT NOT NULL,
    goal_text TEXT NOT NULL,
    goal_sha256 TEXT NOT NULL CHECK (length(goal_sha256) = 64),
    completion_contract_json TEXT NOT NULL,
    completion_contract_sha256 TEXT NOT NULL CHECK (length(completion_contract_sha256) = 64),
    original_guards_json TEXT NOT NULL,
    repository_binding_json TEXT NOT NULL,
    repository_fingerprint TEXT NOT NULL CHECK (length(repository_fingerprint) = 64),
    authorization_json TEXT NOT NULL,
    record_json TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    deadline_at TEXT NOT NULL,
    state_revision INTEGER NOT NULL CHECK (state_revision > 0),
    phase TEXT NOT NULL,
    current_generation INTEGER NOT NULL CHECK (current_generation >= 0),
    passes_consumed INTEGER NOT NULL CHECK (passes_consumed >= 0),
    goal_evaluation TEXT NOT NULL CHECK (goal_evaluation IN ('unmet', 'met', 'indeterminate')),
    last_fingerprint TEXT NOT NULL CHECK (length(last_fingerprint) = 64),
    terminal_reason TEXT
);

CREATE TRIGGER goals_immutable_original
BEFORE UPDATE OF goal_text, goal_sha256, completion_contract_json,
                 completion_contract_sha256, original_guards_json,
                 repository_binding_json, repository_fingerprint,
                 authorization_json, created_at
ON goals
BEGIN
    SELECT RAISE(ABORT, 'immutable goal fields cannot be changed');
END;

CREATE TABLE goal_amendments (
    goal_id TEXT NOT NULL REFERENCES goals(goal_id),
    sequence INTEGER NOT NULL CHECK (sequence > 0),
    kind TEXT NOT NULL CHECK (kind IN ('completion_contract', 'guards')),
    user_authorization TEXT NOT NULL,
    prior_effective_sha256 TEXT NOT NULL CHECK (length(prior_effective_sha256) = 64),
    new_value_json TEXT NOT NULL,
    new_sha256 TEXT NOT NULL CHECK (length(new_sha256) = 64),
    created_at TEXT NOT NULL,
    PRIMARY KEY (goal_id, sequence)
);

CREATE TABLE generations (
    goal_id TEXT NOT NULL REFERENCES goals(goal_id),
    generation INTEGER NOT NULL CHECK (generation > 0),
    handoff_token TEXT NOT NULL,
    idempotency_key TEXT NOT NULL UNIQUE,
    phase TEXT NOT NULL,
    lease_token TEXT NOT NULL,
    invocation_consumed INTEGER NOT NULL CHECK (invocation_consumed IN (0, 1)),
    invocation_state TEXT NOT NULL CHECK (invocation_state IN ('not_authorized', 'authorized', 'returned', 'unknown')),
    consumed_at TEXT,
    returned_at TEXT,
    before_fingerprint TEXT NOT NULL CHECK (length(before_fingerprint) = 64),
    after_fingerprint TEXT,
    fingerprint_status TEXT CHECK (fingerprint_status IS NULL OR fingerprint_status IN ('new', 'unchanged', 'repeated')),
    pending_step_result_json TEXT,
    finalized_receipt_hash TEXT,
    terminal_or_successor_outcome TEXT,
    claimed_at TEXT,
    successor_thread_id TEXT,
    PRIMARY KEY (goal_id, generation),
    UNIQUE (goal_id, handoff_token),
    CHECK ((invocation_consumed = 0 AND invocation_state = 'not_authorized' AND consumed_at IS NULL)
        OR (invocation_consumed = 1 AND invocation_state IN ('authorized', 'returned', 'unknown') AND consumed_at IS NOT NULL))
);

CREATE TABLE leases (
    lease_id INTEGER PRIMARY KEY AUTOINCREMENT,
    repository_fingerprint TEXT NOT NULL CHECK (length(repository_fingerprint) = 64),
    goal_id TEXT NOT NULL REFERENCES goals(goal_id),
    generation INTEGER NOT NULL CHECK (generation >= 0),
    holder_kind TEXT NOT NULL CHECK (holder_kind IN ('launcher', 'continuation', 'successor_reserved', 'quarantined')),
    holder_token TEXT NOT NULL,
    transaction_id TEXT NOT NULL UNIQUE,
    acquired_at TEXT NOT NULL,
    heartbeat_at TEXT NOT NULL,
    expires_at TEXT NOT NULL,
    lease_state TEXT NOT NULL CHECK (lease_state IN ('active', 'released')),
    released_at TEXT
);

CREATE UNIQUE INDEX one_active_lease_per_worktree
ON leases(repository_fingerprint) WHERE lease_state = 'active';

CREATE UNIQUE INDEX one_active_lease_per_goal
ON leases(goal_id) WHERE lease_state = 'active';

CREATE TABLE events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    goal_id TEXT NOT NULL REFERENCES goals(goal_id),
    sequence INTEGER NOT NULL CHECK (sequence > 0),
    kind TEXT NOT NULL CHECK (kind IN ('event', 'step_receipt', 'recovery', 'amendment')),
    payload_json TEXT NOT NULL,
    prior_hash TEXT,
    event_hash TEXT NOT NULL UNIQUE CHECK (length(event_hash) = 64),
    created_at TEXT NOT NULL,
    UNIQUE (goal_id, sequence)
);

CREATE TABLE step_receipts (
    receipt_id INTEGER PRIMARY KEY AUTOINCREMENT,
    goal_id TEXT NOT NULL REFERENCES goals(goal_id),
    generation INTEGER NOT NULL CHECK (generation > 0),
    receipt_kind TEXT NOT NULL,
    payload_json TEXT NOT NULL,
    receipt_hash TEXT NOT NULL UNIQUE CHECK (length(receipt_hash) = 64),
    finalized_at TEXT NOT NULL,
    UNIQUE (goal_id, generation),
    FOREIGN KEY (goal_id, generation) REFERENCES generations(goal_id, generation)
);

CREATE TABLE successor_intents (
    intent_id INTEGER PRIMARY KEY AUTOINCREMENT,
    goal_id TEXT NOT NULL REFERENCES goals(goal_id),
    generation INTEGER NOT NULL CHECK (generation > 0),
    handoff_token TEXT NOT NULL,
    idempotency_key TEXT NOT NULL UNIQUE,
    predecessor_thread_id TEXT,
    successor_thread_id TEXT,
    provider_state TEXT NOT NULL CHECK (provider_state IN ('intent', 'returned', 'ambiguous', 'failed', 'timeout', 'duplicate')),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    UNIQUE (goal_id, generation),
    FOREIGN KEY (goal_id, generation) REFERENCES generations(goal_id, generation)
);

CREATE TABLE provider_receipts (
    provider_receipt_id INTEGER PRIMARY KEY AUTOINCREMENT,
    goal_id TEXT NOT NULL REFERENCES goals(goal_id),
    generation INTEGER NOT NULL CHECK (generation > 0),
    provider_id TEXT NOT NULL,
    idempotency_key TEXT NOT NULL,
    provider_status TEXT NOT NULL CHECK (provider_status IN ('returned', 'definitive_failure', 'ambiguous', 'timeout', 'duplicate')),
    returned_thread_id TEXT,
    response_json TEXT NOT NULL,
    created_at TEXT NOT NULL,
    UNIQUE (provider_id, idempotency_key),
    FOREIGN KEY (goal_id, generation) REFERENCES generations(goal_id, generation)
);

CREATE TABLE recovery_actions (
    recovery_action_id INTEGER PRIMARY KEY AUTOINCREMENT,
    goal_id TEXT NOT NULL REFERENCES goals(goal_id),
    sequence INTEGER NOT NULL CHECK (sequence > 0),
    action TEXT NOT NULL,
    user_authorization TEXT NOT NULL,
    evidence_json TEXT NOT NULL,
    prior_phase TEXT NOT NULL,
    resulting_phase TEXT NOT NULL,
    action_hash TEXT NOT NULL UNIQUE CHECK (length(action_hash) = 64),
    created_at TEXT NOT NULL,
    UNIQUE (goal_id, sequence)
);

CREATE TABLE fingerprints (
    goal_id TEXT NOT NULL REFERENCES goals(goal_id),
    sequence INTEGER NOT NULL CHECK (sequence >= 0),
    fingerprint TEXT NOT NULL CHECK (length(fingerprint) = 64),
    classification TEXT NOT NULL CHECK (classification IN ('initial', 'new', 'unchanged', 'repeated')),
    payload_json TEXT,
    PRIMARY KEY (goal_id, sequence)
);

CREATE INDEX events_goal_sequence ON events(goal_id, sequence);
CREATE INDEX generations_goal_phase ON generations(goal_id, phase);
CREATE INDEX leases_goal_state ON leases(goal_id, lease_state);
