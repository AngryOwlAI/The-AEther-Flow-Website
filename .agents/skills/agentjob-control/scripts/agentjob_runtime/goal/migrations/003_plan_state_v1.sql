-- Immutable production migration for the serial implementation-plan v1
-- profile. Existing generic goal tables and migration bytes remain unchanged.

CREATE TRIGGER schema_migrations_no_update
BEFORE UPDATE ON schema_migrations
BEGIN
    SELECT RAISE(ABORT, 'applied migrations are immutable');
END;

CREATE TRIGGER schema_migrations_no_delete
BEFORE DELETE ON schema_migrations
BEGIN
    SELECT RAISE(ABORT, 'applied migrations are immutable');
END;

CREATE TABLE plans (
    plan_id TEXT PRIMARY KEY,
    outer_goal_id TEXT NOT NULL UNIQUE REFERENCES goals(goal_id),
    plan_schema_version TEXT NOT NULL
        CHECK (plan_schema_version IN (
            'sys4ai.implementation-plan.v1',
            'sys4ai.implementation-plan.v2'
        )),
    state_schema_version TEXT NOT NULL
        CHECK (state_schema_version = 'sys4ai.implementation-plan-state.v1'),
    plan_sha256 TEXT NOT NULL CHECK (length(plan_sha256) = 64),
    effective_plan_sha256 TEXT NOT NULL
        CHECK (length(effective_plan_sha256) = 64),
    repository_binding_json TEXT NOT NULL
        CHECK (json_valid(repository_binding_json)),
    repository_fingerprint TEXT NOT NULL
        CHECK (length(repository_fingerprint) = 64),
    plan_json TEXT NOT NULL CHECK (json_valid(plan_json)),
    state_json TEXT NOT NULL CHECK (json_valid(state_json)),
    state_revision INTEGER NOT NULL CHECK (state_revision > 0),
    phase TEXT NOT NULL CHECK (phase IN (
        'initialized',
        'task_reserved',
        'task_active',
        'task_verifying',
        'continuation_required',
        'completion_candidate',
        'recovery_pending',
        'terminal_complete',
        'terminal_blocked_no_runnable',
        'terminal_awaiting_human',
        'terminal_validation_failed',
        'terminal_capability_blocked',
        'terminal_corrupt_state',
        'terminal_cancelled'
    )),
    current_generation INTEGER NOT NULL CHECK (current_generation >= 0),
    active_task_id TEXT,
    evaluation TEXT NOT NULL
        CHECK (evaluation IN ('unmet', 'met', 'indeterminate')),
    initial_fingerprint TEXT NOT NULL CHECK (length(initial_fingerprint) = 64),
    current_fingerprint TEXT NOT NULL CHECK (length(current_fingerprint) = 64),
    journal_head_sha256 TEXT
        CHECK (journal_head_sha256 IS NULL OR length(journal_head_sha256) = 64),
    terminal_reason TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    UNIQUE (plan_id, plan_sha256),
    FOREIGN KEY (plan_id, active_task_id)
        REFERENCES plan_tasks(plan_id, task_id)
        DEFERRABLE INITIALLY DEFERRED,
    CHECK (
        phase NOT IN ('task_reserved', 'task_active', 'task_verifying')
        OR active_task_id IS NOT NULL
    )
);

CREATE TABLE plan_phases (
    plan_id TEXT NOT NULL REFERENCES plans(plan_id),
    phase_id TEXT NOT NULL,
    canonical_position INTEGER NOT NULL CHECK (canonical_position >= 0),
    phase_sha256 TEXT NOT NULL CHECK (length(phase_sha256) = 64),
    phase_json TEXT NOT NULL CHECK (json_valid(phase_json)),
    PRIMARY KEY (plan_id, phase_id),
    UNIQUE (plan_id, canonical_position)
);

CREATE TABLE plan_phase_dependencies (
    plan_id TEXT NOT NULL,
    phase_id TEXT NOT NULL,
    depends_on_phase_id TEXT NOT NULL,
    dependency_position INTEGER NOT NULL CHECK (dependency_position >= 0),
    PRIMARY KEY (plan_id, phase_id, depends_on_phase_id),
    UNIQUE (plan_id, phase_id, dependency_position),
    FOREIGN KEY (plan_id, phase_id)
        REFERENCES plan_phases(plan_id, phase_id),
    FOREIGN KEY (plan_id, depends_on_phase_id)
        REFERENCES plan_phases(plan_id, phase_id),
    CHECK (phase_id <> depends_on_phase_id)
);

