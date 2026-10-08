#!/usr/bin/env python3
"""
Security Awareness Training Evaluator
======================================
Evaluates the quality of security awareness training questions and scenarios
against a structured rubric based on learning design and cybersecurity best practice.

Usage:
    python evaluator.py

Enter one question at a time. The tool scores each question and gives
specific feedback. At the end it produces an overall report for the full quiz.

Built by Tessa Angelika Mmaitsi — github.com/Tessangelika
"""

from datetime import date


# ---------------------------------------------------------------------------
# Rubric criteria
# Each criterion has a name, description, keywords/signals to look for,
# and a weight (all equal for now — 1 point each).
# ---------------------------------------------------------------------------

CRITERIA = [
    {
        "id": "scenario",
        "name": "Has a realistic scenario",
        "description": "The question includes a concrete situation or context, not just a bare question.",
        "signals": [
            "you receive", "you are", "it is", "your colleague", "an email",
            "a message", "you notice", "you find", "someone", "your manager",
            "you get", "imagine", "scenario", "situation", "context",
            "monday morning", "friday afternoon", "at work", "at a conference",
            "while working", "your ceo", "your boss", "a link", "a usb",
            "a phone call", "a text", "whatsapp", "you click", "you open"
        ],
        "weight": 1
    },
    {
        "id": "recognition",
        "name": "Tests recognition, not just recall",
        "description": "The question asks the learner to identify or respond to an attack signal, not just name a definition.",
        "signals": [
            "what should you do", "what do you do", "what is the safest",
            "which response", "how should you respond", "what is your",
            "what would you", "what is the best", "what is the correct",
            "what action", "how do you", "which of the following",
            "what is the most appropriate", "what is the right"
        ],
        "weight": 1
    },
    {
        "id": "correct_answer",
        "name": "Has a correct answer",
        "description": "One answer is clearly correct and is marked or identifiable.",
        "signals": [
            "correct:", "answer:", "right answer", "correct answer",
            "the answer is", "correct option", "(correct)", "[correct]",
            "answer key", "c)", "b)", "a)", "d)", "option a", "option b",
            "option c", "option d"
        ],
        "weight": 1
    },
    {
        "id": "explanation",
        "name": "Explains why the answer is correct",
        "description": "The question or its notes include an explanation of the reasoning behind the correct answer.",
        "signals": [
            "because", "this is", "the reason", "explanation:", "why:",
            "feedback:", "this works by", "attackers", "this technique",
            "social engineering", "verify", "this is correct because",
            "the correct response", "this matters", "the risk here",
            "this is a sign", "this is how"
        ],
        "weight": 1
    },
    {
        "id": "wrong_feedback",
        "name": "Gives feedback on wrong answers",
        "description": "The question or its notes explain why the incorrect options are wrong.",
        "signals": [
            "incorrect:", "wrong because", "this is not", "avoid",
            "do not", "don't", "this would", "this could",
            "this is risky", "this still", "this leaves", "not safe",
            "still exposes", "the problem with", "why not"
        ],
        "weight": 1
    },
    {
        "id": "attack_type",
        "name": "Maps to a recognisable attack type",
        "description": "The scenario relates to a known threat category (phishing, social engineering, malware, etc.).",
        "signals": [
            "phishing", "spear phishing", "vishing", "smishing",
            "social engineering", "malware", "ransomware", "bec",
            "business email compromise", "brute force", "credential",
            "usb", "baiting", "pretexting", "impersonation",
            "man in the middle", "evil twin", "wi-fi", "wifi",
            "password", "2fa", "mfa", "multi-factor", "spoofing",
            "whaling", "insider threat", "data breach", "att&ck",
            "mitre", "t1566", "t1110", "t1200", "t1204", "t1557"
        ],
        "weight": 1
    }
]

PASS_THRESHOLD = 4  # out of 6


# ---------------------------------------------------------------------------
# Evaluation logic
# ---------------------------------------------------------------------------

