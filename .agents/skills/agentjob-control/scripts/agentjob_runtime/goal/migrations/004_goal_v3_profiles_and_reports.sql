-- Additive v3 storage. Historical v1/v2 canonical records and migration bytes
-- remain unchanged and readable.

ALTER TABLE generations ADD COLUMN requested_reasoning_effort TEXT;
ALTER TABLE generations ADD COLUMN effective_reasoning_effort TEXT;
ALTER TABLE generations ADD COLUMN profile_evidence_json TEXT;
ALTER TABLE generations ADD COLUMN environment_mode TEXT;
ALTER TABLE generations ADD COLUMN observed_repository_topology_json TEXT;
ALTER TABLE generations ADD COLUMN resolution_disposition_json TEXT;
ALTER TABLE generations ADD COLUMN repair_strategy_id TEXT;
ALTER TABLE generations ADD COLUMN strategy_attempt INTEGER NOT NULL DEFAULT 0;
ALTER TABLE generations ADD COLUMN material_progress_dimensions_json TEXT;
ALTER TABLE generations ADD COLUMN human_necessity_report_ref TEXT;
ALTER TABLE generations ADD COLUMN completion_report_ref TEXT;

CREATE TABLE goal_activation_receipts (
    goal_id TEXT PRIMARY KEY REFERENCES goals(goal_id),
    activation_id TEXT NOT NULL UNIQUE,
    receipt_json TEXT NOT NULL CHECK (json_valid(receipt_json)),
    receipt_sha256 TEXT NOT NULL UNIQUE CHECK (length(receipt_sha256) = 64),
    accepted_at TEXT NOT NULL
);

CREATE TABLE goal_resolution_strategies (
    goal_id TEXT NOT NULL REFERENCES goals(goal_id),
    sequence INTEGER NOT NULL CHECK (sequence > 0),
    generation INTEGER NOT NULL CHECK (generation > 0),
    blocker_signature TEXT NOT NULL CHECK (length(blocker_signature) = 64),
    strategy_id TEXT,
    attempt INTEGER NOT NULL CHECK (attempt >= 0),
    disposition_json TEXT NOT NULL CHECK (json_valid(disposition_json)),
    disposition_sha256 TEXT NOT NULL CHECK (length(disposition_sha256) = 64),
    PRIMARY KEY (goal_id, sequence),
    UNIQUE (goal_id, blocker_signature, strategy_id)
);

CREATE TABLE goal_human_necessity_reports (
    goal_id TEXT PRIMARY KEY REFERENCES goals(goal_id),
    report_id TEXT NOT NULL UNIQUE,
    report_json TEXT NOT NULL CHECK (json_valid(report_json)),
    report_sha256 TEXT NOT NULL UNIQUE CHECK (length(report_sha256) = 64),
    created_at TEXT NOT NULL
);

CREATE TABLE goal_completion_reports (
    goal_id TEXT PRIMARY KEY REFERENCES goals(goal_id),
    report_id TEXT NOT NULL UNIQUE,
    report_json TEXT NOT NULL CHECK (json_valid(report_json)),
    report_sha256 TEXT NOT NULL UNIQUE CHECK (length(report_sha256) = 64),
    completed_at TEXT NOT NULL
);

CREATE TABLE repository_topology_authorizations (
    authorization_id TEXT PRIMARY KEY,
    goal_id TEXT REFERENCES goals(goal_id),
    action TEXT NOT NULL CHECK (action IN (
        'repository-branch-create',
        'repository-worktree-create',
        'repository-binding-change'
    )),
    command_id TEXT NOT NULL,
    authorization_json TEXT NOT NULL CHECK (json_valid(authorization_json)),
    authorization_sha256 TEXT NOT NULL UNIQUE CHECK (length(authorization_sha256) = 64),
    consumed INTEGER NOT NULL CHECK (consumed IN (0, 1)),
    authorized_at TEXT NOT NULL,
    consumed_at TEXT
);

CREATE TRIGGER goal_activation_receipts_no_update
BEFORE UPDATE ON goal_activation_receipts
BEGIN
    SELECT RAISE(ABORT, 'activation receipts are immutable');
END;

CREATE TRIGGER goal_activation_receipts_no_delete
BEFORE DELETE ON goal_activation_receipts
BEGIN
    SELECT RAISE(ABORT, 'activation receipts are immutable');
END;

CREATE TRIGGER goal_completion_reports_no_update
BEFORE UPDATE ON goal_completion_reports
BEGIN
    SELECT RAISE(ABORT, 'completion reports are immutable');
END;

CREATE TRIGGER goal_completion_reports_no_delete
BEFORE DELETE ON goal_completion_reports
BEGIN
    SELECT RAISE(ABORT, 'completion reports are immutable');
END;

CREATE TRIGGER goal_human_necessity_reports_no_update
BEFORE UPDATE ON goal_human_necessity_reports
BEGIN
    SELECT RAISE(ABORT, 'human-necessity reports are immutable');
END;

CREATE TRIGGER goal_human_necessity_reports_no_delete
BEFORE DELETE ON goal_human_necessity_reports
BEGIN
    SELECT RAISE(ABORT, 'human-necessity reports are immutable');
END;

CREATE TRIGGER repository_topology_authorizations_consume_once
BEFORE UPDATE ON repository_topology_authorizations
WHEN NOT (
    OLD.consumed = 0
    AND NEW.consumed = 1
    AND OLD.authorization_id = NEW.authorization_id
    AND OLD.goal_id IS NEW.goal_id
    AND OLD.action = NEW.action
    AND OLD.command_id = NEW.command_id
    AND OLD.authorized_at = NEW.authorized_at
    AND OLD.consumed_at IS NULL
    AND NEW.consumed_at IS NOT NULL
    AND json_extract(OLD.authorization_json, '$.consumed') = 0
    AND json_extract(NEW.authorization_json, '$.consumed') = 1
)
BEGIN
    SELECT RAISE(ABORT, 'topology authorization may only be consumed once');
END;

CREATE TRIGGER repository_topology_authorizations_no_delete
BEFORE DELETE ON repository_topology_authorizations
BEGIN
    SELECT RAISE(ABORT, 'topology authorization receipts are append-only');
END;