CREATE TABLE plan_tasks (
    plan_id TEXT NOT NULL REFERENCES plans(plan_id),
    task_id TEXT NOT NULL,
    task_sha256 TEXT NOT NULL CHECK (length(task_sha256) = 64),
    phase_id TEXT NOT NULL,
    canonical_position INTEGER NOT NULL CHECK (canonical_position >= 0),
    origin_kind TEXT NOT NULL
        CHECK (origin_kind IN ('canonical', 'replacement')),
    task_json TEXT NOT NULL CHECK (json_valid(task_json)),
    PRIMARY KEY (plan_id, task_id),
    UNIQUE (plan_id, canonical_position),
    UNIQUE (plan_id, task_id, task_sha256),
    FOREIGN KEY (plan_id, phase_id)
        REFERENCES plan_phases(plan_id, phase_id)
);

CREATE TABLE plan_task_dependencies (
    plan_id TEXT NOT NULL,
    task_id TEXT NOT NULL,
    depends_on_task_id TEXT NOT NULL,
    dependency_position INTEGER NOT NULL CHECK (dependency_position >= 0),
    PRIMARY KEY (plan_id, task_id, depends_on_task_id),
    UNIQUE (plan_id, task_id, dependency_position),
    FOREIGN KEY (plan_id, task_id)
        REFERENCES plan_tasks(plan_id, task_id),
    FOREIGN KEY (plan_id, depends_on_task_id)
        REFERENCES plan_tasks(plan_id, task_id),
    CHECK (task_id <> depends_on_task_id)
);

CREATE TABLE plan_receipts (
    receipt_id TEXT PRIMARY KEY,
    plan_id TEXT NOT NULL REFERENCES plans(plan_id),
    receipt_kind TEXT NOT NULL
        CHECK (receipt_kind IN ('task', 'phase_gate', 'plan_completion')),
    task_id TEXT,
    phase_id TEXT,
    generation INTEGER CHECK (generation IS NULL OR generation > 0),
    disposition TEXT NOT NULL,
    reason_code TEXT NOT NULL CHECK (length(reason_code) > 0),
    acceptance_status TEXT NOT NULL
        CHECK (acceptance_status IN (
            'pass', 'fail', 'indeterminate', 'not_applicable'
        )),
    validator_status TEXT NOT NULL
        CHECK (validator_status IN (
            'pass', 'fail', 'indeterminate', 'not_applicable'
        )),
    checkpoint_status TEXT NOT NULL
        CHECK (checkpoint_status IN (
            'pass', 'fail', 'not_required', 'unknown', 'not_applicable'
        )),
    record_json TEXT NOT NULL CHECK (json_valid(record_json)),
    receipt_sha256 TEXT NOT NULL UNIQUE CHECK (length(receipt_sha256) = 64),
    finalized INTEGER NOT NULL CHECK (finalized = 1),
    finalized_at TEXT NOT NULL,
    UNIQUE (plan_id, task_id, receipt_id),
    FOREIGN KEY (plan_id, task_id)
        REFERENCES plan_tasks(plan_id, task_id),
    FOREIGN KEY (plan_id, phase_id)
        REFERENCES plan_phases(plan_id, phase_id),
    CHECK (
        (receipt_kind = 'task'
            AND task_id IS NOT NULL
            AND phase_id IS NULL
            AND generation IS NOT NULL)
        OR
        (receipt_kind = 'phase_gate'
            AND task_id IS NULL
            AND phase_id IS NOT NULL
            AND generation IS NULL)
        OR
        (receipt_kind = 'plan_completion'
            AND task_id IS NULL
            AND phase_id IS NULL
            AND generation IS NULL)
    ),
    CHECK (
        (receipt_kind = 'task' AND disposition IN (
            'blocked',
            'replan_required',
            'human_gate_required',
            'validation_failed',
            'invocation_unknown',
            'cancelled',
            'task_complete'
        ))
        OR
        (receipt_kind = 'phase_gate' AND disposition IN (
            'pass', 'fail', 'indeterminate'
        ))
        OR
        (receipt_kind = 'plan_completion' AND disposition IN (
            'plan_complete',
            'blocked',
            'validation_failed',
            'human_gate_required',
            'invocation_unknown',
            'cancelled'
        ))
    )
);

