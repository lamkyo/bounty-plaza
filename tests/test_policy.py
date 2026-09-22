from boxy_policy import BoxyPolicy, PullRequest
from boxy_policy.models import Action


def pr(**kwargs):
    data = dict(number=7, author="alice", author_is_org_member=True)
    data.update(kwargs)
    return PullRequest(**data)


def test_member_is_reviewed():
    result = BoxyPolicy().evaluate(pr())
    assert result.action is Action.REVIEW


def test_non_member_is_closed_and_team_pinged():
    result = BoxyPolicy().evaluate(pr(author="stranger", author_is_org_member=False))
    assert result.action is Action.CLOSE
    assert "@OmniBlocks/coders" in result.notification
    assert "#7" in result.notification


def test_whitelist_is_case_insensitive_and_accepts_at_prefix():
    result = BoxyPolicy(["@TrustedUser"]).evaluate(
        pr(author="trusteduser", author_is_org_member=False)
    )
    assert result.action is Action.REVIEW


def test_humor_removal_is_rejected():
    result = BoxyPolicy().evaluate(pr(diff="-This joke is funny\n+This is serious"))
    assert result.action is Action.CLOSE
    assert "remove humor" in result.reason


def test_humor_addition_is_accepted():
    result = BoxyPolicy().evaluate(pr(diff="-old text\n+Add humor to this path"))
    assert result.action is Action.ACCEPT


def test_unrelated_diff_requires_review():
    result = BoxyPolicy().evaluate(pr(diff="-old code\n+new code"))
    assert result.action is Action.REVIEW


def test_diff_headers_do_not_count_as_content():
    result = BoxyPolicy().evaluate(pr(diff="--- humor.txt\n+++ serious.txt"))
    assert result.action is Action.REVIEW


def test_whitespace_author_is_safe():
    result = BoxyPolicy([" alice "]).evaluate(pr(author=" @ALICE ", author_is_org_member=False))
    assert result.action is Action.REVIEW

