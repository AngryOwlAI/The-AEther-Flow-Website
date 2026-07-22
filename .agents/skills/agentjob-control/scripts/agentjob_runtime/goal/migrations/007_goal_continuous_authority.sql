-- Additive generic v4 intake, authority, one-shot grant, and coordinator state.
-- Historical v1-v3 goal records and v1-v2 receipts remain byte-preserved.

CREATE TABLE goal_question_batches (
    batch_id TEXT PRIMARY KEY,
    goal_id TEXT NOT NULL REFERENCES goals(goal_id),
    batch_json TEXT NOT NULL CHECK (json_valid(batch_json)),
    batch_sha256 TEXT NOT NULL UNIQUE CHECK (length(batch_sha256) = 64),
    created_at TEXT NOT NULL
);

CREATE TABLE goal_execution_authorities (
    authority_id TEXT PRIMARY KEY,
    goal_id TEXT NOT NULL REFERENCES goals(goal_id),
    authority_json TEXT NOT NULL CHECK (json_valid(authority_json)),
    authority_sha256 TEXT NOT NULL UNIQUE CHECK (length(authority_sha256) = 64),
    created_at TEXT NOT NULL
);

CREATE TABLE goal_question_responses (
    response_id TEXT PRIMARY KEY,
    goal_id TEXT NOT NULL REFERENCES goals(goal_id),
    batch_id TEXT NOT NULL REFERENCES goal_question_batches(batch_id),
    response_json TEXT NOT NULL CHECK (json_valid(response_json)),
    response_sha256 TEXT NOT NULL UNIQUE CHECK (length(response_sha256) = 64),
    answered_at TEXT NOT NULL
);

CREATE TABLE goal_grant_consumptions (
    consumption_id TEXT PRIMARY KEY,
    goal_id TEXT NOT NULL REFERENCES goals(goal_id),
    generation INTEGER NOT NULL CHECK (generation >= 0),
    grant_id TEXT NOT NULL,
    action_sha256 TEXT NOT NULL CHECK (length(action_sha256) = 64),
    consumption_json TEXT NOT NULL CHECK (json_valid(consumption_json)),
    consumption_sha256 TEXT NOT NULL UNIQUE CHECK (length(consumption_sha256) = 64),
    consumed_at TEXT NOT NULL,
    UNIQUE (goal_id, grant_id)
);

CREATE TABLE goal_coordinator_states (
    goal_id TEXT PRIMARY KEY REFERENCES goals(goal_id),
    coordinator_thread_id TEXT NOT NULL,
    status TEXT NOT NULL CHECK (
        status IN (
            'active',
            'worker_active',
            'suspended_safeguard',
            'goal_reached',
            'cancelled'
        )
    ),
    state_json TEXT NOT NULL CHECK (json_valid(state_json)),
    updated_at TEXT NOT NULL
);

CREATE INDEX goal_question_batches_by_goal
ON goal_question_batches(goal_id, created_at, batch_id);

CREATE INDEX goal_question_responses_by_goal
ON goal_question_responses(goal_id, answered_at, response_id);

CREATE INDEX goal_grant_consumptions_by_goal
ON goal_grant_consumptions(goal_id, generation, grant_id);

CREATE TRIGGER goal_question_batches_no_update
BEFORE UPDATE ON goal_question_batches
BEGIN
    SELECT RAISE(ABORT, 'goal question batches are immutable');
END;

CREATE TRIGGER goal_question_batches_no_delete
BEFORE DELETE ON goal_question_batches
BEGIN
    SELECT RAISE(ABORT, 'goal question batches are immutable');
END;

CREATE TRIGGER goal_execution_authorities_no_update
BEFORE UPDATE ON goal_execution_authorities
BEGIN
    SELECT RAISE(ABORT, 'goal execution authorities are immutable');
END;

CREATE TRIGGER goal_execution_authorities_no_delete
BEFORE DELETE ON goal_execution_authorities
BEGIN
    SELECT RAISE(ABORT, 'goal execution authorities are immutable');
END;

CREATE TRIGGER goal_question_responses_no_update
BEFORE UPDATE ON goal_question_responses
BEGIN
    SELECT RAISE(ABORT, 'goal question responses are immutable');
END;

CREATE TRIGGER goal_question_responses_no_delete
BEFORE DELETE ON goal_question_responses
BEGIN
    SELECT RAISE(ABORT, 'goal question responses are immutable');
END;

CREATE TRIGGER goal_grant_consumptions_no_update
BEFORE UPDATE ON goal_grant_consumptions
BEGIN
    SELECT RAISE(ABORT, 'goal grant consumptions are immutable');
END;

CREATE TRIGGER goal_grant_consumptions_no_delete
BEFORE DELETE ON goal_grant_consumptions
BEGIN
    SELECT RAISE(ABORT, 'goal grant consumptions are immutable');
END;
