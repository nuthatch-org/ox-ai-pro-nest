-- Event-history subset. Mapping inspected statically; accumulated fields are absent.
CREATE VIEW "month_snapshot_entity" AS
SELECT "monthId" AS id, "monthId", "rddDistributed", "rddCount", "ldDistributed", "ldCount", block_timestamp AS timestamp FROM ox_ai_pro__month_snapshot;
