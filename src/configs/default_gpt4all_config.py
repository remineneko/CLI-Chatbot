import random

randomized_seed = random.randint(0, 10**15) # I could go from -1, but -1 itself is randomizing.
print(f"Testing on seed {randomized_seed}")

model = dict(
    cache = None, 
    verbose = False, 
    callbacks = None, 
    callback_manager = None,
    model = "ggml-gpt4all-j.bin",
    n_ctx = 512,
    n_parts = -1,
    seed = randomized_seed,
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

