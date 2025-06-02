# 2 - Gram

In this [exercise](2-gram.py), we implemented bigrams for a tokenized dataset to generate tokens based on a user-provided word. To optimize performance, we also saved training checkpoints during the bigram model creation process, avoiding the need to regenerate the bigram every time the code is executed.

## Issue
After completing the bigram model, we tested it with the following sample input:

```
Enter your words:
World
of the first reading of the first reading of the first reading of the first reading of the first reading of the first reading of the first reading of the first reading of the first reading of the first reading of the first reading of the first reading of the first reading of the first reading of the first reading of the first reading of the first reading of the first reading of the first reading of the first reading of the first reading of the first reading of the first reading of the first reading of the first reading of

End of Inquire
```
The result was a repetitive and nonsensical sequence. Instead of generating coherent sentences based on the dataset, the model appeared to fixate on the most frequently occurring phrase, leading to excessive repetition.

## Possible Fixes

To improve the output in future iterations, I plan to:
- Implement a trigram model to provide more context and reduce repetition.
- Introduce controlled randomness or temperature-based sampling during generation to encourage variation and avoid overly deterministic patterns.

These adjustments should help produce more diverse and meaningful text outputs.