CREATE UNIQUE INDEX one_task_receipt_per_task
ON plan_receipts(plan_id, task_id)
WHERE receipt_kind = 'task';

CREATE UNIQUE INDEX one_task_receipt_per_generation
ON plan_receipts(plan_id, generation)
WHERE receipt_kind = 'task';

CREATE UNIQUE INDEX one_phase_gate_receipt_per_phase
ON plan_receipts(plan_id, phase_id)
WHERE receipt_kind = 'phase_gate';

CREATE UNIQUE INDEX one_completion_receipt_per_plan
ON plan_receipts(plan_id)
WHERE receipt_kind = 'plan_completion';

CREATE TABLE plan_task_states (
    plan_id TEXT NOT NULL,
    task_id TEXT NOT NULL,
    task_sha256 TEXT NOT NULL CHECK (length(task_sha256) = 64),
    lifecycle_status TEXT NOT NULL CHECK (lifecycle_status IN (
        'pending',
        'reserved',
        'active',
        'verifying',
        'completed',
        'blocked',
        'superseded',
        'replan_required',
        'human_gate_required',
        'validation_failed',
        'invocation_unknown',
        'cancelled'
    )),
    generation INTEGER CHECK (generation IS NULL OR generation > 0),
    worker_discussions INTEGER NOT NULL
        CHECK (worker_discussions BETWEEN 0 AND 1),
    continue_invocations INTEGER NOT NULL
        CHECK (continue_invocations BETWEEN 0 AND 1),
    agentjobs INTEGER NOT NULL CHECK (agentjobs BETWEEN 0 AND 1),
    provider_creates INTEGER NOT NULL
        CHECK (provider_creates BETWEEN 0 AND 1),
    successor_creates INTEGER NOT NULL
        CHECK (successor_creates BETWEEN 0 AND 1),
    same_task_successors INTEGER NOT NULL CHECK (same_task_successors = 0),
    receipt_id TEXT,
    receipt_sha256 TEXT
        CHECK (receipt_sha256 IS NULL OR length(receipt_sha256) = 64),
    fingerprint_before TEXT
        CHECK (fingerprint_before IS NULL OR length(fingerprint_before) = 64),
    fingerprint_after TEXT
        CHECK (fingerprint_after IS NULL OR length(fingerprint_after) = 64),
    terminal_reason TEXT,
    lifecycle_json TEXT NOT NULL CHECK (json_valid(lifecycle_json)),
    updated_at TEXT NOT NULL,
    PRIMARY KEY (plan_id, task_id),
    FOREIGN KEY (plan_id, task_id, task_sha256)
        REFERENCES plan_tasks(plan_id, task_id, task_sha256),
    FOREIGN KEY (plan_id, task_id, receipt_id)
        REFERENCES plan_receipts(plan_id, task_id, receipt_id)
        DEFERRABLE INITIALLY DEFERRED,
    CHECK (
        lifecycle_status <> 'pending'
        OR (
            generation IS NULL
            AND worker_discussions = 0
            AND continue_invocations = 0
            AND agentjobs = 0
            AND provider_creates = 0
            AND successor_creates = 0
            AND receipt_id IS NULL
            AND receipt_sha256 IS NULL
            AND fingerprint_before IS NULL
            AND fingerprint_after IS NULL
            AND terminal_reason IS NULL
        )
    ),
    CHECK (
        lifecycle_status NOT IN ('reserved', 'active', 'verifying')
        OR (
            generation IS NOT NULL
            AND receipt_id IS NULL
            AND receipt_sha256 IS NULL
            AND terminal_reason IS NULL
        )
    ),
    CHECK (
        lifecycle_status NOT IN (
            'completed',
            'blocked',
            'superseded',
            'replan_required',
            'human_gate_required',
            'validation_failed',
            'invocation_unknown',
            'cancelled'
        )
        OR (
            generation IS NOT NULL
            AND receipt_id IS NOT NULL
            AND receipt_sha256 IS NOT NULL
            AND fingerprint_before IS NOT NULL
            AND fingerprint_after IS NOT NULL
        )
    ),
    CHECK (
        lifecycle_status <> 'completed'
        OR terminal_reason IS NULL
    ),
    CHECK (
        lifecycle_status NOT IN (
            'blocked',
            'superseded',
            'replan_required',
            'human_gate_required',
            'validation_failed',
            'invocation_unknown',
            'cancelled'
        )
        OR terminal_reason IS NOT NULL
    )
);

