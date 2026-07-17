# Minimal Software Project

This neutral fixture models one bounded source edit. The governed transaction
changes `src/value.txt` from `value=1` to `value=2` and runs one approved local
check. Control records are installed into a temporary copy by the end-to-end
test so this source fixture remains reusable.

Authority status: the fixture, temporary records, and test receipt are
non-authoritative examples. A PASS proves only the declared bounded value
fixture, not the correctness of a larger software system.
