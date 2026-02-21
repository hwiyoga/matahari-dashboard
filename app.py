import streamlit as st
import pandas as pd

st.set_page_config(page_title="MATAHARI Dashboard", layout="wide")

@st.cache_data
def load_data():
    return pd.read_excel("20251217_all_participants.xlsx")

df = load_data()

st.sidebar.title("MATAHARI Data Views")

page = st.sidebar.radio(
    "Go to",
    [
        "All Participants",
        "Qualified Participants",
        "Not Yet Qualified Participants"
    ]
)

st.title("Program Akselerasi MATAHARI")

# Ensure Notes column exists (safe enhancement)
if "Notes" not in df.columns:
    df["Notes"] = ""

# --------- PAGE LOGIC ---------

if page == "All Participants":
    st.subheader("All Participants")

    # --- Aggregation by Ditjen ---
    st.markdown("### Summary by Directorate General (Ditjen)")

    ditjen_summary_all = (
        df
        .groupby("Ditjen")
        .size()
        .reset_index(name="Number of Participants")
        .sort_values("Number of Participants", ascending=False)
    )

    st.dataframe(ditjen_summary_all, use_container_width=True)

    st.markdown("### Distribution of Participants by Ditjen")

    st.bar_chart(
        data=ditjen_summary_all,
        x="Ditjen",
        y="Number of Participants"
    )

    st.markdown("### Detailed Participant List")

    edited_df = st.data_editor(
        df,
        column_config={
            "Notes": st.column_config.TextColumn(
                "Notes",
                width="large",
                help="Internal coordination notes"
            )
        },
        disabled=[col for col in df.columns if col != "Notes"],
        use_container_width=True
    )

    if st.button("Save changes"):
        edited_df.to_excel("participants.xlsx", index=False)
        st.success("Changes saved.")

elif page == "Qualified Participants":
    st.subheader("Qualified Participants (LULUS)")

    qualified_df = df[df["Final Status"] == "LULUS"]

    # --- Aggregation by Ditjen ---
    st.markdown("### Summary by Directorate General (Ditjen)")

    ditjen_summary = (
        qualified_df
        .groupby("Ditjen")
        .size()
        .reset_index(name="Number of Participants")
        .sort_values("Number of Participants", ascending=False)
    )

    st.dataframe(ditjen_summary, use_container_width=True)

# THIS IS BAR CHART

    st.markdown("### Distribution of Qualified Participants by Ditjen")

    st.bar_chart(
    	data=ditjen_summary,
    	x="Ditjen",
    	y="Number of Participants"
    )

    # --- Detailed list ---
    st.markdown("### Detailed List of Qualified Participants")
    st.dataframe(qualified_df, use_container_width=True)

elif page == "Qualified Participants":
    st.subheader("Qualified Participants (LULUS)")

    qualified_df = df[df["Final Status"] == "LULUS"]
    st.dataframe(qualified_df, use_container_width=True)

elif page == "Not Yet Qualified Participants":
    st.subheader("Not Yet Qualified Participants (TIDAK LOLOS, LANJUT ESAI PENDEK)")

    not_qualified_df = df[df["Final Status"] == "TIDAK LOLOS"]
    st.dataframe(not_qualified_df, use_container_width=True)