CREATE UNIQUE INDEX one_active_plan_task
ON plan_task_states(plan_id)
WHERE lifecycle_status IN ('reserved', 'active', 'verifying');

CREATE UNIQUE INDEX one_plan_task_per_generation
ON plan_task_states(plan_id, generation)
WHERE generation IS NOT NULL;

CREATE INDEX plan_task_states_status
ON plan_task_states(plan_id, lifecycle_status);

CREATE TABLE plan_amendments (
    amendment_id TEXT PRIMARY KEY,
    plan_id TEXT NOT NULL REFERENCES plans(plan_id),
    sequence INTEGER NOT NULL CHECK (sequence > 0),
    prior_effective_plan_sha256 TEXT NOT NULL
        CHECK (length(prior_effective_plan_sha256) = 64),
    new_effective_plan_sha256 TEXT NOT NULL
        CHECK (length(new_effective_plan_sha256) = 64),
    prior_journal_sha256 TEXT NOT NULL
        CHECK (length(prior_journal_sha256) = 64),
    record_json TEXT NOT NULL CHECK (json_valid(record_json)),
    amendment_sha256 TEXT NOT NULL UNIQUE CHECK (length(amendment_sha256) = 64),
    finalized INTEGER NOT NULL CHECK (finalized = 1),
    created_at TEXT NOT NULL,
    UNIQUE (plan_id, sequence)
);

CREATE TABLE plan_supersessions (
    supersession_id TEXT PRIMARY KEY,
    plan_id TEXT NOT NULL REFERENCES plans(plan_id),
    original_task_id TEXT NOT NULL,
    original_task_sha256 TEXT NOT NULL
        CHECK (length(original_task_sha256) = 64),
    original_receipt_id TEXT NOT NULL REFERENCES plan_receipts(receipt_id),
    replacement_graph_sha256 TEXT NOT NULL
        CHECK (length(replacement_graph_sha256) = 64),
    reason_code TEXT NOT NULL,
    record_json TEXT NOT NULL CHECK (json_valid(record_json)),
    supersession_sha256 TEXT NOT NULL UNIQUE
        CHECK (length(supersession_sha256) = 64),
    finalized INTEGER NOT NULL CHECK (finalized = 1),
    created_at TEXT NOT NULL,
    UNIQUE (plan_id, original_task_id),
    UNIQUE (supersession_id, plan_id),
    FOREIGN KEY (plan_id, original_task_id, original_task_sha256)
        REFERENCES plan_tasks(plan_id, task_id, task_sha256),
    FOREIGN KEY (plan_id, original_task_id, original_receipt_id)
        REFERENCES plan_receipts(plan_id, task_id, receipt_id)
);

CREATE TABLE plan_supersession_replacements (
    supersession_id TEXT NOT NULL
        REFERENCES plan_supersessions(supersession_id),
    plan_id TEXT NOT NULL,
    replacement_task_id TEXT NOT NULL,
    replacement_position INTEGER NOT NULL CHECK (replacement_position >= 0),
    PRIMARY KEY (supersession_id, replacement_task_id),
    UNIQUE (supersession_id, replacement_position),
    FOREIGN KEY (supersession_id, plan_id)
        REFERENCES plan_supersessions(supersession_id, plan_id),
    FOREIGN KEY (plan_id, replacement_task_id)
        REFERENCES plan_tasks(plan_id, task_id)
);

CREATE TABLE plan_supersession_acceptance (
    supersession_id TEXT NOT NULL
        REFERENCES plan_supersessions(supersession_id),
    criterion_id TEXT NOT NULL,
    replacement_task_id TEXT NOT NULL,
    shared_gate_ref TEXT,
    PRIMARY KEY (supersession_id, criterion_id, replacement_task_id),
    FOREIGN KEY (supersession_id, replacement_task_id)
        REFERENCES plan_supersession_replacements(
            supersession_id,
            replacement_task_id
        )
);

