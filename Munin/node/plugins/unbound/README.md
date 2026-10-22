# Imported Unbound plugin sources

`unbound_munin_original` is a historical upstream reference, retained unchanged
and non-executable. Only that exact reference path is excluded from ShellCheck
and shfmt; it is not a selected runtime entry point.

`unbound_munin_` is the separately imported candidate. It retains its existing
state/cache and locking behavior. Publication cleanup quotes counter comparisons,
uses an empty-string test, removes an unused assignment and applies repository
formatting. Explicit lint annotations retain decimal `expr` calculations and
intentional iteration over whitespace-free Unbound statistic keys.

The plugin settings and link helper are retained separately. No Unbound profile
is selected or deployed by these files. Qualify target privileges, state handling,
configuration/fetch and host assignment before a separately approved installation.
These imports are unrelated to j2-svntp1's accepted NTP monitoring profile.
