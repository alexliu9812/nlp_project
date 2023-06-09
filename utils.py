import os
import hnswlib
import paddle
from training.ann_util import build_index
from training.data import (
    convert_example_test,
    create_dataloader,
    gen_id2corpus,
    gen_text_file,
)
from training.model import SimCSE
import csv

from paddlenlp.data import Pad, Tuple
from paddlenlp.datasets import MapDataset
from paddlenlp.transformers import AutoModel, AutoTokenizer
from paddlenlp.utils.log import logger


def get_sentence(sentence, tokenizer, inner_model, final_index, ques_dic, ans_dic):
    encoded_inputs = tokenizer(text=[sentence], max_seq_len=128)
    input_ids = encoded_inputs["input_ids"]
    token_type_ids = encoded_inputs["token_type_ids"]
    input_ids = paddle.to_tensor(input_ids, dtype="int64")
    token_type_ids = paddle.to_tensor(token_type_ids, dtype="int64")
    cls_embedding = inner_model.get_pooled_embedding(
        input_ids=input_ids, token_type_ids=token_type_ids
    )
    # print('提取特征:{}'.format(cls_embedding))
    recalled_idx, cosine_sims = final_index.knn_query(cls_embedding.numpy(), 5)
    ans = []
    for doc_idx, cosine_sim in zip(recalled_idx[0], cosine_sims[0]):
        # print(doc_idx)
        ans.append([ques_dic[doc_idx], ans_dic[doc_idx], 1.0 - cosine_sim])
    return ans
# print(my_dict)

# params_path = "model/model_state.pdparams"

# paddle.set_device("cpu")
# rank = paddle.distributed.get_rank()
# if paddle.distributed.get_world_size() > 1:
#     paddle.distributed.init_parallel_env()
# tokenizer = AutoTokenizer.from_pretrained("rocketqa-zh-base-query-encoder")

# pretrained_model = AutoModel.from_pretrained("rocketqa-zh-base-query-encoder")

# model = SimCSE(pretrained_model, output_emb_size=256)
# model = paddle.DataParallel(model)

# # Load pretrained semantic model
# if params_path and os.path.isfile(params_path):
#     state_dict = paddle.load(params_path)
#     model.set_dict(state_dict)
#     logger.info("Loaded parameters from %s" % params_path)
# else:
#     raise ValueError("Please set --params_path with correct pretrained model file")

# inner_model = model._layers

# final_index = hnswlib.Index(space="ip", dim=256)
# final_index.load_index("model/my_index.bin")
# ans_dic = {}
# ques_dic = {}

# with open("data/qa_pair.csv", mode="r", encoding="utf-8") as file:
#     # 使用csv模块创建reader对象
#     reader = csv.reader(file)

#     # 创建一个空字典
#     i = 0
#     # 遍历每一行，将第一列作为key，第二列作为value添加到字典中
#     for row in reader:
#         ans_dic[i] = row[1]
#         ques_dic[i] = row[0]
#         i += 1

# results = get_sentence("新加坡怎么找房子？", inner_model, final_index, ques_dic, ans_dic)
# print(results)
