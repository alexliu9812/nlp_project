import streamlit as st
import pandas as pd
from Introduction import *

selected_language = st.sidebar.selectbox("Select a language", ["English", "简体中文"])

# 根据用户选择的语言显示相应的消息
if selected_language == "English":

    question = st.text_input("Enter your question 👇")

    # 使用 Streamlit 的布局功能，创建两个同一行的按钮
    col1, col2 = st.columns(2, gap='large')

    # 设置按钮的宽度与页面一样
    button_width = col1.width
    ans = get_sentence(question, inner_model, final_index, ques_dic, ans_dic)
    # 在每个列中创建一个按钮
    with col1:
        button1 = st.button("Select the most probable answer")

    with col2:
        button2 = st.button("Possible answers")

    # 使用CSS样式设置按钮的大小

    if question:
        if button1:
            st.markdown('<hr style="border: 1px solid #f0f0f0; width: 100%;">', unsafe_allow_html=True)
            st.markdown('RESULT')
            st.write("The most matching question is:", ans[0][0])
            st.write("The result is:", ans[0][1])
            st.write("The probality is:", ans[0][2])
        if button2:
            st.markdown('Result')
            for i in range(len(ans)):
                st.write("The question ranked %d in terms of matching is:" % (i + 1), ans[i][0])
                st.write("The answer is:", ans[i][1])
                st.write("The probality is:", ans[i][2])
                st.markdown('<hr style="border: 1px solid #f0f0f0; width: 100%;">', unsafe_allow_html=True)
    else:
        if button1 or button2:
            # 警告弹窗
            st.info("Please enter your question")
elif selected_language == "简体中文":

    question = st.text_input("请输入你的问题 👇")

    # 使用 Streamlit 的布局功能，创建两个同一行的按钮
    col1, col2 = st.columns(2, gap='large')

    # 设置按钮的宽度与页面一样
    button_width = col1.width
    ans = get_sentence(question, inner_model, final_index, ques_dic, ans_dic)
    # 在每个列中创建一个按钮
    with col1:
        button1 = st.button("选取最可能的答案")

    with col2:
        button2 = st.button("给出几个可能的答案")

    # 使用CSS样式设置按钮的大小

    if question:
        if button1:
            st.markdown('<hr style="border: 1px solid #f0f0f0; width: 100%;">', unsafe_allow_html=True)
            st.markdown('返回结果')
            st.write("最匹配的问题为", ans[0][0])
            st.write("答案为：", ans[0][1])
            st.write("概率为：", ans[0][2])
        if button2:
            st.markdown('返回结果')
            for i in range(len(ans)):
                st.markdown('<hr style="border: 1px solid #f0f0f0; width: 100%;">', unsafe_allow_html=True)
                st.write("匹配度排名第%d的问题是:" % (i + 1), ans[i][0])
                st.write("答案为：", ans[i][1])
                st.write("概率为：", ans[i][2])
    else:
        if button1 or button2:
            # 警告弹窗
            st.info("请输入您的问题再进行问答")
