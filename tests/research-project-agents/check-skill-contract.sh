#!/bin/sh
# Assert the research-project-agents skill text and expected-section contract.
#
# A live agent run against tests/fixtures/orient-sample/ is manual. This script
# does not invoke an agent. It checks SKILL.md, expected-sections.txt, and that
# the fixture has evidence for Structure / Purpose / Where to look plus merge
# and skip cases.
#
# Naming ## Domain / ## Self-Improvement Loop for each project in SKILL.md is
# allowed when those strings are forbidden generated headings (drop / do not
# emit). They must still be listed under [forbidden] in expected-sections.txt.
#
# Usage (from anywhere):
#   tests/research-project-agents/check-skill-contract.sh

set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
repo_root=$(CDPATH= cd -- "$script_dir/../.." && pwd)
skill=$repo_root/.agents/skills/research-project-agents/SKILL.md
expected=$script_dir/expected-sections.txt
fixture=$repo_root/tests/fixtures/orient-sample

failures=0

fail() {
	printf '%s\n' "FAIL: $*" >&2
	failures=$((failures + 1))
}

ok() {
	printf '%s\n' "ok: $*"
}

contains() {
	grep -Fq -- "$1" "$2"
}

contains_re() {
	grep -Eq -- "$1" "$2"
}

require_file() {
	if [ -f "$1" ]; then
		ok "file exists: $1"
	else
		fail "missing file: $1"
	fi
}

require_text() {
	if contains "$1" "$2"; then
		ok "$3"
	else
		fail "$3 (missing: $1)"
	fi
}

require_re() {
	if contains_re "$1" "$2"; then
		ok "$3"
	else
		fail "$3 (missing /$1/)"
	fi
}

forbid_re() {
	if contains_re "$1" "$2"; then
		fail "$3 (still matches /$1/)"
	else
		ok "$3"
	fi
}

forbid_text() {
	if contains "$1" "$2"; then
		fail "$3 (still contains: $1)"
	else
		ok "$3"
	fi
}

check_expected_sections() {
	require_file "$expected"
	[ -f "$expected" ] || return 0

	require_text "[required]" "$expected" "expected-sections.txt has [required]"
	require_text "[forbidden]" "$expected" "expected-sections.txt has [forbidden]"

	# Locked required / forbidden headings. Do not weaken this list to go green.
	# Title marker is a bare "#" line under [required].
	section=
	saw_title=0
	saw_structure=0
	saw_purpose=0
	saw_where=0
	saw_domain=0
	saw_loop=0

	while IFS= read -r line || [ -n "$line" ]; do
		case $line in
		"[required]")
			section=required
			continue
			;;
		"[forbidden]")
			section=forbidden
			continue
			;;
		"# "* | "")
			continue
			;;
		esac

		if [ "$section" = required ]; then
			case $line in
			"#") saw_title=1 ;;
			"## Structure") saw_structure=1 ;;
			"## Purpose") saw_purpose=1 ;;
			"## Where to look") saw_where=1 ;;
			*) fail "expected-sections.txt [required] has unexpected line: $line" ;;
			esac
		elif [ "$section" = forbidden ]; then
			case $line in
			"## Domain") saw_domain=1 ;;
			"## Self-Improvement Loop for each project") saw_loop=1 ;;
			*) fail "expected-sections.txt [forbidden] has unexpected line: $line" ;;
			esac
		fi
	done <"$expected"

	if [ "$saw_title" -eq 1 ]; then
		ok "expected-sections.txt requires # title"
	else
		fail "expected-sections.txt missing required # title"
	fi
	if [ "$saw_structure" -eq 1 ]; then
		ok "expected-sections.txt requires ## Structure"
	else
		fail "expected-sections.txt missing required ## Structure"
	fi
	if [ "$saw_purpose" -eq 1 ]; then
		ok "expected-sections.txt requires ## Purpose"
	else
		fail "expected-sections.txt missing required ## Purpose"
	fi
	if [ "$saw_where" -eq 1 ]; then
		ok "expected-sections.txt requires ## Where to look"
	else
		fail "expected-sections.txt missing required ## Where to look"
	fi
	if [ "$saw_domain" -eq 1 ]; then
		ok "expected-sections.txt forbids ## Domain"
	else
		fail "expected-sections.txt missing forbidden ## Domain"
	fi
	if [ "$saw_loop" -eq 1 ]; then
		ok "expected-sections.txt forbids ## Self-Improvement Loop for each project"
	else
		fail "expected-sections.txt missing forbidden ## Self-Improvement Loop for each project"
	fi
}

check_fixture() {
	require_file "$fixture/README.md"
	require_file "$fixture/src/app.py"
	require_file "$fixture/node_modules/pkg/index.js"
	require_file "$fixture/package-lock.json"
	require_file "$fixture/AGENTS.md"

	[ -f "$fixture/AGENTS.md" ] || return 0

	require_text "Keep:" "$fixture/AGENTS.md" \
		"fixture AGENTS.md has a keepable sentence"
	if contains "## Domain" "$fixture/AGENTS.md" ||
		contains "## Self-Improvement Loop for each project" "$fixture/AGENTS.md"; then
		ok "fixture AGENTS.md has old Domain or Self-Improvement Loop block"
	else
		fail "fixture AGENTS.md missing old Domain or Self-Improvement Loop block"
	fi
}

