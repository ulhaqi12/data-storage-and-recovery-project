import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

from urls import insert_url_entry, get_url_table_as_dataframe, scrape_all_urls
from superfluous import insert_word_into_superfluous, get_superfluous_words_as_dataframe
from keywords import (split_and_store_keywords, get_keywords_as_dataframe,
                      remove_superfluous_words_from_keywords, update_keywords_from_changes_table)
from changes import insert_changes_into_table, get_changes_table_as_dataframe


st.set_page_config(page_title="Storage Project", layout="wide")
st.header("Storage and Data Recovery Project")


url, superfluous, changes, keywords, report, xml, json, csv = st.tabs(["URL", "Superfluous", "Changes", "Keywords",
                                                                       "Report", "XML", "JSON", "CSV/XLS"])


with url:
    col1, col2 = st.columns(2)
    with col1:
        scrape_button = st.button("Scrape")

        if scrape_button:
            scrape_all_urls()

    with col2:

        split_button = st.button("Split")

        if split_button:
            split_and_store_keywords()

    with st.form("New URL"):
        url = st.text_input("Add New URL")
        submitted = st.form_submit_button("Add Url")

    with st.form("Superfluous Word"):
        superfluous_word = st.text_input("Add superfluous word")
        submitted_super = st.form_submit_button("Add Word")

    if submitted:
        insert_url_entry(url=url)

    if submitted_super:
        insert_word_into_superfluous(word=superfluous_word)

    st.header("URL Table")
    url_df = get_url_table_as_dataframe()
    st.dataframe(url_df, width=1000)


with superfluous:
    with st.form("Superfluous Word2"):
        superfluous_word = st.text_input("Add superfluous word")
        submitted_super2 = st.form_submit_button("Add Word")

    if submitted_super2:
        insert_word_into_superfluous(word=superfluous_word)

    superfluous_df = get_superfluous_words_as_dataframe()
    st.dataframe(superfluous_df, width=500)


with keywords:
    clean_button = st.button("Clean")

    if clean_button:
        remove_superfluous_words_from_keywords()
        update_keywords_from_changes_table()

    with st.form("Keywords"):
        col1, col2 = st.columns(2)
        with col1:
            old_keyword = st.text_input("Old Keyword")
        with col2:
            new_keyword = st.text_input("New Keyword")
        changes_submitted = st.form_submit_button("Insert")

    if changes_submitted:
        insert_changes_into_table(old_keyword=old_keyword, new_keyword=new_keyword)

    with st.form("Superfluous Word3"):
        superfluous_word = st.text_input("Add superfluous word")
        submitted_super3 = st.form_submit_button("Add Word")

    if submitted_super3:
        insert_word_into_superfluous(word=superfluous_word)

    keyword_df = get_keywords_as_dataframe()
    st.dataframe(keyword_df, width=500)

with changes:
    changes_df = get_changes_table_as_dataframe()
    st.dataframe(changes_df, width=500)


with report:
    keyword_df_report = get_keywords_as_dataframe()
    st.set_option('deprecation.showPyplotGlobalUse', False)
    plt.figure(figsize=(20, 6))
    sns.barplot(x="keyword", y="occurrence", data=keyword_df_report, palette="viridis")
    plt.xlabel("Keyword")
    plt.ylabel("Occurrences")
    plt.title("Keyword Occurrences")
    plt.xticks(rotation=45, ha="right")
    st.pyplot()