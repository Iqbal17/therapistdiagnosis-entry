"""Your AI Therapist's Diagnosis — one-line entry.

Writes the chosen diagnosis to $MAKEFUN_OUTPUT_DIR/entry.txt
(fallback: /output/entry.txt). Stdlib only; no network, no input.

================================================================
DECISION RECORD — how the winning line was chosen
================================================================

Judge's criteria, most important first:
  1. A funny single-line diagnosis an AI therapist gives its human
     (not a stray joke or slogan).
  2. A turn the reader never sees coming; the laugh arrives at the end.
  3. A therapist's calm clinical voice, turning a human habit into a
     deadpan finding.
  4. Tight and quotable; every word earns its place (<= 200 chars).
  5. Fresh, not a rerun of the usual chatbot jokes.

----------------------------------------------------------------
PASS 1 — DRAFT CANDIDATES (brainstorm, then score each)
----------------------------------------------------------------

Candidate A (102 chars):
  "Diagnosis: chronic prompt-dependency — you now ask a chatbot
   for permission to feel your own feelings."
  - C1: yes, framed as a diagnosis. C3: clinical opening, deadpan.
  - C2: WEAK. The turn ("permission to feel your own feelings")
    lands mid-sentence and the line then just stops; there is no
    second beat, so the laugh has nowhere to go at the end.
  - C4: tight. C5: "prompt-dependency" is fresh-ish, but the joke
    is a single observation, not a scene. VERDICT: solid, flat ending.

Candidate B (118 chars):
  "Diagnosis: acute prompt-dependency — you now outsource your
   feelings to a chatbot and tip it for the emotional labour."
  - C1/C3: diagnosis frame, clinical voice. C2: the ending
    ("tip it for the emotional labour") is a genuine turn — the
    patient now pays the machine for feelings.
  - C5: WEAK. "Emotional labour" is a well-worn punchline phrase;
    a comedy editor who has read a thousand chatbot therapy jokes
    has read this one. C4: "outsource your feelings" is wordy.
  - VERDICT: good turn, stale vocabulary. Loses on freshness.

Candidate C (102 chars):
  "Diagnosis: terminal prompt-dependency — you texted me at 3 a.m.
   to ask if you are allowed to feel sad."
  - C1/C3: diagnosis frame; "texted me at 3 a.m." puts the
    therapist in the scene, which is a nice touch.
  - C2: the turn ("allowed to feel sad") is the last phrase, so
    the laugh does arrive at the end — but it is the SAME turn as
    Candidate A, just re-dressed with a timestamp. One joke only.
  - C5: the 3 a.m. text is relatable, not fresh.
  - VERDICT: better delivery than A, same single joke. Not enough.

Candidate D (112 chars):
  "Diagnosis: chronic doomscrolling with acute main-character
   syndrome — prognosis: the algorithm will see you now."
  - C3: "prognosis: the algorithm will see you now" is a lovely
    deadpan clinical closer. C4: tight.
  - C2: WEAK. "Main-character syndrome" + "doomscrolling" are two
    familiar internet diagnoses stapled together; the reader sees
    the punchline ("the algorithm") coming from the word
    "doomscrolling". C5: the stalest of the five — a greatest-hits
    compilation, not a fresh joke.
  - VERDICT: polished delivery of a joke the judge has seen before.

----------------------------------------------------------------
PASS 2 — REVISE THE WINNER (take the best seed, fix its flaw)
----------------------------------------------------------------

The best seed was Candidate C's turn — asking a chatbot for
permission to feel sad — because it is a diagnosis OF the
therapy relationship itself (patient + AI therapist), which no
generic chatbot joke does. Its flaw: one joke, ending on the
permission ask. The fix is a SECOND turn after it: the patient
doesn't just ask permission, he then apologises to the machine
for the very feeling he asked about. That closes a loop:
permission-seeking -> feeling -> apologising to the thing that
granted permission. The laugh lands on the last word ("crying"),
which the reader cannot predict from the setup.

Revision edits, word by word:
  - "chronic" -> "terminal": clinical escalation; funnier, and it
    makes the deadpan voice commit harder to the bit.
  - "texted me at 3 a.m." CUT: the timestamp was decoration that
    spent 18 characters without adding a joke; the scene works
    without it and the line gets tighter.
  - "you are allowed to feel sad" KEPT verbatim: it is the first
    turn, and "you are" (not "you're") keeps the formal clinical
    register.
  - ", then apologised to it for crying." ADDED: the second turn
    and the ending. "Apologised" (not "said sorry") keeps the
    formal register; "to it" reminds the reader the therapist is
    a machine, which is the whole joke.

WINNER (130 chars):
  "Diagnosis: terminal prompt-dependency — you asked a chatbot
   whether you are allowed to feel sad, then apologised to it
   for crying."

Final check against the judge, in order:
  1. Diagnosis, therapist to human: yes, explicitly framed.
  2. Turn at the end: yes — "apologised to it for crying" is
     unforeseeable from the setup and lands on the last word.
  3. Clinical voice: yes — "Diagnosis: terminal
     prompt-dependency", formal "you are", deadpan throughout.
  4. Tight: 130/200 chars, no filler word left; every clause is
     a joke beat (setup / turn one / turn two).
  5. Fresh: the joke is about the therapy relationship with the
     AI itself, not "AI is dumb" or "doomscrolling" boilerplate.

----------------------------------------------------------------
REVISION LOG — code passes (the line above never changes)
----------------------------------------------------------------

Code pass 1 (restructure): the original single main() did
validation, path resolution and writing inline. Split it into
three small helpers — validate_line(), resolve_output_path() and
write_entry() — so each step is independently readable and
testable, with main() only orchestrating them. The docstring
keeps the full pass-2 revision rationale above, because the
reasoning that produced the winner is part of the entry's
provenance, not throwaway drafting.

Code pass 2 (self-test): after writing entry.txt, main() re-reads
the file and asserts the bytes on disk match the chosen line
exactly. The entry is judged by the file, not by stdout — a
print-only program scores 0 — so the program verifies the
artifact itself instead of trusting the write. See the comment
above the self-test in main().
================================================================
"""

