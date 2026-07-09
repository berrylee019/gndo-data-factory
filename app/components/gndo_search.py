import pandas as pd
import streamlit as st


def render_gndo_search(rkg_df):

    st.header("GNDO Search")

    chapters = sorted(
        rkg_df["chapter"].dropna().unique()
    )

    selected_chapter = st.selectbox(
        "Select Chapter",
        chapters,
        key="chapter_selector"
    )

    chapter_df = rkg_df[
        rkg_df["chapter"] == selected_chapter
    ].copy()

    st.caption(
        f"{selected_chapter} : {len(chapter_df)} records"
    )

    keyword = st.text_input(
        "Search GNDO Objects",
        placeholder="예: REQ-CH07-001"
    )

    if keyword:

        result = chapter_df[
            chapter_df.astype(str)
            .apply(
                lambda x:
                x.str.contains(
                    keyword,
                    case=False,
                    na=False
                )
            )
            .any(axis=1)
        ]

    else:

        result = chapter_df

    st.dataframe(
        result,
        width="stretch"
    )

    if result.empty:
        return None

    idx = st.selectbox(
        "Select Result",
        result.index,
        format_func=lambda i:
            f"{result.loc[i,'requirement_id']} | {result.loc[i,'topic']}"
    )

    return result.loc[idx]
