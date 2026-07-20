-- Additive implementation-plan execution-profile storage. Historical goal and
-- plan records remain readable; existing migrations are not rewritten.

ALTER TABLE plans ADD COLUMN runtime_profile_version INTEGER NOT NULL DEFAULT 1
    CHECK (runtime_profile_version IN (1, 2));
ALTER TABLE plans ADD COLUMN activation_sequence INTEGER NOT NULL DEFAULT 0
    CHECK (activation_sequence >= 0);
ALTER TABLE plans ADD COLUMN activation_receipt_sha256 TEXT
    CHECK (
        activation_receipt_sha256 IS NULL
        OR length(activation_receipt_sha256) = 64
    );
ALTER TABLE plans ADD COLUMN execution_profile_json TEXT
    CHECK (
        execution_profile_json IS NULL
        OR json_valid(execution_profile_json)
    );
ALTER TABLE plans ADD COLUMN topology_policy_json TEXT
    CHECK (
        topology_policy_json IS NULL
        OR json_valid(topology_policy_json)
    );
ALTER TABLE plans ADD COLUMN activation_goal_text TEXT;
ALTER TABLE plans ADD COLUMN activation_goal_sha256 TEXT
    CHECK (
        activation_goal_sha256 IS NULL
        OR length(activation_goal_sha256) = 64
    );
ALTER TABLE plans ADD COLUMN profile_effective_from_generation INTEGER
    CHECK (
        profile_effective_from_generation IS NULL
        OR profile_effective_from_generation > 0
    );
ALTER TABLE plans ADD COLUMN repository_binding_sha256 TEXT
    CHECK (
        repository_binding_sha256 IS NULL
        OR length(repository_binding_sha256) = 64
    );

CREATE TABLE plan_activation_receipts (
    activation_id TEXT PRIMARY KEY,
    plan_id TEXT NOT NULL REFERENCES plans(plan_id),
    activation_sequence INTEGER NOT NULL CHECK (activation_sequence > 0),
    receipt_json TEXT NOT NULL CHECK (json_valid(receipt_json)),
    receipt_sha256 TEXT NOT NULL UNIQUE CHECK (length(receipt_sha256) = 64),
    effective_from_generation INTEGER NOT NULL
        CHECK (effective_from_generation > 0),
    superseded_activation_id TEXT,
    accepted_at TEXT NOT NULL,
    UNIQUE (plan_id, activation_sequence),
    FOREIGN KEY (superseded_activation_id)
        REFERENCES plan_activation_receipts(activation_id),
    CHECK (
        (activation_sequence = 1 AND superseded_activation_id IS NULL)
        OR
        (activation_sequence > 1 AND superseded_activation_id IS NOT NULL)
    )
);

ALTER TABLE plan_provider_intents
    ADD COLUMN execution_profile_sha256 TEXT
    CHECK (
        execution_profile_sha256 IS NULL
        OR length(execution_profile_sha256) = 64
    );
ALTER TABLE plan_provider_intents
    ADD COLUMN requested_reasoning_effort TEXT;
ALTER TABLE plan_provider_intents
    ADD COLUMN effective_reasoning_effort TEXT;
ALTER TABLE plan_provider_intents
    ADD COLUMN profile_verification_status TEXT
    CHECK (
        profile_verification_status IS NULL
        OR profile_verification_status IN (
            'not_verified', 'pending', 'verified', 'mismatch', 'unavailable'
        )
    );
ALTER TABLE plan_provider_intents
    ADD COLUMN profile_evidence_ref TEXT;
ALTER TABLE plan_provider_intents
    ADD COLUMN environment_mode TEXT
    CHECK (
        environment_mode IS NULL
        OR environment_mode = 'reuse_bound_checkout'
    );
ALTER TABLE plan_provider_intents
    ADD COLUMN repository_binding_sha256 TEXT
    CHECK (
        repository_binding_sha256 IS NULL
        OR length(repository_binding_sha256) = 64
    );
ALTER TABLE plan_provider_intents
    ADD COLUMN observed_topology_sha256 TEXT
    CHECK (
        observed_topology_sha256 IS NULL
        OR length(observed_topology_sha256) = 64
    );
ALTER TABLE plan_provider_intents
    ADD COLUMN same_thread_profile_repair_json TEXT
    CHECK (
        same_thread_profile_repair_json IS NULL
        OR json_valid(same_thread_profile_repair_json)
    );