CREATE TABLE plan_selection_proofs (
    proof_id TEXT PRIMARY KEY,
    plan_id TEXT NOT NULL REFERENCES plans(plan_id),
    plan_revision INTEGER NOT NULL CHECK (plan_revision > 0),
    outcome TEXT NOT NULL CHECK (outcome IN (
        'selected',
        'no_ready_task',
        'blocked_no_runnable',
        'completion_candidate',
        'invalid'
    )),
    selected_task_id TEXT,
    record_json TEXT NOT NULL CHECK (json_valid(record_json)),
    proof_sha256 TEXT NOT NULL UNIQUE CHECK (length(proof_sha256) = 64),
    finalized INTEGER NOT NULL CHECK (finalized = 1),
    created_at TEXT NOT NULL,
    UNIQUE (plan_id, plan_revision),
    FOREIGN KEY (plan_id, selected_task_id)
        REFERENCES plan_tasks(plan_id, task_id),
    CHECK (
        (outcome = 'selected' AND selected_task_id IS NOT NULL)
        OR (outcome <> 'selected' AND selected_task_id IS NULL)
    )
);

CREATE TABLE plan_provider_intents (
    intent_id TEXT PRIMARY KEY,
    plan_id TEXT NOT NULL REFERENCES plans(plan_id),
    task_id TEXT NOT NULL,
    task_sha256 TEXT NOT NULL CHECK (length(task_sha256) = 64),
    generation INTEGER NOT NULL CHECK (generation > 0),
    provider_id TEXT NOT NULL,
    idempotency_key TEXT NOT NULL,
    handoff_token_sha256 TEXT NOT NULL
        CHECK (length(handoff_token_sha256) = 64),
    predecessor_thread_id TEXT,
    expected_revision INTEGER NOT NULL CHECK (expected_revision >= 0),
    repository_fingerprint TEXT NOT NULL
        CHECK (length(repository_fingerprint) = 64),
    status TEXT NOT NULL CHECK (status IN (
        'intent', 'returned', 'failed', 'ambiguous', 'timeout', 'duplicate'
    )),
    provider_create_budget INTEGER NOT NULL CHECK (provider_create_budget = 1),
    create_attempts INTEGER NOT NULL CHECK (create_attempts BETWEEN 0 AND 1),
    returned_thread_id TEXT,
    provider_response_sha256 TEXT
        CHECK (
            provider_response_sha256 IS NULL
            OR length(provider_response_sha256) = 64
        ),
    retry_authorized INTEGER NOT NULL CHECK (retry_authorized = 0),
    record_json TEXT NOT NULL CHECK (json_valid(record_json)),
    intent_sha256 TEXT NOT NULL UNIQUE CHECK (length(intent_sha256) = 64),
    finalized INTEGER NOT NULL CHECK (finalized IN (0, 1)),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    UNIQUE (plan_id, generation),
    UNIQUE (provider_id, idempotency_key),
    FOREIGN KEY (plan_id, task_id, task_sha256)
        REFERENCES plan_tasks(plan_id, task_id, task_sha256),
    CHECK (
        status <> 'intent'
        OR (
            create_attempts = 0
            AND returned_thread_id IS NULL
            AND provider_response_sha256 IS NULL
            AND finalized = 0
        )
    ),
    CHECK (
        status <> 'returned'
        OR (
            create_attempts = 1
            AND returned_thread_id IS NOT NULL
            AND provider_response_sha256 IS NOT NULL
            AND finalized = 1
        )
    ),
    CHECK (
        status NOT IN ('failed', 'ambiguous', 'timeout', 'duplicate')
        OR (create_attempts = 1 AND finalized = 1)
    )
);

CREATE UNIQUE INDEX one_open_plan_provider_intent
ON plan_provider_intents(plan_id)
WHERE status = 'intent' AND finalized = 0;

CREATE TABLE plan_fingerprints (
    plan_id TEXT NOT NULL REFERENCES plans(plan_id),
    sequence INTEGER NOT NULL CHECK (sequence >= 0),
    fingerprint TEXT NOT NULL CHECK (length(fingerprint) = 64),
    classification TEXT NOT NULL CHECK (classification IN (
        'initial', 'new', 'unchanged', 'repeated'
    )),
    payload_json TEXT CHECK (payload_json IS NULL OR json_valid(payload_json)),
    PRIMARY KEY (plan_id, sequence)
);