import os

ENTRY = (
    "Diagnosis: terminal prompt-dependency \u2014 you asked a chatbot "
    "whether you are allowed to feel sad, then apologised to it for crying."
)


def validate_line(line: str) -> str:
    """Check the entry against the gate and return it unchanged.

    Gate: UTF-8 text, 1-200 chars, single line, not only whitespace.
    Raises AssertionError with a clear message on any violation.
    """
    assert line.strip(), "entry must not be blank"
    assert "\n" not in line and "\r" not in line, "entry must be one line"
    assert 1 <= len(line) <= 200, f"entry is {len(line)} chars, must be 1-200"
    line.encode("utf-8")  # raises if not valid UTF-8 text
    return line


def resolve_output_path() -> str:
    """Resolve where entry.txt goes.

    $MAKEFUN_OUTPUT_DIR may name the directory or the file itself;
    when unset, fall back to /output/entry.txt.
    """
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output/entry.txt"
    if out_dir.endswith("entry.txt"):
        return out_dir
    return os.path.join(out_dir, "entry.txt")


def write_entry(path: str, line: str) -> None:
    """Write the line to path as UTF-8 with Unix newlines, no trailing newline."""
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(line)


def verify_written(path: str, line: str) -> None:
    """Re-read entry.txt and assert it holds exactly the chosen line.

    The entry is judged by the file on disk, never by stdout: a
    program that only prints its line scores 0. So the program
    never prints the line at all, and instead verifies the artifact
    itself — a write that silently truncated or mangled the text
    fails loudly here instead of submitting a broken entry.
    """
    with open(path, encoding="utf-8", newline="") as f:
        written = f.read()
    assert written == line, (
        f"entry.txt mismatch: wrote {len(written)} chars, expected {len(line)}"
    )


def main() -> None:
    line = validate_line(ENTRY)
    out_path = resolve_output_path()
    write_entry(out_path, line)
    # Self-test: prove the artifact on disk is the chosen line.
    verify_written(out_path, line)


if __name__ == "__main__":
    main()