CREATE TRIGGER plan_activation_receipts_no_update
BEFORE UPDATE ON plan_activation_receipts
BEGIN
    SELECT RAISE(ABORT, 'plan activation receipts are immutable');
END;

CREATE TRIGGER plan_activation_receipts_no_delete
BEFORE DELETE ON plan_activation_receipts
BEGIN
    SELECT RAISE(ABORT, 'plan activation receipts are immutable');
END;

CREATE TRIGGER plans_profile_v2_insert_complete
BEFORE INSERT ON plans
WHEN NEW.runtime_profile_version = 2
     AND (
        NEW.activation_sequence < 1
        OR NEW.activation_receipt_sha256 IS NULL
        OR NEW.execution_profile_json IS NULL
        OR NEW.topology_policy_json IS NULL
        OR NEW.activation_goal_text IS NULL
        OR length(trim(NEW.activation_goal_text)) = 0
        OR NEW.activation_goal_sha256 IS NULL
        OR NEW.profile_effective_from_generation IS NULL
        OR NEW.repository_binding_sha256 IS NULL
        OR json_extract(
            NEW.execution_profile_json,
            '$.current_thread_verification_status'
        ) <> 'verified'
        OR json_extract(
            NEW.execution_profile_json,
            '$.successor_inheritance_required'
        ) <> 1
        OR json_extract(
            NEW.execution_profile_json,
            '$.effective_from_generation'
        ) <> NEW.profile_effective_from_generation
        OR json_extract(
            NEW.execution_profile_json,
            '$.repository_binding_sha256'
        ) <> NEW.repository_binding_sha256
        OR json_extract(
            NEW.topology_policy_json,
            '$.environment_mode'
        ) <> 'reuse_bound_checkout'
     )
BEGIN
    SELECT RAISE(ABORT, 'runtime-profile v2 plan row is incomplete');
END;

CREATE TRIGGER plans_profile_v1_insert_null
BEFORE INSERT ON plans
WHEN NEW.runtime_profile_version = 1
     AND (
        NEW.activation_sequence <> 0
        OR NEW.activation_receipt_sha256 IS NOT NULL
        OR NEW.execution_profile_json IS NOT NULL
        OR NEW.topology_policy_json IS NOT NULL
        OR NEW.activation_goal_text IS NOT NULL
        OR NEW.activation_goal_sha256 IS NOT NULL
        OR NEW.profile_effective_from_generation IS NOT NULL
        OR NEW.repository_binding_sha256 IS NOT NULL
     )
BEGIN
    SELECT RAISE(ABORT, 'legacy runtime-profile v1 fields must remain null');
END;

CREATE TRIGGER plans_profile_update_requires_receipt
BEFORE UPDATE OF
    runtime_profile_version,
    activation_sequence,
    activation_receipt_sha256,
    execution_profile_json,
    topology_policy_json,
    activation_goal_text,
    activation_goal_sha256,
    profile_effective_from_generation,
    repository_binding_sha256
ON plans
WHEN
    NEW.runtime_profile_version <> OLD.runtime_profile_version
    OR NEW.activation_sequence <> OLD.activation_sequence
    OR NEW.activation_receipt_sha256 IS NOT OLD.activation_receipt_sha256
    OR NEW.execution_profile_json IS NOT OLD.execution_profile_json
    OR NEW.topology_policy_json IS NOT OLD.topology_policy_json
    OR NEW.activation_goal_text IS NOT OLD.activation_goal_text
    OR NEW.activation_goal_sha256 IS NOT OLD.activation_goal_sha256
    OR NEW.profile_effective_from_generation
       IS NOT OLD.profile_effective_from_generation
    OR NEW.repository_binding_sha256 IS NOT OLD.repository_binding_sha256
