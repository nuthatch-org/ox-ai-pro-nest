-- Event-history subset. Mapping inspected statically; accumulated fields are absent.
CREATE VIEW "subscription_event" AS
SELECT tx_hash || '-' || CAST(log_index AS VARCHAR) AS id, block_timestamp AS timestamp, block_number AS block, tx_hash AS "txHash", "userId" AS member, "usdValue" AS amount, CAST(currency AS INTEGER) AS currency, CAST("firstSub" AS BOOLEAN) AS "firstSub", "sponsorId" FROM ox_ai_pro__subscribed;
