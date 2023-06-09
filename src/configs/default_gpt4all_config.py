model = dict(
    model = "ggml-gpt4all-j.bin",
    n_ctx = 512,
    n_parts = -1,
    seed = -1,
    f16_kv = False,
    logits_all = False,
    vocab_only = False,
    use_mlock = False,
    embedding = False,
    n_threads = 4,
    n_predict = 1000,
    temp = 0.8,
    top_p = 0.95,
    top_k = 40,
    echo = False,
    stop = [],
    repeat_last_n = 64,
    repeat_penalty = 1.3,
    n_batch = 2,
    streaming = False,
    context_erase = 0.5
)

