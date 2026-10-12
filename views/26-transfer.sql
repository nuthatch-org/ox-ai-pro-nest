-- Event-history subset. Mapping inspected statically; accumulated fields are absent.
CREATE VIEW "transfer" AS
SELECT tx_hash || '-' || CAST(log_index AS VARCHAR) AS id, block_timestamp AS timestamp, block_number AS block, tx_hash AS "txHash", 'park' AS kind, "fromUserId" AS "fromMember", "fromUserId", "toEmailHash", CAST(NULL AS VARCHAR) AS "toUserId", CAST(NULL AS VARCHAR) AS "toMember", amount FROM ox_ai_pro__p_b_transferred
UNION ALL SELECT tx_hash || '-' || CAST(log_index AS VARCHAR) AS id, block_timestamp AS timestamp, block_number AS block, tx_hash AS "txHash", 'send' AS kind, "fromUserId" AS "fromMember", "fromUserId", CAST(NULL AS VARCHAR) AS "toEmailHash", "toUserId", "toUserId" AS "toMember", amount FROM ox_ai_pro__p_b_sent;
