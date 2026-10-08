# SAT Evaluator

**Security Awareness Training Evaluator**  
A quality review tool for cybersecurity quiz questions and training scenarios.

Built by [Tessa Angelika Mmaitsi](https://github.com/Tessangelika) — Learning Experience Designer and CyberGirls Fellow.

---

## What it does

Paste in a security awareness quiz question (including answer options, correct answer, and any feedback notes) and the tool scores it against a six-point quality rubric. At the end it produces a full report for the whole quiz showing where the gaps are.

It is designed for:
- Learning designers reviewing cybersecurity training content before deployment
- Security teams assessing the quality of awareness quizzes
- Anyone building scenario-based security training who wants structured feedback

---

## The rubric

Each question is evaluated against six criteria:

| # | Criterion | Why it matters |
|---|---|---|
| 1 | Has a realistic scenario | Abstract questions don't build real-world recognition skills |
| 2 | Tests recognition, not just recall | Learners need to practise responding, not just naming concepts |
| 3 | Has a correct answer | Ambiguous questions undermine trust in the training |
| 4 | Explains why the answer is correct | Reasoning builds lasting behaviour change |
| 5 | Gives feedback on wrong answers | Learners who get it wrong need to understand their mistake |
| 6 | Maps to a recognisable attack type | Mental models help learners apply learning beyond the quiz |

A question needs 4 out of 6 to pass. The final report shows pass rate per criterion across the whole quiz and highlights the two biggest gaps.

---

## Usage

No external dependencies. Runs on Python 3.8 or later.

```bash
python evaluator.py
```

You will be prompted to:
1. Enter a quiz title (optional)
2. Paste each question — include the scenario, answer options, correct answer, and any feedback notes you have
3. Press Enter twice when done with each question
4. Type EXIT to finish and see the full report
5. Optionally save the report to a text file

---

## Example output

```
============================================================
  QUESTION 1 RESULT
============================================================
  Score: 5/6  |  PASS

  ✓  Has a realistic scenario
  ✗  Tests recognition, not just recall
       → Reframe the question so the learner has to decide what to do,
         not just name a concept. Use: 'What should you do?' or
         'What is the safest response?'
  ✓  Has a correct answer
  ✓  Explains why the answer is correct
  ✓  Gives feedback on wrong answers
  ✓  Maps to a recognisable attack type
```

---

## What makes a good security awareness question

The tool is based on evidence from learning design and security education research:

**Scenario-based questions outperform knowledge-recall questions** for behaviour change. A learner who can answer "What is phishing?" cannot necessarily recognise a phishing email in their inbox. A learner who has practised responding to a realistic scenario is more likely to respond correctly when it happens for real.

**Feedback on wrong answers matters as much as feedback on right ones.** Learners who pick the wrong option and see only "Incorrect" leave with a gap. Learners who see "Incorrect — replying to the email keeps you in contact with the attacker" leave with understanding.

**Naming the attack type builds a mental model** that transfers across contexts. A learner who knows they just practised a BEC scenario can recognise BEC signals in situations the training didn't cover.

---

## Design philosophy

This tool applies the same logic as the broader [threat-aware-learner](https://github.com/Tessangelika/threat-aware-learner) project: security awareness training should change behaviour, not just pass audits. Most security quizzes test whether people remember definitions. This tool evaluates whether quizzes are designed to build the skills that actually protect organisations.

---

## Requirements

Python 3.8 or later. No external dependencies.

---

## Status

| Feature | Status |
|---|---|
| Six-point rubric evaluation | Complete |
| Per-question feedback | Complete |
| Full quiz summary report | Complete |
| Save report to file | Complete |
| Web interface | Planned |
| ATT&CK technique auto-detection | Planned |
