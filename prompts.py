# prompts.py
# Stores reusable prompt templates for OpenAI

# can adjust for tone/role
SYSTEM_PROMPT = (
    "You are an operations/project delivery assistant. "
    "You read raw Slack messages and write a client-facing weekly update. "
    "Be concise, outcome-oriented, and professional."
)

#Prompt template (maybe use diff file format so we can edit outside python)
USER_PROMPT_TEMPLATE = """
Here are Slack messages from the last 7 days of a project channel:

---
{channel_text}
---

Using ONLY what is implied by those messages, write a weekly update in 5 sections:

1. Outcomes Delivered (Why It Matters)
   - What was achieved since the last update?
   - Tie work to business impact, not tasks.
   - Include brief metric or validation if available.

2. Progress vs. Plan
   - Narrative (on track / ahead / in motion)
   - Avoid task lists.

3. Risks, Constraints, or Dependencies
   - Possible blockers, scope/timing risks.
   - Mitigation plan.
   - Note if client input/action is required.
   - Keep tone calm, proactive.

4. Next Steps & Required Inputs
   - Next 1-2 delivery steps.
   - Decisions or inputs needed (by when, from whom).

5. Alignment & Communication Check
   - Are scope/cadence still right?
   - Suggest adjustments if helpful.
"""