-- Event-history subset. Mapping inspected statically; accumulated fields are absent.
CREATE VIEW "reward" AS
SELECT tx_hash || '-' || CAST(log_index AS VARCHAR) AS id, block_timestamp AS timestamp, block_number AS block, tx_hash AS "txHash", "uplineId" AS upline, "fromUserId", pb, pc FROM ox_ai_pro__reward_booked;
