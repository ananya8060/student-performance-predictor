import streamlit as st
import pandas as pd
import pickle
import plotly.graph_objects as go
st.set_page_config("Student Performance Predictor", "🎓", layout="wide")
USER={"admin":"1234","student":"pass"}
if "logged_in" not in st.session_state: st.session_state.logged_in = False
# --- CSS ---
st.markdown("""
<style>
body,*{font-family:'Segoe UI'}
[data-testid="stAppViewContainer"]{
    background:linear-gradient(135deg,#8b78e6,#b19cd9,#d6a3ff);}
.card,.result{
    background:rgba(255,255,255,0.85);
    padding:25px;border-radius:20px;
    box-shadow:0 8px 30px rgba(0,0,0,0.12);
    backdrop-filter:blur(12px);
    margin-bottom:20px;}
.card h1,.result,label,p,span,h2{color:#000!important;}
.stButton>button{
    background:linear-gradient(90deg,#4ade80,#16a34a);
    color:white!important;border-radius:12px;
    padding:10px 25px;font-weight:600;}
.stButton>button:hover{transform:scale(1.05)}
/* ---- BLACK SLIDER FIX ---- */
[data-baseweb="slider"] div[role="slider"] {background:#000!important;}
[data-baseweb="slider"] div[data-testid="stTickBar"] div {background:#000!important;}
[data-baseweb="slider"] .css-1ld3jju,
[data-baseweb="slider"] .css-14i8n1p,
[data-baseweb="slider"] .css-1y4p8pa,
[data-baseweb="slider"] .css-1d1z4yc {color:#000!important;}
/* --- Bigger Labels for Numeric + Categorical Items --- */
.css-17eq0hr, label, .stSelectbox label, .stSlider label {
    font-size: 20px !important;
    font-weight: 600 !important;
    color: black !important;}
</style>
""", unsafe_allow_html=True)
# --- LOGIN ---
if not st.session_state.logged_in:
    st.markdown('<div class="card"><h1>🎓 Welcome to Student Performance Predictor</h1></div>',
                 unsafe_allow_html=True)
    st.info("Please login to move further")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")
    if st.button("Login") and USER.get(u) == p: st.session_state.logged_in = True
    st.stop()
# --- MODEL ---
m = pickle.load(open("student_marks_model.pkl","rb"))
# --- FACTORS ---
factors=[("Hours_Studied","⏰","num",0,24,8),("Attendance","📅","num",0,100,50),("Sleep_Hours","😴","num",0,24,8),("Previous_Scores","📊","num",0,100,50),("Physical_Activity","🏃","num",0,10,1),("Tutoring_Sessions","📚","num",0,10,1),("Parental_Involvement","👨‍👩‍👧","cat"),("Access_to_Resources","💻","cat"),("Extracurricular_Activities","🎨","cat"),("Motivation_Level","🔥","cat"),("Internet_Access","🌐","cat"),("Teacher_Quality","👩‍🏫","cat"),("Gender","🚻","cat")
]
options={"Parental_Involvement":["Low","Medium","High"],"Access_to_Resources":["Low","Medium","High"],"Extracurricular_Activities":["Low","Medium","High"],"Motivation_Level":["Low","Medium","High"],"Internet_Access":["Yes","No"],"Teacher_Quality":["Low","Medium","High"],"Gender":["Male","Female"]}
st.markdown('<div class="card"><h1>🎓 Student Performance Predictor</h1></div>',
            unsafe_allow_html=True)
# --- INPUTS ---
data={}
for typ,title in [("num","📊 Numeric Factors"),("cat","🎯 Categorical Factors")]:
    with st.expander("", expanded=True):
        st.markdown(f"<h3>{title}</h3>", unsafe_allow_html=True)
        cols = st.columns(2)
        for i,f in enumerate(factors):
            name,icon,tp,*rest=f
            if tp != typ: continue
            c = cols[i % 2]
            if tp=="num":
                mn,mx,df = rest
                data[name] = c.slider(f"{icon} {name}", mn, mx, df, key=name)
            else:
                data[name] = c.selectbox(f"{icon} {name}", options[name], key=name)
# --- PREDICT ---
if st.button("Predict Score 🚀"):
    score = m.predict(pd.DataFrame([data]))[0]
    st.markdown(f'<div class="result">Predicted Exam Score: <b>{score:.2f}</b></div>',
                unsafe_allow_html=True)
    fig = go.Figure([go.Bar(
        x=["Previous Score","Predicted Score"],
        y=[data["Previous_Scores"],score],
        marker_color=["#60a5fa","#34d399"]
    )])
    fig.update_layout(
        yaxis=dict(range=[0,100]),
        title="📊 Score Comparison",
        plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)