CREATE TABLE plan_leases (
    lease_id INTEGER PRIMARY KEY AUTOINCREMENT,
    plan_id TEXT NOT NULL REFERENCES plans(plan_id),
    task_id TEXT,
    generation INTEGER NOT NULL CHECK (generation >= 0),
    holder_kind TEXT NOT NULL CHECK (holder_kind IN (
        'coordinator', 'successor_reserved', 'worker', 'quarantined'
    )),
    holder_token_sha256 TEXT NOT NULL CHECK (length(holder_token_sha256) = 64),
    transaction_id TEXT NOT NULL UNIQUE,
    outer_lease_transaction_id TEXT NOT NULL UNIQUE
        REFERENCES leases(transaction_id),
    repository_fingerprint TEXT NOT NULL
        CHECK (length(repository_fingerprint) = 64),
    acquired_at TEXT NOT NULL,
    heartbeat_at TEXT NOT NULL,
    expires_at TEXT NOT NULL,
    lease_state TEXT NOT NULL CHECK (lease_state IN ('active', 'released')),
    released_at TEXT,
    FOREIGN KEY (plan_id, task_id)
        REFERENCES plan_tasks(plan_id, task_id)
);

CREATE UNIQUE INDEX one_active_plan_lease
ON plan_leases(plan_id)
WHERE lease_state = 'active';

CREATE UNIQUE INDEX one_active_plan_lease_per_worktree
ON plan_leases(repository_fingerprint)
WHERE lease_state = 'active';

CREATE TABLE plan_events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    plan_id TEXT NOT NULL REFERENCES plans(plan_id),
    sequence INTEGER NOT NULL CHECK (sequence > 0),
    kind TEXT NOT NULL CHECK (kind IN (
        'event',
        'task_receipt',
        'phase_gate_receipt',
        'plan_completion_receipt',
        'provider_intent',
        'selection_proof',
        'amendment',
        'supersession',
        'recovery'
    )),
    payload_json TEXT NOT NULL CHECK (json_valid(payload_json)),
    prior_hash TEXT CHECK (prior_hash IS NULL OR length(prior_hash) = 64),
    event_hash TEXT NOT NULL UNIQUE CHECK (length(event_hash) = 64),
    created_at TEXT NOT NULL,
    UNIQUE (plan_id, sequence)
);

CREATE TABLE plan_recovery_actions (
    recovery_action_id TEXT PRIMARY KEY,
    plan_id TEXT NOT NULL REFERENCES plans(plan_id),
    sequence INTEGER NOT NULL CHECK (sequence > 0),
    action TEXT NOT NULL,
    user_authorization TEXT NOT NULL,
    evidence_json TEXT NOT NULL CHECK (json_valid(evidence_json)),
    prior_phase TEXT NOT NULL,
    resulting_phase TEXT NOT NULL,
    action_sha256 TEXT NOT NULL UNIQUE CHECK (length(action_sha256) = 64),
    created_at TEXT NOT NULL,
    UNIQUE (plan_id, sequence)
);

CREATE INDEX plan_tasks_canonical_order
ON plan_tasks(plan_id, canonical_position, task_id);

CREATE INDEX plan_task_dependencies_candidate
ON plan_task_dependencies(plan_id, task_id, dependency_position);

CREATE INDEX plan_receipts_task_lookup
ON plan_receipts(plan_id, task_id, receipt_kind, finalized);

CREATE INDEX plan_provider_intents_status
ON plan_provider_intents(plan_id, status, generation);

CREATE INDEX plan_events_sequence
ON plan_events(plan_id, sequence);

CREATE VIEW plan_effective_task_leaves_v1 AS
WITH RECURSIVE replacement_closure(
    plan_id,
    root_task_id,
    effective_task_id
) AS (
    SELECT plan_id, task_id, task_id
    FROM plan_tasks
    UNION
    SELECT
        closure.plan_id,
        closure.root_task_id,
        replacement.replacement_task_id
    FROM replacement_closure AS closure
    JOIN plan_supersessions AS supersession
      ON supersession.plan_id = closure.plan_id
     AND supersession.original_task_id = closure.effective_task_id
     AND supersession.finalized = 1
    JOIN plan_supersession_replacements AS replacement
      ON replacement.supersession_id = supersession.supersession_id
     AND replacement.plan_id = closure.plan_id
)
SELECT
    closure.plan_id,
    closure.root_task_id,
    closure.effective_task_id
FROM replacement_closure AS closure
WHERE NOT EXISTS (
    SELECT 1
    FROM plan_supersessions AS supersession
    WHERE supersession.plan_id = closure.plan_id
      AND supersession.original_task_id = closure.effective_task_id
      AND supersession.finalized = 1
);

