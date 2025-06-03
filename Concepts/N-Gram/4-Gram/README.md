## 4 - Gram
This marks the final exercise in my exploration of N-gram models. Over the past few days, I’ve gained a deeper understanding of tokenization and next-word prediction, which has naturally led me to draw connections between traditional N-gram models and more modern approaches like Retrieval-Augmented Generation (RAG).

While N-gram models rely on the statistical likelihood of a token following a sequence of previous tokens, RAG systems instead use semantic similarity to retrieve relevant chunks of text. In essence:

- N-grams use preceding tokens to predict the most likely next token.

- RAG uses a user query to retrieve semantically relevant document chunks, which are then passed to the language model for response generation.

Both approaches operate under an assumption of proximity or correlation:

- In N-grams, a word is likely to follow another based on observed frequency.

- In RAG, a document chunk is likely to contain relevant information for a given question.

# Observations
- Tokenizer Matters: N-gram models struggle with BPE (Byte Pair Encoding) tokenizers, and while a custom whitespace-based tokenizer improves results, it still has limitations—especially when punctuation or morphological variations are involved in a small dataset.

- Grammatical Weaknesses: N-gram models are generally poor at generating grammatically correct sentences. They're best suited for simple information retrieval tasks rather than natural language generation.

- Content Sensitivity: The quality of the generated output is heavily dependent on the corpus. Mixed-topic datasets tend to produce awkward or "funny" outputs, as patterns from unrelated topics get merged inappropriately. In contrast, single-subject corpora produce more coherent results.

- Scope of Use: Even advanced N-gram models (e.g., trigram or 5-gram) are essentially memorization systems rather than understanding-based models. Despite their shortcomings, they remain useful for lightweight systems, educational purposes, and rapid prototyping.