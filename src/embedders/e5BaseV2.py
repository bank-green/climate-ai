import os
import numpy as np

import torch.nn.functional as F

from torch import Tensor, save, load
from transformers import AutoTokenizer, AutoModel

import faiss

dimension = 768


def average_pool(last_hidden_states: Tensor, attention_mask: Tensor) -> Tensor:
    last_hidden = last_hidden_states.masked_fill(~attention_mask[..., None].bool(), 0.0)
    return last_hidden.sum(dim=1) / attention_mask.sum(dim=1)[..., None]


tokenizer = AutoTokenizer.from_pretrained("intfloat/e5-base-v2")
model = AutoModel.from_pretrained("intfloat/e5-base-v2")


def vectorize(chunks):
    input = ["passage: " + c for c in chunks]

    # Tokenize the input texts
    batch_dict = tokenizer(
        input, max_length=512, padding=True, truncation=True, return_tensors="pt"
    )

    outputs = model(**batch_dict)
    embeddings = average_pool(outputs.last_hidden_state, batch_dict["attention_mask"])

    return embeddings.tolist()


def embed_question(question):
    # Tokenize the query
    batch_dict = tokenizer(
        question, max_length=512, padding=True, truncation=True, return_tensors="pt"
    )

    outputs = model(**batch_dict)
    question_embeddings = average_pool(
        outputs.last_hidden_state, batch_dict["attention_mask"]
    )
    return question_embeddings
