import streamlit as st

import os
import hnswlib
import csv

import paddle
from training.ann_util import build_index
from training.data import (
    convert_example_test,
    create_dataloader,
    gen_id2corpus,
    gen_text_file,
)
from training.model import SimCSE

from paddlenlp.data import Pad, Tuple
from paddlenlp.datasets import MapDataset
from paddlenlp.transformers import AutoModel, AutoTokenizer
from paddlenlp.utils.log import logger
from utils import get_sentence

params_path = "model/model_state.pdparams"

paddle.set_device("gpu")
rank = paddle.distributed.get_rank()
if paddle.distributed.get_world_size() > 1:
    paddle.distributed.init_parallel_env()
tokenizer = AutoTokenizer.from_pretrained("rocketqa-zh-base-query-encoder")

pretrained_model = AutoModel.from_pretrained("rocketqa-zh-base-query-encoder")

model = SimCSE(pretrained_model, output_emb_size=256)
model = paddle.DataParallel(model)

# Load pretrained semantic model
if params_path and os.path.isfile(params_path):
    state_dict = paddle.load(params_path)
    model.set_dict(state_dict)
    logger.info("Loaded parameters from %s" % params_path)
else:
    raise ValueError("Please set --params_path with correct pretrained model file")

inner_model = model._layers

final_index = hnswlib.Index(space="ip", dim=256)
final_index.load_index("model/my_index.bin")

tokenizer = AutoTokenizer.from_pretrained("rocketqa-zh-base-query-encoder")

ans_dic = {}
ques_dic = {}
with open("data/qa_pair.csv", mode="r", encoding="utf-8") as file:
    # 使用csv模块创建reader对象
    reader = csv.reader(file)

    # 创建一个空字典
    # ans_dic = {}
    # ques_dic = {}
    i = 0
    # 遍历每一行，将第一列作为key，第二列作为value添加到字典中
    for row in reader:
        ans_dic[i] = row[1]
        ques_dic[i] = row[0]
        i += 1

st.set_page_config(
    page_title="SGenius Chatbot",
)
selected_language = st.sidebar.selectbox("Select a language", ["English", "简体中文"])
a = st.sidebar.button('Introduction')
if a:
    st.sidebar.write('Our project aims to build an intelligent question answering robot using PaddleNLP to answer questions related to living in Singapore and living on campus at the National University of Singapore (NUS).')



# 根据用户选择的语言显示相应的消息
if selected_language == "English":

    question = st.text_input("Enter your question 👇")

    # 使用 Streamlit 的布局功能，创建两个同一行的按钮
    col1, col2 = st.columns(2, gap='large')

    # 设置按钮的宽度与页面一样
    button_width = col1.width
    print(question)
    ans = get_sentence(question, tokenizer, inner_model, final_index, ques_dic, ans_dic)
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
    print(question)
    ans = get_sentence(question, tokenizer, inner_model, final_index, ques_dic, ans_dic)
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

