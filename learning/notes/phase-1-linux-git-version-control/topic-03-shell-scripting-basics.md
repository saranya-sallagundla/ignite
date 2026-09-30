# Topic 3 — Linux: Shell Scripting Basics

> Personal study notebook — full teaching content, commands, outputs, and explanations.
> Distinct from `progress.md` (tracking) and `session_notes.md` (short personal reflection).

---

## Day 1 — 2026-07-10 (script structure, variables, conditionals)

### 1. What is a shell script, and the shebang line

A shell script is a text file containing a sequence of shell commands, saved so they can run
repeatably without retyping them.

**Syntax**: every proper script's first line:
```
#!/bin/bash
```
- `#!` — marker telling the OS "this file is a script, here's what should run it"
- `/bin/bash` — path to the interpreter that executes the rest of the file

Without it, a script can still run via `bash script.sh` (explicitly naming the interpreter), but
not via `./script.sh` directly, since the OS wouldn't know which interpreter to use.

**Verified hands-on**:
```
$ printf '#!/bin/bash\necho "Hello from my first script"\n' > hello.sh
$ bash hello.sh
Hello from my first script
$ ./hello.sh
bash: ./hello.sh: Permission denied
```
`bash hello.sh` worked immediately (explicitly invoking the interpreter). `./hello.sh` failed —
new files via `>` redirection default to `644` (no execute), same lesson as Topic 2's
`myscript.sh` exercise. Fixed the same way:
```
$ chmod 744 hello.sh
$ ./hello.sh
Hello from my first script
```
**New shorthand learned**: `chmod +x FILE` — symbolic mode, adds execute permission (owner/group/
others) without needing to compute the exact octal number. The common real-world idiom for "just
make this runnable," used more often than manually computing `744`/`755` for scripts.

**Gotcha, hit and corrected**: running `/hello.sh` (no leading dot) instead of `./hello.sh` —
`/hello.sh` means "look at the filesystem root," an entirely different location. `.` = current
directory, `/` alone = root of the whole tree (Topic 1 concept, reinforced).

**Permissions persist across content overwrites**: rewriting `hello.sh`'s content via `>` (to add
a variable, next section) did **not** require `chmod +x` again — since the file already existed
with `rwxr--r--`, overwriting content via `>` doesn't touch the file's permission metadata (same
inode, permissions untouched). Only a genuinely **new** filename would default back to `644`.

### 2. Variables

**Syntax**: `VARIABLE_NAME=value` (no spaces around `=` — strict in bash) · reference with
`$VARIABLE_NAME`

**Verified hands-on**:
```
$ printf '#!/bin/bash\nname="World"\necho "Hello, $name!"\n' > hello.sh
$ ./hello.sh
Hello, World!
```

### 3. Positional arguments

**Syntax**: `$1`, `$2`, `$3`... — 1st, 2nd, 3rd argument passed to the script. `$0` = the
script's own name/path. `$#` = total count of arguments passed.

**Verified hands-on**:
```
$ printf '#!/bin/bash\necho "Script name: $0"\necho "First arg: $1"\necho "Second arg: $2"\necho "Total args: $#"\n' > args.sh
$ chmod +x args.sh
$ ./args.sh apple banana
Script name: ./args.sh
First arg: apple
Second arg: banana
Total args: 2
```
A missing positional argument (e.g. running with only one arg, so `$2` has nothing) doesn't
error — bash just treats it as an empty/unset value, printing nothing after the label.

### 4. Conditionals — `if`/`elif`/`else`/`fi`

**Syntax**:
```
if [ CONDITION ]; then
    commands
elif [ CONDITION ]; then
    commands
else
    commands
fi
```
Strict syntax rules: **spaces required** around `[` and `]` (`[` is actually a command, not just
a bracket character), `;` before `then`, block closes with `fi` (backwards spelling, same
convention as `esac` for `case`).

**Operators**: numbers — `-eq -ne -gt -lt -ge -le`; strings — `=` / `==`; `-z STRING` (true if
empty); `-f FILE` (true if file exists).

**Verified hands-on — string/empty check**:
```
$ printf '#!/bin/bash\nif [ -z "$1" ]; then\n    echo "Error: no argument provided"\nelse\n    echo "You provided: $1"\nfi\n' > check.sh
$ chmod +x check.sh
$ ./check.sh
Error: no argument provided
$ ./check.sh hello
You provided: hello
```

