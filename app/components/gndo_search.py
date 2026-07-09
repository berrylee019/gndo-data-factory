import pandas as pd
import streamlit as st


def render_gndo_search(rkg_df):

    st.subheader("GNDO Search")

    ##########################################
    # Chapter
    ##########################################

    chapters = sorted(
        rkg_df["chapter"].dropna().unique()
    )

    selected_chapter = st.selectbox(

        "Select Chapter",

        chapters,

        key="chapter"

    )

    chapter_df = rkg_df[
        rkg_df["chapter"] == selected_chapter
    ]

    ##########################################
    # Search
    ##########################################

    keyword = st.text_input(
        "Search"
    )

    ##########################################
    # Filter
    ##########################################

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

    ##########################################
    # DataFrame
    ##########################################

    st.dataframe(
        result,
        width="stretch"
    )

    ##########################################
    # Row Selection
    ##########################################

    if result.empty:

        return None

    idx = st.selectbox(

        "Select Result",

        result.index,

        format_func=lambda i:
        f"{result.loc[i,'requirement_id']}"

    )

    return result.loc[idx]
