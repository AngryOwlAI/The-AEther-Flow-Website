-- Additive continuous implementation-plan coordinator storage. Historical
-- activation, plan, task, and provider records remain byte-preserved.

CREATE TABLE plan_question_batches (
    batch_id TEXT PRIMARY KEY,
    plan_id TEXT NOT NULL REFERENCES plans(plan_id),
    batch_json TEXT NOT NULL CHECK (json_valid(batch_json)),
    batch_sha256 TEXT NOT NULL UNIQUE CHECK (length(batch_sha256) = 64),
    created_at TEXT NOT NULL
);

CREATE TABLE plan_execution_authorities (
    authority_id TEXT PRIMARY KEY,
    plan_id TEXT NOT NULL REFERENCES plans(plan_id),
    authority_json TEXT NOT NULL CHECK (json_valid(authority_json)),
    authority_sha256 TEXT NOT NULL UNIQUE CHECK (length(authority_sha256) = 64),
    created_at TEXT NOT NULL
);

CREATE TABLE plan_question_responses (
    response_id TEXT PRIMARY KEY,
    plan_id TEXT NOT NULL REFERENCES plans(plan_id),
    batch_id TEXT NOT NULL REFERENCES plan_question_batches(batch_id),
    response_json TEXT NOT NULL CHECK (json_valid(response_json)),
    response_sha256 TEXT NOT NULL UNIQUE CHECK (length(response_sha256) = 64),
    answered_at TEXT NOT NULL
);

CREATE TABLE plan_continuous_states (
    plan_id TEXT PRIMARY KEY REFERENCES plans(plan_id),
    state_revision INTEGER NOT NULL CHECK (state_revision > 0),
    status TEXT NOT NULL CHECK (
        status IN (
            'active',
            'worker_active',
            'awaiting_user_input',
            'suspended_safeguard',
            'goal_reached',
            'cancelled'
        )
    ),
    state_json TEXT NOT NULL CHECK (json_valid(state_json)),
    updated_at TEXT NOT NULL
);

CREATE TABLE plan_coordinator_wakeups (
    wakeup_id TEXT PRIMARY KEY,
    plan_id TEXT NOT NULL REFERENCES plans(plan_id),
    generation INTEGER NOT NULL CHECK (generation > 0),
    worker_thread_id TEXT NOT NULL,
    coordinator_thread_id TEXT NOT NULL,
    task_receipt_sha256 TEXT NOT NULL CHECK (length(task_receipt_sha256) = 64),
    idempotency_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL CHECK (status IN ('pending', 'delivered', 'ambiguous')),
    record_json TEXT NOT NULL CHECK (json_valid(record_json)),
    record_sha256 TEXT NOT NULL CHECK (length(record_sha256) = 64),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    UNIQUE (plan_id, generation, task_receipt_sha256)
);

CREATE TABLE plan_completion_reports (
    plan_id TEXT PRIMARY KEY REFERENCES plans(plan_id),
    report_json TEXT NOT NULL CHECK (json_valid(report_json)),
    report_sha256 TEXT NOT NULL UNIQUE CHECK (length(report_sha256) = 64),
    completed_at TEXT NOT NULL
);

CREATE INDEX plan_question_batches_by_plan
ON plan_question_batches(plan_id, created_at, batch_id);

CREATE INDEX plan_question_responses_by_plan
ON plan_question_responses(plan_id, answered_at, response_id);

CREATE INDEX plan_coordinator_wakeups_by_plan
ON plan_coordinator_wakeups(plan_id, generation, wakeup_id);

CREATE TRIGGER plan_question_batches_no_update
BEFORE UPDATE ON plan_question_batches
BEGIN
    SELECT RAISE(ABORT, 'plan question batches are immutable');
END;

CREATE TRIGGER plan_question_batches_no_delete
BEFORE DELETE ON plan_question_batches
BEGIN
    SELECT RAISE(ABORT, 'plan question batches are immutable');
END;

CREATE TRIGGER plan_execution_authorities_no_update
BEFORE UPDATE ON plan_execution_authorities
BEGIN
    SELECT RAISE(ABORT, 'plan execution authorities are immutable');
END;

CREATE TRIGGER plan_execution_authorities_no_delete
BEFORE DELETE ON plan_execution_authorities
BEGIN
    SELECT RAISE(ABORT, 'plan execution authorities are immutable');
END;

CREATE TRIGGER plan_question_responses_no_update
BEFORE UPDATE ON plan_question_responses
BEGIN
    SELECT RAISE(ABORT, 'plan question responses are immutable');
END;

CREATE TRIGGER plan_question_responses_no_delete
BEFORE DELETE ON plan_question_responses
BEGIN
    SELECT RAISE(ABORT, 'plan question responses are immutable');
END;

CREATE TRIGGER plan_completion_reports_no_update
BEFORE UPDATE ON plan_completion_reports
BEGIN
    SELECT RAISE(ABORT, 'plan completion reports are immutable');
END;

CREATE TRIGGER plan_completion_reports_no_delete
BEFORE DELETE ON plan_completion_reports
BEGIN
    SELECT RAISE(ABORT, 'plan completion reports are immutable');
END;

CREATE TRIGGER plan_coordinator_wakeups_identity_immutable
BEFORE UPDATE ON plan_coordinator_wakeups
WHEN
    NEW.wakeup_id IS NOT OLD.wakeup_id
    OR NEW.plan_id IS NOT OLD.plan_id
    OR NEW.generation IS NOT OLD.generation
    OR NEW.worker_thread_id IS NOT OLD.worker_thread_id
    OR NEW.coordinator_thread_id IS NOT OLD.coordinator_thread_id
    OR NEW.task_receipt_sha256 IS NOT OLD.task_receipt_sha256
    OR NEW.idempotency_key IS NOT OLD.idempotency_key
    OR NEW.created_at IS NOT OLD.created_at
BEGIN
    SELECT RAISE(ABORT, 'plan coordinator wakeup identity is immutable');
END;
