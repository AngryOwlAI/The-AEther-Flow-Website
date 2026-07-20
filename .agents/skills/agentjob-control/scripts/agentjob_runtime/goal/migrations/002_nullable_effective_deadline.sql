ALTER TABLE goals ADD COLUMN effective_deadline_at TEXT;

UPDATE goals
SET effective_deadline_at = COALESCE(
    (
        SELECT json_extract(amendment.value, '$.new_value.deadline_at')
        FROM json_each(goals.record_json, '$.amendments') AS amendment
        WHERE json_extract(amendment.value, '$.kind') = 'guards'
          AND json_type(amendment.value, '$.new_value.deadline_at') = 'text'
        ORDER BY CAST(amendment.key AS INTEGER) DESC
        LIMIT 1
    ),
    json_extract(record_json, '$.deadline_at'),
    deadline_at
);

CREATE TRIGGER goals_sync_effective_deadline_after_insert
AFTER INSERT ON goals
WHEN NEW.schema_version = 'sys4ai.continue-goal.v1'
BEGIN
    UPDATE goals
    SET effective_deadline_at = COALESCE(
        (
            SELECT json_extract(amendment.value, '$.new_value.deadline_at')
            FROM json_each(NEW.record_json, '$.amendments') AS amendment
            WHERE json_extract(amendment.value, '$.kind') = 'guards'
              AND json_type(amendment.value, '$.new_value.deadline_at') = 'text'
            ORDER BY CAST(amendment.key AS INTEGER) DESC
            LIMIT 1
        ),
        json_extract(NEW.record_json, '$.deadline_at'),
        NEW.deadline_at
    )
    WHERE goal_id = NEW.goal_id;
END;

CREATE TRIGGER goals_sync_effective_deadline_after_update
AFTER UPDATE OF record_json, deadline_at ON goals
WHEN NEW.schema_version = 'sys4ai.continue-goal.v1'
BEGIN
    UPDATE goals
    SET effective_deadline_at = COALESCE(
        (
            SELECT json_extract(amendment.value, '$.new_value.deadline_at')
            FROM json_each(NEW.record_json, '$.amendments') AS amendment
            WHERE json_extract(amendment.value, '$.kind') = 'guards'
              AND json_type(amendment.value, '$.new_value.deadline_at') = 'text'
            ORDER BY CAST(amendment.key AS INTEGER) DESC
            LIMIT 1
        ),
        json_extract(NEW.record_json, '$.deadline_at'),
        NEW.deadline_at
    )
    WHERE goal_id = NEW.goal_id;
END;