CREATE VIEW plan_ready_tasks_v1 AS
SELECT
    task.plan_id,
    task.task_id,
    task.task_sha256,
    task.phase_id,
    task.canonical_position
FROM plan_tasks AS task
JOIN plan_task_states AS task_state
  ON task_state.plan_id = task.plan_id
 AND task_state.task_id = task.task_id
WHERE task_state.lifecycle_status = 'pending'
  AND NOT EXISTS (
      SELECT 1
      FROM plan_task_states AS active
      WHERE active.plan_id = task.plan_id
        AND active.lifecycle_status IN ('reserved', 'active', 'verifying')
  )
  AND NOT EXISTS (
      SELECT 1
      FROM plan_supersessions AS superseded_candidate
      WHERE superseded_candidate.plan_id = task.plan_id
        AND superseded_candidate.original_task_id = task.task_id
        AND superseded_candidate.finalized = 1
  )
  AND NOT EXISTS (
      SELECT 1
      FROM plan_task_dependencies AS dependency
      JOIN plan_effective_task_leaves_v1 AS effective
        ON effective.plan_id = dependency.plan_id
       AND effective.root_task_id = dependency.depends_on_task_id
      LEFT JOIN plan_task_states AS dependency_state
        ON dependency_state.plan_id = effective.plan_id
       AND dependency_state.task_id = effective.effective_task_id
      LEFT JOIN plan_receipts AS receipt
        ON receipt.plan_id = effective.plan_id
       AND receipt.task_id = effective.effective_task_id
       AND receipt.receipt_kind = 'task'
       AND receipt.finalized = 1
      WHERE dependency.plan_id = task.plan_id
        AND dependency.task_id = task.task_id
        AND NOT (
            dependency_state.lifecycle_status = 'completed'
            AND receipt.disposition = 'task_complete'
            AND receipt.acceptance_status = 'pass'
            AND receipt.validator_status = 'pass'
            AND receipt.checkpoint_status IN ('pass', 'not_required')
        )
  );

CREATE TRIGGER plans_revision_cas
BEFORE UPDATE ON plans
WHEN NEW.state_revision <> OLD.state_revision + 1
BEGIN
    SELECT RAISE(ABORT, 'plan state revision must advance by exactly one');
END;

CREATE TRIGGER plans_immutable_identity
BEFORE UPDATE OF
    outer_goal_id,
    plan_schema_version,
    state_schema_version,
    plan_sha256,
    repository_binding_json,
    repository_fingerprint,
    plan_json,
    initial_fingerprint,
    created_at
ON plans
BEGIN
    SELECT RAISE(ABORT, 'immutable plan identity cannot be changed');
END;

CREATE TRIGGER plans_no_delete
BEFORE DELETE ON plans
BEGIN
    SELECT RAISE(ABORT, 'plan records are append-only');
END;

CREATE TRIGGER plan_phases_no_update
BEFORE UPDATE ON plan_phases
BEGIN
    SELECT RAISE(ABORT, 'phase definitions are immutable');
END;

CREATE TRIGGER plan_phases_no_delete
BEFORE DELETE ON plan_phases
BEGIN
    SELECT RAISE(ABORT, 'phase definitions are immutable');
END;

CREATE TRIGGER plan_phase_dependencies_no_update
BEFORE UPDATE ON plan_phase_dependencies
BEGIN
    SELECT RAISE(ABORT, 'phase dependency definitions are immutable');
END;

CREATE TRIGGER plan_phase_dependencies_no_delete
BEFORE DELETE ON plan_phase_dependencies
BEGIN
    SELECT RAISE(ABORT, 'phase dependency definitions are immutable');
END;

CREATE TRIGGER plan_tasks_no_update
BEFORE UPDATE ON plan_tasks
BEGIN
    SELECT RAISE(ABORT, 'task definitions are immutable');
END;

CREATE TRIGGER plan_tasks_no_delete
BEFORE DELETE ON plan_tasks
BEGIN
    SELECT RAISE(ABORT, 'task definitions are immutable');
END;

CREATE TRIGGER plan_task_dependencies_no_update
BEFORE UPDATE ON plan_task_dependencies
BEGIN
    SELECT RAISE(ABORT, 'task dependency definitions are immutable');
END;

