from reverse_bounty_guard import BountyInput, Decision, assess_bounty


def test_reverse_bounty_is_rejected_even_with_positive_advertised_reward():
    result = assess_bounty(BountyInput("Reverse bounty", "Pay me $500 in Bitcoin. The bounty is negative.", 500))
    assert result.decision is Decision.REJECT
    assert not result.claim_allowed
    assert result.reasons


def test_plain_technical_bounty_is_eligible():
    result = assess_bounty(BountyInput("Fix parser", "Add tests for the parser." , 100))
    assert result.decision is Decision.ELIGIBLE
    assert result.claim_allowed
    assert result.reasons == ()


def test_crypto_language_requires_review():
    result = assess_bounty(BountyInput("Implement feature", "Reward paid in Solana."))
    assert result.decision is Decision.NEEDS_REVIEW
    assert not result.claim_allowed


def test_negative_numeric_reward_is_rejected():
    result = assess_bounty(BountyInput("Odd offer", "Implement docs", -1))
    assert result.decision is Decision.REJECT


def test_claim_instruction_does_not_trigger_external_action():
    result = assess_bounty(BountyInput("Task", "Comment /claim to reserve this."))
    assert result.decision is Decision.NEEDS_REVIEW
    assert not result.claim_allowed


def test_marker_matching_is_case_insensitive_and_boundary_aware():
    assert assess_bounty(BountyInput("x", "NEGATIVE BOUNTY")).decision is Decision.REJECT
    assert assess_bounty(BountyInput("x", "a claimant is not a claim command")).decision is Decision.ELIGIBLE