check_happy_path() {
	require_file "$skill"
	[ -f "$skill" ] || return 0

	require_re "user must name the target directory|must name the target" "$skill" \
		"skill requires a user-named target"
	require_re "Ask and stop if it is missing|Ask if missing" "$skill" \
		"skill asks and stops when the target is missing"
	require_text "Do not default to this harness" "$skill" \
		"skill does not default to this harness"
	require_re "AGENTS.md (in that same directory|at the user-named directory)" "$skill" \
		"skill writes AGENTS.md at the named directory"
	require_text "Prefer merge over wipe" "$skill" \
		"skill prefers merge over wipe"
	require_re "Skip vendored, generated, and lockfile" "$skill" \
		"skill skips vendored, generated, and lockfile noise"
	require_re "sub-agents to explore|spawn sub-agents" "$skill" \
		"skill uses sub-agents to explore"
	require_re "[Ss]ub-agents must not .*write AGENTS.md|not let a sub-agent write AGENTS.md" "$skill" \
		"skill: sub-agents explore only (must not write AGENTS.md)"
	require_text "## Structure" "$skill" \
		"skill text includes required heading ## Structure"
	require_text "## Purpose" "$skill" \
		"skill text includes required heading ## Purpose"
	require_text "## Where to look" "$skill" \
		"skill text includes required heading ## Where to look"
	require_text "# <name>" "$skill" \
		"skill text includes required # title pattern"
}

check_edges() {
	[ -f "$skill" ] || return 0

	# Domain walk-up procedure (old machinery). Prohibitions such as
	# "Do not walk up" or "Drop leftover Domain walk-up" are not the procedure.
	forbid_re "^## Domain AGENTS\\.md" "$skill" \
		"skill has no Domain AGENTS.md walk-up section"
	forbid_re "^Walk-up:" "$skill" \
		"skill has no Walk-up procedure"
	forbid_text "Walk toward filesystem root" "$skill" \
		"skill does not walk toward filesystem root"
	forbid_text "Locate the domain AGENTS.md" "$skill" \
		"skill does not locate a domain AGENTS.md"
	forbid_text "first ancestor that contains" "$skill" \
		"skill does not walk ancestors for domain AGENTS.md"
	forbid_text "This is a **project** AGENTS.md" "$skill" \
		"skill does not emit the old Domain snippet"

	# Verbatim lessons.md loop body (the heading may be named as forbidden output).
	forbid_text "After ANY correction from the user: update 'lessons.md'" "$skill" \
		"skill does not contain the verbatim lessons.md loop"

	# TCODE / tcode-ai-harness as default or named target.
	forbid_re "(^|[^A-Za-z0-9_-])TCODE([^A-Za-z0-9_-]|$)" "$skill" \
		"skill does not name TCODE as a target"
	forbid_text "tcode-ai-harness" "$skill" \
		"skill does not name tcode-ai-harness as a target"

	# Windows path examples (the prohibition line is allowed).
	forbid_re "[A-Za-z]:\\\\|[A-Za-z]:/[^/]|\\\\Users\\\\|\\\\Program Files" "$skill" \
		"skill has no Windows path examples"

	# "domain vs project" as required terms (old Terminology section).
	forbid_re "^## Terminology" "$skill" \
		"skill has no Terminology section requiring domain vs project"
	forbid_text "Use only these two terms" "$skill" \
		"skill does not require domain vs project as the only terms"
	forbid_text "always domain vs project" "$skill" \
		"skill does not require always domain vs project"
	forbid_text "Do not mix terminology" "$skill" \
		"skill does not require domain vs project terminology"
	forbid_text "**domain** AGENTS.md" "$skill" \
		"skill does not define required domain AGENTS.md term"

	if [ -f "$skill" ]; then
		if grep -i "domain vs project" "$skill" |
			grep -Eiv "no |not |don't |do not" >/dev/null; then
			fail "skill uses domain vs project as required terms"
		else
			ok "skill does not use domain vs project as required terms"
		fi
	fi

	# Forbidden generated headings may be quoted as drop / do-not-emit.
	# They must not appear as required template items or verbatim blocks.
	assert_heading_not_templated "## Domain" \
		"## Domain"
	assert_heading_not_templated "## Self-Improvement Loop for each project" \
		"## Self-Improvement Loop for each project"
}

# A SKILL.md line may name a forbidden generated heading only in a drop /
# do-not-emit instruction. A bare heading or required-order listing fails.
assert_heading_not_templated() {
	heading=$1
	label=$2
	templated=0

	while IFS= read -r line || [ -n "$line" ]; do
		case $line in
		*"$heading"*)
			if printf '%s\n' "$line" | grep -Eqi 'drop leftover|do not emit|not emit|forbidden'; then
				continue
			fi
			templated=1
			fail "skill templates $label as output (not as a forbidden heading): $line"
			;;
		esac
	done <"$skill"

	if [ "$templated" -eq 0 ]; then
		ok "skill does not template $label as generated output"
	fi
}

main() {
	check_expected_sections
	check_fixture
	check_happy_path
	check_edges

	if [ "$failures" -ne 0 ]; then
		printf '%s\n' "FAIL: $failures check(s) failed" >&2
		exit 1
	fi
	printf '%s\n' "PASS: research-project-agents skill contract"
}

main "$@"
