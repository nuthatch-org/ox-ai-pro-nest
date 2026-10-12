-- Event-history subset. Mapping inspected statically; accumulated fields are absent.
CREATE VIEW "member" AS
SELECT "userId" AS id FROM ox_ai_pro__member_registered
UNION
SELECT "sponsorId" AS id FROM ox_ai_pro__member_registered WHERE "sponsorId" <> '0'
UNION
SELECT "userId" AS id FROM ox_ai_pro__subscribed
UNION
SELECT "sponsorId" AS id FROM ox_ai_pro__subscribed WHERE "sponsorId" <> '0'
UNION
SELECT "uplineId" AS id FROM ox_ai_pro__reward_booked
UNION
SELECT "userId" AS id FROM ox_ai_pro__parked_p_b_claimed
UNION
SELECT "userId" AS id FROM ox_ai_pro__rank_up
UNION
SELECT "userId" AS id FROM ox_ai_pro__campaign_reward
UNION
SELECT "userId" AS id FROM ox_ai_pro__director_locked
UNION
SELECT "userId" AS id FROM ox_ai_pro__director_eligibility_set
UNION
SELECT "userId" AS id FROM ox_ai_pro__director_claimed
UNION
SELECT "fromUserId" AS id FROM ox_ai_pro__p_b_transferred
UNION
SELECT "fromUserId" AS id FROM ox_ai_pro__p_b_sent
UNION
SELECT "toUserId" AS id FROM ox_ai_pro__p_b_sent
UNION
SELECT "userId" AS id FROM ox_ai_pro__withdraw_p_b
UNION
SELECT "userId" AS id FROM ox_ai_pro__withdraw_p_b_as
UNION
SELECT "userId" AS id FROM ox_ai_pro__withdraw_p_c
UNION
SELECT "userId" AS id FROM ox_ai_pro__origin_initialized
UNION
SELECT '115792089237316195423570985008687907853269984665640564039457584007913129639935' AS id FROM ox_ai_pro__rdd_overflow_to_creator;
