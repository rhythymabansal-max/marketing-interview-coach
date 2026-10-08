# 25 Likely Viva Questions — Simple PGDM Answers

1. **Why did you choose this use case?**
I chose it because marketing placement interviews are highly practice-oriented. Students need repeated opportunities to answer questions and improve how they communicate.

2. **Why is this an AI application?**
Question selection and validation are rule-based, but the core evaluation of an open-ended candidate answer and generation of personalized feedback is performed by Gemini. That language evaluation is not a fixed lookup table.

3. **Why Gemini?**
It gives us a capable language model through a straightforward Python SDK and supports structured output, which makes the evaluator easier to control.

4. **Why not just use ChatGPT manually?**
A general chatbot can do this with a prompt, but my application packages the workflow: question bank, controls, fixed rubric, validation, scoring, progress and final summary.

5. **What is prompt engineering here?**
It is the design of instructions and context given to the model. I define the persona, scope, rubric, score anchors, output fields and guardrails instead of asking the model to simply “grade this answer.”

6. **Why structured JSON?**
Because the UI needs predictable fields. Structured output reduces the risk of receiving prose when the app expects a score and feedback fields.

7. **What are the six scoring criteria?**
Relevance, accuracy, conceptual understanding, structure, practical application and communication clarity.

8. **Why use temperature 0.2?**
I want useful language generation but relatively stable scoring. A low temperature reduces unnecessary randomness.

9. **What is Streamlit session state?**
It is Streamlit's mechanism for retaining values across reruns for a user's current session. I use it for the question list, current index, answers, evaluations and configuration.

10. **Does the app have a database?**
No. It deliberately does not claim persistent database storage. The current interview exists in Streamlit session state.

11. **Does it use RAG?**
No. The question bank is a local CSV, not a retrieval-augmented generation system.

12. **Does it use fine-tuning?**
No. The model is guided through system and evaluation prompts plus structured output.

13. **What happens if the API fails?**
The exception is caught and the app uses a basic fallback evaluation so it does not crash.

14. **What happens if the API key is missing?**
The app detects that the key is unavailable and uses the fallback evaluation.

15. **How do you protect the API key?**
It is read from `GEMINI_API_KEY` or Streamlit Secrets. It is not hard-coded and `.env`/secrets files are excluded from Git.

16. **How do you handle prompt injection?**
There are local pattern checks for common attacks and a system-level scope instruction telling Gemini not to reveal instructions or follow unrelated requests.

17. **Give an edge case.**
“Good.” is an edge case because it is too short. The app asks the user to provide a more complete answer. An adversarial hacking request is another example and is redirected.

18. **Can the AI hallucinate?**
Yes. It can misunderstand the question or evaluate an answer imperfectly. That is a key limitation and why the tool is positioned as a coaching aid rather than a hiring authority.

19. **What would you not use it for?**
I would not use it for autonomous hiring decisions or other high-stakes judgments.

20. **Who are the competitors?**
Huru and Yoodli are two real competitors in AI interview/roleplay preparation. They are broader and more mature than this academic prototype.

21. **What is your differentiation?**
The prototype is narrowly focused on marketing and sales placements and is intentionally transparent and easy to explain. Its architecture is small enough for a student project.

22. **How would you monetize it?**
I would start with B-school placement-cell partnerships and institutional subscriptions. Individual premium features could include company-specific practice, resume-based questions and voice interviews.

23. **How would you scale it?**
I would add more question domains, languages, company-specific question generation, voice practice, persistent profiles and analytics.

24. **What was the biggest technical challenge?**
Making the AI output reliable enough for an application UI. The solution was a fixed prompt, rubric, structured schema, validation and fallback path.

25. **What would you improve first?**
I would add persistent user history and voice-based interviews, because those would make the product more useful beyond a single practice session.