def evaluate_question(text):
    """
    Evaluate a single question against all rubric criteria.

    Args:
        text (str): The full text of the question, including options,
                    correct answer, and any feedback notes.

    Returns:
        dict: {
            "score": int,
            "max_score": int,
            "results": list of {criterion, passed, feedback},
            "passed": bool
        }
    """
    lower = text.lower()
    results = []
    score = 0

    for criterion in CRITERIA:
        matched = any(signal in lower for signal in criterion["signals"])
        if matched:
            score += criterion["weight"]
            results.append({
                "criterion": criterion["name"],
                "passed": True,
                "feedback": "Found."
            })
        else:
            results.append({
                "criterion": criterion["name"],
                "passed": False,
                "feedback": _missing_feedback(criterion["id"])
            })

    return {
        "score": score,
        "max_score": len(CRITERIA),
        "results": results,
        "passed": score >= PASS_THRESHOLD
    }


def _missing_feedback(criterion_id):
    """Return specific improvement guidance for a failed criterion."""
    guidance = {
        "scenario": (
            "Add a concrete situation. Start with context: who is the learner, "
            "what are they doing, what happens? E.g. 'It is Monday morning. "
            "You receive an email from IT asking you to reset your password.'"
        ),
        "recognition": (
            "Reframe the question so the learner has to decide what to do, "
            "not just name a concept. Use: 'What should you do?' or "
            "'What is the safest response?'"
        ),
        "correct_answer": (
            "Make sure one answer is clearly marked as correct — either in "
            "your notes, an answer key, or by labelling it (Correct)."
        ),
        "explanation": (
            "Add an explanation for the correct answer. Tell the learner "
            "WHY it is right, not just THAT it is right. This is what "
            "builds lasting behaviour change."
        ),
        "wrong_feedback": (
            "Explain why the wrong options are wrong. Learners who pick "
            "the wrong answer need to understand their mistake, not just "
            "see that they were wrong."
        ),
        "attack_type": (
            "Connect the scenario to a named threat type (phishing, social "
            "engineering, BEC, brute force, etc.). This gives learners a "
            "mental model they can apply beyond this one question."
        )
    }
    return guidance.get(criterion_id, "Review this criterion.")


# ---------------------------------------------------------------------------
# Report formatting
# ---------------------------------------------------------------------------

def format_question_report(question_number, evaluation):
    """Format a single question's evaluation results as readable text."""
    lines = []
    lines.append(f"\n{'='*60}")
    lines.append(f"  QUESTION {question_number} RESULT")
    lines.append(f"{'='*60}")
    lines.append(
        f"  Score: {evaluation['score']}/{evaluation['max_score']}  |  "
        f"{'PASS' if evaluation['passed'] else 'NEEDS WORK'}"
    )
    lines.append("")

    for result in evaluation["results"]:
        status = "✓" if result["passed"] else "✗"
        lines.append(f"  {status}  {result['criterion']}")
        if not result["passed"]:
            lines.append(f"       → {result['feedback']}")

    return "\n".join(lines)