**Verified hands-on — numeric comparison**:
```
$ printf '#!/bin/bash\nif [ "$1" -gt 0 ]; then\n    echo "Positive"\nelif [ "$1" -lt 0 ]; then\n    echo "Negative"\nelse\n    echo "Zero"\nfi\n' > numcheck.sh
$ chmod +x numcheck.sh
$ ./numcheck.sh 5
Positive
$ ./numcheck.sh -3
Negative
$ ./numcheck.sh 0
Zero
```

### 5. Arithmetic expansion

**Syntax**: `$(( EXPRESSION ))` — lets bash evaluate math, including `%` (modulo — remainder
after division). `$1 % 2` is `0` for even numbers, `1` for odd numbers.

### 6. Combined exercise — `classify.sh` (sign + odd/even), written from scratch with real debugging

Goal: one script, two independent `if` blocks — classify a number's sign AND odd/even.

**The real struggle, worth keeping as a record** (several genuine, distinct mistakes, each
corrected in turn):
1. **Wrong labels reused** — first attempt copied `numcheck.sh`'s sign-check labels
   ("positive"/"negative"/"zero") onto the odd/even logic, answering the wrong question
   entirely. Corrected by isolating the underlying concept first (remainder `0` → even, `1` →
   odd) before returning to code.
2. **`else` given a condition** — wrote `else [ ... ]; then`, which is invalid; `else` never
   takes a condition (that's what `elif` is for — a genuinely different, additional check). Since
   "remainder is 0" vs. "remainder isn't 0" are the only two possibilities, bare `else` already
   covers the second case with no condition needed.
3. **Missing separator after `else`** — `else echo "..."` on one line errors; needs `else;
   echo "..."` or `else` on its own line. Same root issue recurred later with `fi` too (`echo
   "zero" fi` — `fi` on the same line as `echo`'s argument gets treated as literal text being
   echoed, not the closing keyword).
4. **Merged `fi`/`if`** — closing one block and opening the next got run together
   (`fi [ ... ]; then` — missing a fresh `if` keyword), and separately, forgot the `fi` between
   the two independent blocks entirely. Fix: **two completely separate `if...fi` pairs**, one
   fully closed before the next begins — nothing shared or merged between them.
5. **`nano` (`nano FILENAME`) vs. `printf`'s `\n` handling** — typed literal backslash-`n` characters into `nano`
   expecting them to become line breaks (works in `printf`, since `printf` specifically
   interprets `\n`; **`nano` does not** — it needs the actual **Enter key**, not typed-out `\n`
   text). Result: the entire script became one garbled line, and the shebang line absorbed the
   rest of the script as if it were the interpreter path, producing `cannot execute: required
   file not found`. Fixed by retyping with real line breaks.
6. **Final self-debugged syntax error** — after fixing the above, hit
   `syntax error near unexpected token ';'` pointing at a specific line number, and fixed it
   independently by re-opening `nano` and adjusting — genuine independent troubleshooting using
   bash's line-number error reporting.

**Final, correct, working script**:
```bash
#!/bin/bash
if [ "$1" -gt 0 ]; then
    echo "positive"
elif [ "$1" -lt 0 ]; then
    echo "negative"
else
    echo "zero"
fi

if [ $(( $1 % 2 )) -eq 0 ]; then
    echo "even"
else
    echo "odd"
fi
```

**Verified hands-on — all three test cases correct**:
```
$ ./classify.sh 7
positive
odd
$ ./classify.sh -4
negative
even
$ ./classify.sh 0
zero
even
```
(7: positive, `7%2=1`→odd ✓ · -4: negative, `-4%2=0`→even ✓ · 0: zero, `0%2=0`→even ✓)

### 7. `nano` — basic terminal text editor

**Syntax**: `nano FILENAME` — opens/creates a file for direct editing in the terminal
- Type normally, press **Enter** for real line breaks (not `\n` as text — that's a `printf`-only
  behavior)
- `Ctrl+O` then `Enter` — save ("Write Out")
- `Ctrl+X` — exit

Used here because multi-line scripts are more natural to write in a real editor than via
`printf`'s escape-sequence trick, which only really suits short one-liners.

---

## Day 2 — 2026-07-11 / 2026-07-12 (loops, functions, exit codes — quiz deferred on functions)

### 1. Loops — `for` and `while`

**Syntax**: `for VAR in ITEM1 ITEM2 ITEM3; do ... done` — iterate over a fixed list
**Syntax**: `for VAR in "$@"; do ... done` — iterate over however many arguments were passed to
the script, whatever they are (combines with Day 1's positional-argument knowledge)
**Syntax**: `while [ CONDITION ]; do ... done` — repeats as long as the condition stays true

**Verified hands-on — `for` over arguments**:
```
$ printf '#!/bin/bash\nfor fruit in "$@"; do\n    echo "I like $fruit"\ndone\n' > fruits_loop.sh
$ chmod +x fruits_loop.sh
$ ./fruits_loop.sh apple bannana cherry
I like apple
I like bannana
I like cherry
$ ./fruits_loop.sh kiwi
I like kiwi
```
Adapts to however many arguments are given — no hardcoded list.

**Verified hands-on — `while` counter, including a real self-debugged bug**:
```
count=1
while [ $count -le 5 ]; do
    echo "Count: $count"
    count=$(( count + 1 ))
done
```
**Gotcha, hit for real**: wrote the increment as `number=$(( count + 1 ))` — assigning to the
correct variable (`number`) but reading from the *wrong* one (`count`, which was undefined,
evaluating to `0`), so `number` stayed stuck at `1` forever. Root cause of an infinite loop:
**the loop's condition variable never actually changes**, so the condition never becomes false.
Fixed to `number=$(( number + 1 ))` — same variable on both sides. `Ctrl+C` (sends `SIGINT`) is
how you'd stop a genuinely stuck loop running in a terminal.

**`$@` vs `"$@"` — a real distinction, explained directly (goes past what was explicitly taught,
surfaced during the Day 2 quiz)**: `"$@"` (quoted) treats each argument as one distinct item,
even if an argument itself contains spaces. `$@` (unquoted) triggers word-splitting — an argument
like `"my folder"` would incorrectly split into two separate loop items (`my` and `folder`). Real
bug risk with paths/names containing spaces; always quote `"$@"`.

### 2. Functions

**Syntax**: `function_name() { commands }` — define once; call later just by name:
`function_name`. Arguments passed to a function are read the same way as script arguments
(`$1`, `$2`) — but scoped only to that specific function call.

**Verified hands-on**:
```
#!/bin/bash
greet() {
    echo "Hello, $1!"
}
greet "Alice"
greet "Bob"
```
→ `Hello, Alice!` then `Hello, Bob!`

**Combined with a script-level conditional** (two independently-scoped `$1`s in one script):
```
#!/bin/bash
greet() {
    echo "Hello, $1!"
}
if [ "$1" -eq 1 ]; then
    greet "Alice"
elif [ "$1" -eq 2 ]; then
    greet "Bob"
fi
```
→ `./function.sh 1` → `Hello, Alice!` · `./function.sh 2` → `Hello, Bob!`

**⚠ Attempt 1 quiz gap — function scoping did not click this session, despite several
different explanations (office/tray analogy, step-by-step value tracing).** The core fact:
`$1` inside the `if` line refers to the *script's own* first argument; `$1` inside `greet()` is
a *completely separate*, independently-scoped variable, holding only whatever was explicitly
handed to that specific function call — the two never merge or share state, even though they
have the identical label `$1`. **To revisit next session, before Topic 4, with a fresh approach**
— likely worth trying real side-by-side `echo` tracing (printing both `$1`s at each step of an
actual run) rather than another analogy, since analogies didn't land after multiple attempts.

**Also missed on the Day 2 quiz**: a function that's *defined* but never *called* anywhere in the
script produces no output and no error — defining a function is like writing a recipe card, it
doesn't "cook" anything until something explicitly invokes it (`function_name` on its own line,
outside the definition).

### 3. Exit codes and error handling

**Syntax**: `$?` — holds the exit code of the **most recently run** command. `0` = success;
any non-zero value = some kind of failure (the specific number is defined by whichever program
ran — e.g., `ls` uses `2` for "path doesn't exist," not just a generic `1`).

**Verified hands-on**:
```
$ ls /etc
... (real output) ...
$ echo $?
0
$ ls /nonexsistent-folder
ls: cannot access '/nonexsistent-folder': No such file or directory
$ echo $?
2
```

**Using it in a script**:
```
#!/bin/bash
ls "$1" > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "Folder exists"
else
    echo "Folder does not exist"
fi
```
`> /dev/null` discards normal output; `2>&1` redirects error output the same way (full
explanation of the `2>&1` numbering deferred to Topic 4). Combo means "run it, but suppress all
output — we only care about the exit code."

**Verified hands-on**:
```
$ ./checkfolder.sh /etc
Folder exists
$ ./checkfolder.sh /fake
Folder does not exist
```

### 4. Combined exercise — `checkall.sh` (function + loop + exit code, tied to the project)

Goal: check multiple folders at once, reusing one function per folder — directly useful later in
`project/scripts/` for verifying expected directories exist before a deployment step runs.

**Final working script, built in two steps (wrap existing logic into a function, then loop over
it)**:
```bash
#!/bin/bash
check_folder() {
    ls "$1" > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "$1 exists"
    else
        echo "$1 does not exist"
    fi
}

for folder in "$@"; do
    check_folder "$folder"
done
```

**Verified hands-on**:
```
$ ./checkall.sh /etc /fake1 /tmp
/etc exists
/fake1 does not exist
/tmp exists
```
Real self-debugging along the way: filename mismatches (script initially saved under a different
name, then a typo rename to `.ah` instead of `.sh`) — both caught and fixed independently using
`mv`, without needing correction.

---

## Day 2 Quiz — Topic 3 (all of shell scripting) — Attempt 1: FAIL, Attempt 2: PASS

### Attempt 1 — FAIL (functions)

Interview-style, open-ended. Ran ~32 minutes (over the 20-min cap). 5 questions, question and
full correct answer for each:

1. **Debug this: `if [$1 -gt 10]` throws an error — what's wrong and why?**
   The problem is the missing spaces around `[` and `]`. `[` isn't just punctuation — it's
   actually a command (the test command), and `]` is its required closing argument, so bash needs
   whitespace on both sides to recognize them as separate tokens. Written as `[$1`, bash instead
   sees one single merged word — after variable expansion (e.g. `$1` = `5`) it becomes the literal
   token `[5`, and bash tries to run a command literally named `[5`, which doesn't exist, producing
   a "command not found"-style error rather than doing the comparison. The fix is to always put
   spaces around the brackets and quote the variable: `if [ "$1" -gt 10 ]; then`.

2. **An infinite `while` loop is running live — what caused it, and how do you stop it?**
   The root cause of an infinite `while` loop is that the condition variable never actually
   changes value, so the loop's test condition never becomes false. This happens in practice when
   the increment line assigns to the wrong variable — e.g. `number=$(( count + 1 ))` updates
   `number` but reads from `count`, leaving the loop's real condition variable frozen. The fix is
   making sure the same variable is both tested and incremented (`count=$(( count + 1 ))`). To stop
   a loop that's already stuck running in the terminal, `Ctrl+C` sends the process a `SIGINT`
   signal, interrupting it immediately.

3. **What's the real relationship between the script's `$1` (used in an `if` check) and a
   function's own `$1` (e.g. inside `greet()`) in the same script?**
   They are two entirely separate, independently-scoped variables that just happen to share the
   identical label `$1` — they never merge, share state, or affect one another. The script-level
   `$1` always refers to the first argument passed to the script itself on the command line. A
   function's `$1` refers only to whatever argument was explicitly passed to that specific function
   call (e.g. `greet "Alice"` gives `greet`'s own `$1` the value `"Alice"`, regardless of what the
   script's `$1` currently holds). This was proven directly with a trace script that printed the
   script's `$1` before calling `greet`, printed `greet`'s own `$1` from inside the function, then
   printed the script's `$1` again after the call returned — the outer value stayed completely
   unchanged across the whole run, confirming the two variables never interact.

4. **What happens if a function is defined in a script but never called anywhere?**
   Nothing happens — no output and no error. Defining a function (`function_name() { ... }`) is
   like writing a recipe card: it just stores the instructions for later, it doesn't execute
   anything by itself. A function only actually runs when something explicitly invokes it by name
   on its own line (e.g. `function_name`), outside of the definition block. A script that defines a
   function but never calls it will run to completion having done nothing with that function at
   all.

5. **What's the actual difference between `"$@"` and `$@` in a `for` loop?**
   `"$@"` (quoted) preserves each argument as one distinct item, even if that argument itself
   contains spaces. `$@` (unquoted) triggers word-splitting, so an argument like `"my folder"`
   would incorrectly be split into two separate loop items (`my` and `folder`) instead of staying
   one. This is a real bug risk whenever arguments might contain spaces (paths, names), so `"$@"`
   should always be quoted in practice.

**How Attempt 1 actually went**: Q1 and Q2 passed cleanly. Q3 (the `$1` scoping question) did not
land despite multiple analogy-based explanations, and was flagged for deferred mastery. Q4 was
missed entirely ("no idea"). Q5 went beyond what had been explicitly taught this session, so it
was explained directly rather than held against the score.

### Re-teach — concrete tracing instead of analogy

Rather than another analogy, built and ran a real script printing `$1` at three points — before,
inside, and after a function call — so the independent scoping could be **observed directly**:
```bash
#!/bin/bash
echo "outer value before: $1"
greet() {
    echo "inside function value: $1"
}
greet "Alice"
echo "outer value after: $1"
```
```
$ ./trace.sh 99
outer value before: 99
inside function value: Alice
outer value after: 99
```
Watching the outer `99` stay unchanged before *and* after the function call — never becoming
`Alice`, never affected by it — made the independent-scoping concept land where analogies (the
office/tray comparison, tried multiple ways) hadn't. Two quick verification questions
(predicting `./trace.sh 500`'s output; explaining why a defined-but-never-called function
produces nothing) both passed immediately afterward.

### Attempt 2 — full retest, all-new questions — PASS

Ran ~23 minutes. Five fresh interview-style questions, not repeats of Attempt 1, question and
full correct answer for each:

1. **What's the actual difference between `-eq` and `=`?**
   `-eq` is one of the numeric comparison operators (alongside `-ne`, `-gt`, `-lt`, `-ge`, `-le`)
   — it compares its two operands as integer numbers. `=` (or `==`) is the string comparison
   operator — it compares its two operands as literal text, character by character. Using the
   wrong one for the data type being compared either errors out or gives a misleading result, so
   picking the operator has to match whether you're actually comparing numbers or strings.

2. **When would you use `"$@"` in a loop versus just hardcoding a fixed list of items — what's
   the practical tradeoff?**
   A hardcoded list (`for VAR in ITEM1 ITEM2 ITEM3; do ... done`) only works for a fixed,
   known-in-advance set of items — it's simple, but the script has to be edited any time the set
   of items changes. `"$@"` instead iterates over whatever arguments were actually passed to the
   script at runtime, so the exact same script adapts to any number of inputs without any code
   changes — proven earlier with `fruits_loop.sh`, which handled both a 3-fruit run and a 1-fruit
   run with no modification. The tradeoff: a hardcoded list is fine only when the set of items
   genuinely never changes; `"$@"` is the better choice whenever the script needs to stay reusable
   across different runs with different inputs.

3. **Fresh scenario: a function `multiply()` uses `$1` and `$2` internally, and the script also
   has its own outer variable `x`. Does calling `multiply` affect `x`?**
   No — this is the same independent-scoping principle from the `$1` scoping question: `multiply`'s
   `$1` and `$2` are parameters local to that one function call, existing only for as long as that
   call is running, and they have no relationship whatsoever to any variable in the outer script,
   even one also referenced as `$1` or named similarly. The outer variable `x` keeps whatever value
   it already had, completely untouched by the function call, exactly like the outer script's `$1`
   stayed unchanged before and after `greet` was called in the earlier trace exercise.

4. **How do you stop a multi-step script from continuing after one of its steps fails?**
   The `exit CODE` command immediately terminates the running script at that exact line — nothing
   after it executes — and `CODE` becomes the script's own exit status, retrievable afterward via
   `$?`. In a multi-step script, placing `exit 1` (or another non-zero code) right after a failed
   step's check stops every subsequent step from running at all, instead of pressing on with work
   that depends on a step that already failed. It's also better practice to use a different exit
   code per distinct failure point (`exit 1`, `exit 2`, `exit 3`, ...) rather than reusing `1`
   everywhere, since the specific number then tells you (or anything checking `$?` afterward)
   exactly which step failed, not just that something, somewhere, failed.

5. **Given a script that loops over `"$@"`, calls a function, and only prints even numbers, what
   would it output when run against `2 3 4 5`?**
   `2` then `4`. Walking through it one argument at a time using the odd/even check from earlier
   (`$(( $1 % 2 ))` — remainder `0` means even, remainder `1` means odd): `2 % 2 = 0` → even →
   printed; `3 % 2 = 1` → odd → skipped; `4 % 2 = 0` → even → printed; `5 % 2 = 1` → odd → skipped.
   So only `2` and `4` get printed, in that order.

**How Attempt 2 actually went**: Q1 and Q2 passed cleanly. Q3 passed cleanly — the exact gap from
Attempt 1, now solid. Q4 introduced `exit CODE` live (not explicitly taught before this point) and
was reasoned through correctly once raised. Q5 passed cleanly with the correct predicted output.

**Verdict**: **Topic 3 CLEARED, in 2 attempts, 80/100** (Quiz 30/40 — Attempt 1 failed on
function invocation/`$1` scoping, all other areas passed cleanly; Attempt 2 full retest passed
cleanly, all-new questions; Hands-on 28/30 — real, independently-debugged syntax errors throughout
`classify.sh`; Depth 22/30 — functions didn't land until re-taught via concrete tracing instead of
analogy). Lesson for future topics, worth remembering:
if a concept doesn't land after 2-3 varied explanations in the moment, **switch to concrete
tracing (run real code, watch the actual values) rather than trying yet another analogy** — this
unblocked things noticeably faster than continuing to reason abstractly.
