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
5. **`nano` vs. `printf`'s `\n` handling** — typed literal backslash-`n` characters into `nano`
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

## Day 2 — TBD

_To be filled in as Day 2 progresses._
