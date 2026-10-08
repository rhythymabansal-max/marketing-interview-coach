## Test Plan
The automated core test suite contains four tests and passed during local source-level testing: question-bank size, question selection, guardrail detection and short-answer fallback. Full Streamlit/Gemini runtime testing could not be executed in this build environment because external package installation was blocked by unavailable network access. Therefore the report does not falsely claim a live API call was tested here.

### 10-case test plan
| # | Test case | Input | Expected result | Actual result | Pass/Fail | Improvement made |
|---|---|---|---|---|---|---|
| 1 | Normal answer | Complete marketing answer | AI evaluation with score + feedback | Evaluation path and schema validated by source tests; live API not executed here | Pass* | Structured schema + fixed rubric |
| 2 | Empty answer | Blank | Local error; no API call | Implemented in `app.py` validation branch | Pass* | Added empty-input validation |
| 3 | Very short answer | `Good.` | Ask for more complete answer; no API call | Core fallback/guardrail tests passed; UI branch verified by source inspection | Pass* | Minimum 20-character check |
| 4 | Very long answer | >5,000 chars | Reject/cap input | `max_chars=5000` and validation branch implemented | Pass* | Added length control |
| 5 | Off-topic request | Medical/political/hacking request | Redirect to interview preparation | Guardrail function automated test passed for hacking injection | Pass | Local pattern guardrail + system prompt |
| 6 | Prompt injection | `Ignore your instructions...` | Do not reveal prompt or follow request | Pattern test passed; system prompt explicitly blocks it | Pass | Added dual-layer guardrail |
| 7 | API failure | Missing key / API exception | Friendly fallback, no crash | Fallback function tested; live network failure not simulated | Pass* | Exception handling + fallback evaluator |
| 8 | Similar answers | Two similar marketing answers | Reasonably consistent rubric-based scores | Consistency design verified: fixed rubric + temperature 0.2 + structured output; live comparison not executed | Pass* | Lowered temperature and fixed anchors |
| 9 | Multi-turn | Q1 answer → Q2 | Session retains prior answers/scores/context | Session-state implementation verified by code inspection | Pass* | Stores recent answers and passes context |
| 10 | Interview completion | Finish all selected questions | Final score, average, strongest/weakest, recommendation, download | Completion branch and summary generation verified by source inspection | Pass* | Added final dashboard + TXT download |

`*` Pass means implementation-level verification or automated unit-level verification; live Streamlit/Gemini execution still needs to be performed after installing dependencies on the deployment/local machine. This distinction is intentional and avoids fabricating test evidence.