CREATE TRIGGER plan_task_dependencies_no_delete
BEFORE DELETE ON plan_task_dependencies
BEGIN
    SELECT RAISE(ABORT, 'task dependency definitions are immutable');
END;

CREATE TRIGGER plan_receipts_no_update
BEFORE UPDATE ON plan_receipts
BEGIN
    SELECT RAISE(ABORT, 'finalized plan receipts are immutable');
END;

CREATE TRIGGER plan_receipts_no_delete
BEFORE DELETE ON plan_receipts
BEGIN
    SELECT RAISE(ABORT, 'finalized plan receipts are immutable');
END;

CREATE TRIGGER plan_amendments_no_update
BEFORE UPDATE ON plan_amendments
BEGIN
    SELECT RAISE(ABORT, 'finalized plan amendments are immutable');
END;

CREATE TRIGGER plan_amendments_no_delete
BEFORE DELETE ON plan_amendments
BEGIN
    SELECT RAISE(ABORT, 'finalized plan amendments are immutable');
END;

CREATE TRIGGER plan_supersessions_no_update
BEFORE UPDATE ON plan_supersessions
BEGIN
    SELECT RAISE(ABORT, 'finalized plan supersessions are immutable');
END;

CREATE TRIGGER plan_supersessions_no_delete
BEFORE DELETE ON plan_supersessions
BEGIN
    SELECT RAISE(ABORT, 'finalized plan supersessions are immutable');
END;

CREATE TRIGGER plan_supersession_replacements_no_update
BEFORE UPDATE ON plan_supersession_replacements
BEGIN
    SELECT RAISE(ABORT, 'supersession replacements are immutable');
END;

CREATE TRIGGER plan_supersession_replacements_no_delete
BEFORE DELETE ON plan_supersession_replacements
BEGIN
    SELECT RAISE(ABORT, 'supersession replacements are immutable');
END;

CREATE TRIGGER plan_supersession_acceptance_no_update
BEFORE UPDATE ON plan_supersession_acceptance
BEGIN
    SELECT RAISE(ABORT, 'supersession acceptance mappings are immutable');
END;

CREATE TRIGGER plan_supersession_acceptance_no_delete
BEFORE DELETE ON plan_supersession_acceptance
BEGIN
    SELECT RAISE(ABORT, 'supersession acceptance mappings are immutable');
END;

CREATE TRIGGER plan_selection_proofs_no_update
BEFORE UPDATE ON plan_selection_proofs
BEGIN
    SELECT RAISE(ABORT, 'finalized selection proofs are immutable');
END;

CREATE TRIGGER plan_selection_proofs_no_delete
BEFORE DELETE ON plan_selection_proofs
BEGIN
    SELECT RAISE(ABORT, 'finalized selection proofs are immutable');
END;

CREATE TRIGGER plan_provider_intents_finalized_no_update
BEFORE UPDATE ON plan_provider_intents
WHEN OLD.finalized = 1
BEGIN
    SELECT RAISE(ABORT, 'finalized provider intents are immutable');
END;

CREATE TRIGGER plan_provider_intents_no_delete
BEFORE DELETE ON plan_provider_intents
BEGIN
    SELECT RAISE(ABORT, 'provider intents are append-only');
END;

CREATE TRIGGER plan_fingerprints_no_update
BEFORE UPDATE ON plan_fingerprints
BEGIN
    SELECT RAISE(ABORT, 'plan fingerprints are immutable');
END;

CREATE TRIGGER plan_fingerprints_no_delete
BEFORE DELETE ON plan_fingerprints
BEGIN
    SELECT RAISE(ABORT, 'plan fingerprints are immutable');
END;

CREATE TRIGGER plan_events_no_update
BEFORE UPDATE ON plan_events
BEGIN
    SELECT RAISE(ABORT, 'plan journal entries are immutable');
END;

CREATE TRIGGER plan_events_no_delete
BEFORE DELETE ON plan_events
BEGIN
    SELECT RAISE(ABORT, 'plan journal entries are immutable');
END;

CREATE TRIGGER plan_recovery_actions_no_update
BEFORE UPDATE ON plan_recovery_actions
BEGIN
    SELECT RAISE(ABORT, 'plan recovery actions are immutable');
END;

CREATE TRIGGER plan_recovery_actions_no_delete
BEFORE DELETE ON plan_recovery_actions
BEGIN
    SELECT RAISE(ABORT, 'plan recovery actions are immutable');
END;