def format_final_report(all_evaluations, quiz_title="Security Awareness Quiz"):
    """Format a summary report for the full quiz."""
    total_questions = len(all_evaluations)
    passed = sum(1 for e in all_evaluations if e["passed"])
    total_score = sum(e["score"] for e in all_evaluations)
    max_total = sum(e["max_score"] for e in all_evaluations)
    overall_pct = round((total_score / max_total) * 100) if max_total else 0

    # Criterion-level summary
    criterion_pass_counts = {c["id"]: 0 for c in CRITERIA}
    for ev in all_evaluations:
        for result in ev["results"]:
            matched_criterion = next(
                (c for c in CRITERIA if c["name"] == result["criterion"]), None
            )
            if matched_criterion and result["passed"]:
                criterion_pass_counts[matched_criterion["id"]] += 1

    lines = []
    lines.append(f"\n{'='*60}")
    lines.append(f"  FULL QUIZ REPORT — {quiz_title.upper()}")
    lines.append(f"  {date.today().strftime('%d %B %Y')}")
    lines.append(f"{'='*60}")
    lines.append(f"  Questions evaluated:  {total_questions}")
    lines.append(f"  Questions passing:    {passed}/{total_questions}")
    lines.append(f"  Overall quality:      {total_score}/{max_total} ({overall_pct}%)")
    lines.append("")

    if overall_pct >= 80:
        verdict = "Strong. This quiz meets most quality criteria for effective security awareness training."
    elif overall_pct >= 60:
        verdict = "Adequate. Some gaps to address before this quiz is ready to deploy."
    else:
        verdict = "Needs significant revision before deployment. See criterion breakdown below."

    lines.append(f"  Verdict: {verdict}")
    lines.append("")
    lines.append(f"  {'CRITERION':<40} {'PASS RATE'}")
    lines.append(f"  {'-'*50}")

    for criterion in CRITERIA:
        cid = criterion["id"]
        count = criterion_pass_counts[cid]
        pct = round((count / total_questions) * 100) if total_questions else 0
        bar = "#" * (pct // 10) + "-" * (10 - pct // 10)
        lines.append(f"  {criterion['name']:<40} {pct:>3}%  [{bar}]")

    lines.append("")

    # Biggest gaps
    weakest = sorted(
        CRITERIA,
        key=lambda c: criterion_pass_counts[c["id"]]
    )[:2]

    lines.append("  PRIORITY IMPROVEMENTS:")
    for c in weakest:
        count = criterion_pass_counts[c["id"]]
        if count < total_questions:
            lines.append(f"  • {c['name']} ({count}/{total_questions} questions pass this)")
            lines.append(f"    {_missing_feedback(c['id'])}")
            lines.append("")

    lines.append(f"{'='*60}")
    lines.append("  Generated by SAT Evaluator — github.com/Tessangelika/sat-evaluator")
    lines.append(f"{'='*60}\n")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Interactive mode
# ---------------------------------------------------------------------------

def interactive_mode():
    """Run the evaluator interactively."""
    print("\n" + "="*60)
    print("  SECURITY AWARENESS TRAINING EVALUATOR")
    print("  Quality review tool for cybersecurity quiz questions")
    print("="*60)
    print("\n  Paste each question below (including answer options,")
    print("  correct answer, and any feedback notes you have).")
    print("  Press Enter twice when done with each question.\n")

    quiz_title = input("  Quiz or course title (optional): ").strip()
    if not quiz_title:
        quiz_title = "Security Awareness Quiz"

    all_evaluations = []
    question_number = 0

    while True:
        question_number += 1
        print(f"\n  --- Question {question_number} ---")
        print("  Paste question text. Press Enter twice when done.")
        print("  (Type EXIT on a new line to finish and see the full report.)\n")

        lines = []
        while True:
            line = input()
            if line.strip().upper() == "EXIT":
                question_number -= 1
                break
            if line == "" and lines and lines[-1] == "":
                break
            lines.append(line)

        if lines and lines[-1] == "":
            lines = lines[:-1]

        if not lines or (len(lines) == 1 and lines[0].strip().upper() == "EXIT"):
            break

        text = "\n".join(lines)
        if not text.strip():
            question_number -= 1
            break

        evaluation = evaluate_question(text)
        all_evaluations.append(evaluation)
        print(format_question_report(question_number, evaluation))

        if question_number > 0:
            another = input("\n  Add another question? (y/n): ").strip().lower()
            if another != "y":
                break

    if all_evaluations:
        print(format_final_report(all_evaluations, quiz_title))

        save = input("  Save report to file? (y/n): ").strip().lower()
        if save == "y":
            safe_title = quiz_title.replace(" ", "_").lower()
            filename = f"{safe_title}_evaluation_report.txt"
            with open(filename, "w", encoding="utf-8") as f:
                for i, ev in enumerate(all_evaluations, 1):
                    f.write(format_question_report(i, ev))
                    f.write("\n")
                f.write(format_final_report(all_evaluations, quiz_title))
            print(f"\n  Report saved to: {filename}\n")
    else:
        print("\n  No questions evaluated. Exiting.\n")


if __name__ == "__main__":
    interactive_mode()
