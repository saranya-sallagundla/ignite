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

Interview-style, open-ended. Ran ~32 minutes (over the 20-min cap).

1. **Debug `if [$1 -gt 10]`, missing-bracket-space error** — passed cleanly, correct full
   mechanism (token merging, attempted execution of the literal merged word).
2. **Infinite `while` loop — cause and how to stop it live** — passed cleanly, correct on both
   the root cause (counter never increments) and the fix (`Ctrl+C`/`SIGINT`).
3. **`$1` scoping: script-level vs. function-level** — **did not land**, even after multiple
   distinct explanations. Got the surface-level branching outcome right but could not
   articulate that the two `$1`s are entirely separate, independently-scoped variables. Flagged
   for deferred mastery (see above) — revisit before Topic 4.
4. **A defined-but-never-called function produces no output** — missed entirely ("no idea");
   explained directly. Real gap: functions must be explicitly invoked, not just defined.
5. **`"$@"` vs. `$@` (quoting/word-splitting)** — went beyond what was explicitly taught this
   session; explained directly, not held against the score, since introducing it live in the
   quiz is fair when it wasn't covered beforehand.

**Verdict on Attempt 1**: conditionals, loops, and exit codes solid; functions (invocation +
scoping) did not land, even after multiple analogy-based re-explanations in the moment.

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

Ran ~23 minutes. Five fresh interview-style questions, not repeats of Attempt 1:
1. **`-eq` vs. `=`** (numeric vs. string comparison) — passed cleanly.
2. **`"$@"` vs. a hardcoded list — practical tradeoff** — passed cleanly, correctly identified
   flexibility vs. when a fixed list is actually preferable.
3. **Function scoping, fresh scenario** (`multiply()` using `$1`/`$2`, an outer variable `x`
   untouched by the call) — passed cleanly, correctly traced both the function's local
   computation and the outer variable's independence. The exact gap from Attempt 1, now solid.
4. **Stopping a multi-step script on failure** — introduced `exit [CODE]` directly (not
   explicitly taught before this point), then correctly traced that a failed step's `exit 1`
   prevents every subsequent step from running at all. Also correctly reasoned that different
   exit codes per failure point (`exit 1`, `exit 2`, `exit 3`) is better practice than reusing `1`
   everywhere, once the idea was raised.
5. **Combined for-loop + function + even-check reasoning** — correctly predicted output (`2` and
   `4`) for a described (not shown) script run against `2 3 4 5`.

**Final verdict: Topic 3 — CLEARED in 2 attempts.** Lesson for future topics, worth remembering:
if a concept doesn't land after 2-3 varied explanations in the moment, **switch to concrete
tracing (run real code, watch the actual values) rather than trying yet another analogy** — this
unblocked things noticeably faster than continuing to reason abstractly.