BEGIN
    SELECT CASE
        WHEN NEW.runtime_profile_version <> 2
          OR NEW.activation_sequence <> OLD.activation_sequence + 1
          OR NEW.activation_receipt_sha256 IS NULL
          OR NEW.execution_profile_json IS NULL
          OR NEW.topology_policy_json IS NULL
          OR NEW.activation_goal_text IS NULL
          OR length(trim(NEW.activation_goal_text)) = 0
          OR NEW.activation_goal_sha256 IS NULL
          OR NEW.profile_effective_from_generation
             <> OLD.current_generation + 1
          OR NEW.repository_binding_sha256 IS NULL
          OR json_extract(
              NEW.execution_profile_json,
              '$.current_thread_verification_status'
          ) <> 'verified'
          OR json_extract(
              NEW.execution_profile_json,
              '$.successor_inheritance_required'
          ) <> 1
          OR json_extract(
              NEW.execution_profile_json,
              '$.effective_from_generation'
          ) <> NEW.profile_effective_from_generation
          OR json_extract(
              NEW.execution_profile_json,
              '$.repository_binding_sha256'
          ) <> NEW.repository_binding_sha256
          OR json_extract(
              NEW.topology_policy_json,
              '$.environment_mode'
          ) <> 'reuse_bound_checkout'
          OR NOT EXISTS (
              SELECT 1
              FROM plan_activation_receipts AS receipt
              WHERE receipt.plan_id = NEW.plan_id
                AND receipt.activation_sequence = NEW.activation_sequence
                AND receipt.receipt_sha256 =
                    NEW.activation_receipt_sha256
                AND receipt.effective_from_generation =
                    NEW.profile_effective_from_generation
                AND (
                    (
                        OLD.activation_sequence = 0
                        AND receipt.superseded_activation_id IS NULL
                    )
                    OR
                    (
                        OLD.activation_sequence > 0
                        AND receipt.superseded_activation_id =
                            json_extract(
                                OLD.execution_profile_json,
                                '$.activation_id'
                            )
                    )
                )
          )
        THEN RAISE(
            ABORT,
            'plan profile change requires one matching superseding receipt'
        )
    END;
END;

CREATE TRIGGER plan_provider_intents_v2_insert_complete
BEFORE INSERT ON plan_provider_intents
WHEN json_extract(NEW.record_json, '$.schema_version')
     = 'sys4ai.plan-provider-intent.v2'
     AND (
        NEW.execution_profile_sha256 IS NULL
        OR NEW.requested_reasoning_effort IS NULL
        OR NEW.profile_verification_status IS NULL
        OR NEW.environment_mode <> 'reuse_bound_checkout'
        OR NEW.repository_binding_sha256 IS NULL
     )
BEGIN
    SELECT RAISE(ABORT, 'provider intent v2 profile projection is incomplete');
END;

CREATE TRIGGER plan_provider_intents_v2_returned_insert_verified
BEFORE INSERT ON plan_provider_intents
WHEN json_extract(NEW.record_json, '$.schema_version')
     = 'sys4ai.plan-provider-intent.v2'
     AND NEW.status = 'returned'
     AND NEW.finalized = 1
     AND (
        NEW.requested_reasoning_effort
            IS NOT NEW.effective_reasoning_effort
        OR NEW.profile_verification_status <> 'verified'
        OR NEW.profile_evidence_ref IS NULL
        OR length(trim(NEW.profile_evidence_ref)) = 0
        OR NEW.observed_topology_sha256 IS NULL
     )
BEGIN
    SELECT RAISE(
        ABORT,
        'returned provider intent v2 lacks verified profile evidence'
    );
END;

CREATE TRIGGER plan_provider_intents_v2_returned_update_verified
BEFORE UPDATE ON plan_provider_intents
WHEN json_extract(NEW.record_json, '$.schema_version')
     = 'sys4ai.plan-provider-intent.v2'
     AND NEW.status = 'returned'
     AND NEW.finalized = 1
     AND (
        NEW.requested_reasoning_effort
            IS NOT NEW.effective_reasoning_effort
        OR NEW.profile_verification_status <> 'verified'
        OR NEW.profile_evidence_ref IS NULL
        OR length(trim(NEW.profile_evidence_ref)) = 0
        OR NEW.environment_mode <> 'reuse_bound_checkout'
        OR NEW.repository_binding_sha256 IS NULL
        OR NEW.observed_topology_sha256 IS NULL
     )
BEGIN
    SELECT RAISE(
        ABORT,
        'returned provider intent v2 lacks verified profile evidence'
    );
END;

CREATE INDEX plan_activation_receipts_history
ON plan_activation_receipts(
    plan_id,
    effective_from_generation,
    activation_sequence
);
