
import io
import os
from datetime import datetime
import pandas as pd
import streamlit as st
from utils.question_manager import load_questions, select_questions, CATEGORIES, DIFFICULTIES, MODES
from utils.evaluator import evaluate_answer

st.set_page_config(page_title="Marketing Interview Coach AI", page_icon="🎯", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
.block-container {max-width: 1180px; padding-top: 2rem; padding-bottom: 3rem;}
.hero {padding: 1.4rem 1.6rem; border-radius: 18px; background: linear-gradient(135deg, #111827 0%, #1f2937 55%, #334155 100%); color: white; margin-bottom: 1.2rem;}
.hero h1 {margin: 0; font-size: 2.2rem;} .hero p {margin: .35rem 0 0; opacity: .85; font-size: 1.05rem;}
.question-card {padding: 1.2rem 1.4rem; border: 1px solid #e5e7eb; border-radius: 16px; background: #fff; margin: .8rem 0 1rem;}
.feedback-card {padding: 1rem 1.2rem; border-radius: 14px; background: #f8fafc; border: 1px solid #e2e8f0;}
.small {color:#64748b; font-size:.9rem;} .disclaimer {font-size:.78rem; color:#64748b; margin-top:1rem;}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def get_bank(): return load_questions()

def reset_interview():
    for k in ["interview_started","questions","current_idx","answers","evaluations","submitted","finalized","config","run_id"]:
        st.session_state.pop(k, None)

def start_interview(category,difficulty,mode,count):
    df=get_bank(); qs=select_questions(df,category,difficulty,mode,count,seed=int(datetime.now().timestamp())%100000)
    st.session_state.interview_started=True; st.session_state.questions=qs.to_dict("records"); st.session_state.current_idx=0
    st.session_state.answers=[]; st.session_state.evaluations=[]; st.session_state.submitted=False; st.session_state.finalized=False
    st.session_state.config={"category":category,"difficulty":difficulty,"mode":mode,"count":len(qs)}
    st.session_state.run_id=datetime.now().strftime("%Y%m%d%H%M%S")

st.markdown('<div class="hero"><h1>🎯 Marketing Interview Coach AI</h1><p>Practice. Get evaluated. Improve your interview performance.</p></div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("Interview Setup")
    category=st.selectbox("Interview Category",CATEGORIES)
    difficulty=st.selectbox("Difficulty",DIFFICULTIES,index=1)
    mode=st.selectbox("Interview Mode",MODES)
    count=st.number_input("Number of Questions",min_value=3,max_value=10,value=5,step=1)
    c1,c2=st.columns(2)
    if c1.button("Start / Reset",use_container_width=True,type="primary"):
        start_interview(category,difficulty,mode,int(count)); st.rerun()
    if c2.button("Reset",use_container_width=True): reset_interview(); st.rerun()
    st.divider(); st.caption("Built for MBA/PGDM students and freshers preparing for marketing & sales placements.")
    st.info("Privacy: your answer may be sent to Google's Gemini API for evaluation when a GEMINI_API_KEY is configured. Do not enter sensitive personal information.")

if not st.session_state.get("interview_started"):
    st.subheader("Welcome 👋")
    st.write("This AI coach simulates a marketing and sales interview. Choose your category, difficulty and mode from the sidebar, then start practicing.")
    a,b,c=st.columns(3)
    a.metric("Question Bank", f"{len(get_bank())}+ questions")
    b.metric("Evaluation", "0–10 rubric")
    c.metric("Feedback", "Instant + actionable")
    st.markdown("### What you will receive")
    st.markdown("""- Objective score out of 10
- Strengths and missing points
- Improved answer
- One actionable tip
- Final performance summary""")
    st.caption("AI-generated feedback is a coaching aid, not a hiring decision or guarantee.")
    st.stop()

cfg=st.session_state.config; questions=st.session_state.questions; idx=st.session_state.current_idx
st.progress((idx)/len(questions), text=f"Question {min(idx+1,len(questions))} of {len(questions)}")

if idx >= len(questions):
    st.session_state.finalized=True

if st.session_state.finalized:
    st.success("Interview complete!")
    ev=st.session_state.evaluations
    scores=[e["score"] for e in ev if isinstance(e,dict) and isinstance(e.get("score"),int)]
    avg=round(sum(scores)/len(scores),1) if scores else 0
    attempted=len(ev)
    topic_scores={}
    for q,e in zip(questions,ev): topic_scores.setdefault(q["category"],[]).append(e["score"])
    topic_avg={k:round(sum(v)/len(v),1) for k,v in topic_scores.items() if v}
    strongest=max(topic_avg,key=topic_avg.get) if topic_avg else "—"; weakest=min(topic_avg,key=topic_avg.get) if topic_avg else "—"
    performance="Excellent" if avg>=8.5 else "Strong" if avg>=7 else "Developing" if avg>=5 else "Needs improvement"
    st.header("Your Interview Performance")
    x1,x2,x3,x4=st.columns(4); x1.metric("Overall Score",f"{avg}/10"); x2.metric("Questions Attempted",attempted); x3.metric("Strongest Area",strongest); x4.metric("Improvement Area",weakest)
    st.metric("Overall Performance",performance)
    st.markdown("### Recommendations")
    if avg>=8: rec="Maintain your structure, but keep practicing concise examples and role-specific application."
    elif avg>=6: rec=f"Focus on stronger structure and practical examples. Revisit {weakest} and retake a practice round."
    else: rec=f"Build fundamentals first, then practice structured answers. Prioritize {weakest} before increasing difficulty."
    st.write(rec)
    rows=[]
    for i,(q,e) in enumerate(zip(questions,ev),1): rows.append({"Question":i,"Category":q["category"],"Score":e["score"],"Feedback":e["feedback"]})
    report_df=pd.DataFrame(rows)
    st.dataframe(report_df,use_container_width=True,hide_index=True)
    summary = (
        f"Marketing Interview Coach AI\nRun: {st.session_state.run_id}\n"
        f"Mode: {cfg['mode']} | Difficulty: {cfg['difficulty']}\n"
        f"Overall Score: {avg}/10\nQuestions Attempted: {attempted}\n"
        f"Strongest Area: {strongest}\nImprovement Area: {weakest}\n"
        f"Overall Performance: {performance}\n\nRecommendations:\n{rec}\n\nQuestion Results:\n"
        + "\n".join([f"{i}. {q['question']} — {e['score']}/10" for i,(q,e) in enumerate(zip(questions,ev),1)])
    )
    st.download_button("⬇️ Download Performance Summary",summary,file_name=f"interview_summary_{st.session_state.run_id}.txt",mime="text/plain")
    if st.button("Start Another Interview",type="primary"): reset_interview(); st.rerun()
    st.stop()

q=questions[idx]
st.markdown(f'<div class="question-card"><div class="small">{q["category"]} • {q["difficulty"]}</div><h2>{q["question"]}</h2></div>',unsafe_allow_html=True)

if not st.session_state.submitted:
    answer=st.text_area("Your answer",height=190,placeholder="Type your interview answer here…",key=f"answer_{idx}",max_chars=5000)
    if st.button("Submit Answer",type="primary",use_container_width=True):
        cleaned=answer.strip()
        if not cleaned:
            st.error("Please enter an answer before submitting.")
        elif len(cleaned)<20:
            st.warning("Please provide a more complete answer so I can evaluate your response fairly.")
        elif len(cleaned)>5000:
            st.error("Please keep your answer under 5,000 characters.")
        else:
            with st.spinner("Evaluating your answer…"):
                history="\n".join([f"Q: {a['question']}\nA: {a['answer']}\nScore: {a['score']}" for a in st.session_state.answers[-2:]])
                result=evaluate_answer(q["category"],q["difficulty"],q["question"],q["ideal_points"],cleaned,history)
            data=result.data
            st.session_state.answers.append({"question":q["question"],"answer":cleaned,"score":data["score"]})
            st.session_state.evaluations.append(data); st.session_state.submitted=True; st.rerun()
else:
    data=st.session_state.evaluations[-1]
    st.markdown("### AI Evaluation")
    if data["score"]==0 and "outside" in data["feedback"].lower():
        st.warning(data["feedback"])
    else:
        st.metric("Score",f"{data['score']}/10")
        c1,c2=st.columns(2)
        with c1:
            st.markdown("**What you did well**")
            for x in data["strengths"]: st.write(f"• {x}")
        with c2:
            st.markdown("**What was missing**")
            for x in data["missing_points"]: st.write(f"• {x}")
        st.markdown(f'<div class="feedback-card"><b>Feedback</b><br>{data["feedback"]}</div>',unsafe_allow_html=True)
        st.markdown("**Suggested improved answer**")
        st.write(data["improved_answer"])
        st.info(f"💡 Actionable tip: {data['tip']}")
        if st.session_state.evaluations and len(st.session_state.evaluations)>1:
            st.caption("The coach retains the current interview context and recent answer history through Streamlit session state.")
    if idx+1 < len(questions):
        if st.button("Next Question →",type="primary",use_container_width=True):
            st.session_state.current_idx+=1; st.session_state.submitted=False; st.rerun()
    else:
        if st.button("Finish Interview →",type="primary",use_container_width=True):
            st.session_state.current_idx=len(questions); st.session_state.finalized=True; st.rerun()

st.markdown('<div class="disclaimer">AI-generated feedback may be imperfect. Do not use this tool as a hiring, legal, medical, financial, or other high-stakes decision system.</div>',unsafe_allow_html=True)
