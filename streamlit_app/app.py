from __future__ import annotations

import io
import os

import pandas as pd
import plotly.express as px
import requests
import streamlit as st

API_BASE = os.getenv("API_BASE_URL", "http://localhost:8000")

st.set_page_config(page_title="NIST CSF Maturity Dashboard", layout="wide")
st.title("NIST CSF Quarterly Maturity Dashboard")

st.sidebar.header("Upload Quarterly Snapshot")
quarter = st.sidebar.text_input("Quarter", value="2025Q1")
upload = st.sidebar.file_uploader("Upload CSV/XLSX", type=["csv", "xlsx", "xls"])
if st.sidebar.button("Submit") and upload and quarter:
    resp = requests.post(
        f"{API_BASE}/upload",
        params={"quarter": quarter},
        files={"file": (upload.name, upload.getvalue(), upload.type or "application/octet-stream")},
        timeout=30,
    )
    if resp.ok:
        st.sidebar.success(resp.json())
    else:
        st.sidebar.error(resp.text)

quarters_resp = requests.get(f"{API_BASE}/quarters", timeout=15)
quarters = quarters_resp.json().get("quarters", []) if quarters_resp.ok else []

if not quarters:
    st.info("No quarterly data yet. Upload a file to start.")
    st.stop()

selected_quarter = st.selectbox("Quarter", quarters, index=len(quarters) - 1)
report_resp = requests.get(f"{API_BASE}/reports/{selected_quarter}", timeout=20)
report = report_resp.json() if report_resp.ok else {}

col1, col2 = st.columns(2)
with col1:
    st.subheader("Function scores")
    function_df = pd.DataFrame(report.get("function", []))
    if not function_df.empty:
        fig = px.bar(function_df, x="function", y="score", color="function")
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(function_df)

with col2:
    st.subheader("Category heatmap")
    category_df = pd.DataFrame(report.get("category", []))
    if not category_df.empty:
        pivot = category_df.pivot(index="function", columns="category", values="score")
        fig = px.imshow(pivot, text_auto=True, aspect="auto", color_continuous_scale="Blues")
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(category_df)

st.subheader("Subcategory details")
st.dataframe(pd.DataFrame(report.get("subcategory", [])))

if len(quarters) >= 2:
    st.subheader("Quarter-over-quarter delta")
    c1, c2 = st.columns(2)
    with c1:
        from_q = st.selectbox("From", quarters, index=max(0, len(quarters) - 2))
    with c2:
        to_q = st.selectbox("To", quarters, index=len(quarters) - 1)

    if from_q != to_q:
        delta_resp = requests.get(f"{API_BASE}/reports/delta", params={"from_quarter": from_q, "to_quarter": to_q}, timeout=20)
        if delta_resp.ok:
            delta = delta_resp.json()
            delta_func_df = pd.DataFrame(delta.get("function", []))
            if not delta_func_df.empty:
                fig = px.bar(delta_func_df, x="function", y="delta", color="delta", color_continuous_scale="RdYlGn")
                st.plotly_chart(fig, use_container_width=True)
                st.dataframe(delta_func_df)

st.subheader("Exports")
exp1, exp2 = st.columns(2)
with exp1:
    if st.button("Download quarter Excel"):
        r = requests.get(f"{API_BASE}/export/excel/{selected_quarter}", timeout=20)
        if r.ok:
            st.download_button("report.xlsx", data=io.BytesIO(r.content), file_name=f"report_{selected_quarter}.xlsx")
with exp2:
    if st.button("Download quarter PDF"):
        r = requests.get(f"{API_BASE}/export/pdf/{selected_quarter}", timeout=20)
        if r.ok:
            st.download_button("report.pdf", data=io.BytesIO(r.content), file_name=f"report_{selected_quarter}.pdf")
