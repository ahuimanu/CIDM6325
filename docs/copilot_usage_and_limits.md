# COPILOT IN THIS COURSE (WHAT TO DO IF YOU HIT LIMITS)

1) What “rate-limited” means
- GitHub temporarily caps Copilot traffic to keep the service fair for everyone. You may see “rate limited” errors; these typically clear after a short wait.
- Action: wait 1–3 minutes and retry OR switch to an included model (GPT‑4.1 or GPT‑4o on paid plans).
- Review available models, provisions, and limitations here: [Supported AI models in GitHub Copilot](https://docs.github.com/en/copilot/reference/ai-models/supported-models)

2) Models & premium requests (budgeted usage)
- Some models are “included”; others consume “premium requests.”
- Typical multipliers (subject to change): o4‑mini ~0.33×; o3 ~1×; Claude Sonnet ~1×; Claude Opus 4 ~10×.
- Recommendation: day‑to‑day work → GPT‑4o or o4‑mini; deep reasoning bursts → o3 or Claude Sonnet.
- Keep in mind that free models are more than capable for anything we are doing on the order of Matt's book.

3) Practical tips when limits trigger mid‑exercise
- In VS Code Copilot Chat: click the model pill → pick GPT‑4o or o4‑mini.
- Keep prompts tight; avoid rapid-fire re‑prompts.
- If a heavy session is planned, start on an “included” model.
- The ADRs and Briefs should help keep things focused.

4) Where to see usage
- VS Code shows Copilot usage and plan allowances; if you’re out of premium requests, switch to an included model for the rest of the month.
- If you are not paying, you'll need to make do with free provisions.  Even a little bit of lift from built-in models is a massive productivity improvement.

5) Course expectations
- You may use Copilot - I've clearly encouraged it. As you do, cite it when it substantially contributes to code or text.
- If Copilot is unavailable, proceed manually; do not stall on “waiting for limits.”

## VS CODE: CLEAR RATE-LIMIT ROADBLOCK IN <30s

1) Open Copilot Chat sidebar.
2) Click model name (top of chat).
3) Choose: GPT‑4o (included) or o4‑mini (low multiplier).
4) Retry your prompt; if still limited, wait 60–120 seconds and retry.

## FAQ
Q: Why am I hitting limits?
A: Shared demand + premium model multipliers. Included models aren’t charged on paid plans but can still be momentarily rate-limited during peaks.

Q: Which default models are recommended?
A: For basic work: GPT‑4o (included) or GPT-4.1 (included). For tougher reasoning: GPT-5, o3, or Claude Sonnet (watch the 1× multiplier - these are unavailable at free).

Q: Where are the official docs?
A:
- [Rate limits overview (what to do if limited)](https://docs.github.com/en/copilot/concepts/rate-limits?utm_source=chatgpt.com)
- [“Requests” & premium request allowances per plan](https://docs.github.com/en/copilot/concepts/billing/copilot-requests?utm_source=chatgpt.com)
- [Model list + multipliers + where auto‑selection applies (VS Code)](https://docs.github.com/en/enterprise-cloud@latest/copilot/reference/ai-models/supported-models?utm_source=chatgpt.com)
- [Changelog on premium‑request enforcement/visibility in IDEs](https://github.blog/changelog/2025-05-07-enforcement-of-copilot-premium-request-limits-coming-soon/?utm_source=chatgpt.com)

Rate Limits are a fact of life and most "planned degradation" or "platform decay" [business models](https://link.springer.com/article/10.1007/s10676-025-09846-1) (which are a variation on [Planned Obsolescense](https://en.wikipedia.org/wiki/Planned_obsolescence)) ensure that rate and feature limiting will expand.  As such, get used to curtailed power, paying for more power, of finding the balance (Pareto Principle).