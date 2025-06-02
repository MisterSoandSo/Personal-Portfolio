# 3 - Gram

In this exercise, we extend our previous bigram implementation by building a trigram-based text generator. A significant change in this version is the switch from a Byte-Pair Encoding (BPE) tokenizer to a custom whitespace-based tokenizer that treats entire words as atomic tokens.

The target output I had in mind during development was a coherent segment like this:
```
Yet neither would ever think of being armed. If what Machiavelli said was true in the early 1500s, it is pretty clear that it is not true today. (Definition) All this basically translates into a question of whether a leader should be virtuous. I suppose the definition of virtuous would differ with different people, but I think of it as holding a moral philosophy that you try to live by.
```

## Version 1
In [version 1](3-gram.py), the design philosophy focused on performance and simplicity, taking inspiration from low-level implementations (e.g., C++). This version prioritized runtime speed and memory efficiency. While it successfully generated valid text, its reliance on only the top 35 most frequent combinations meant that many less common, but potentially meaningful, trigrams were ignored. As a result, the generation would often stop abruptly due to a lack of valid continuations.

Sample Output:
```
Enter your words:
Yet neither
Yet neither would ever think of as presumptuous, since in discussing this material I depart radically from the perspective

End of Inquire
```
## Version 2
In [version 2](3-gram-1.py), the focus shifted toward flexibility and statistical integrity. I replaced the fixed-size C-style memory arrays with Python dictionaries, reducing the memory management overhead and improving code readability and maintainability. This version supported a broader and more nuanced set of trigrams, but it sometimes produced repetitive or looping outputs.

Sample Output:
```
Enter your words:
Yet neither
Yet neither would ever be found in the United States in Congress assembled, two-thirds of the United States in Congress assembled, two-thirds of the United States in Congress assembled, two-thirds of the United States in Congress assembled, two-thirds of the United States in Congress assembled, two-thirds of the United States in Congress assembled, two-thirds of the United States in Congress assembled, two-thirds of the United States in Congress assembled, two-thirds of the United States in Congress assembled, two-thirds of the United States in Congress assembled, two-thirds of the United States in Congress assembled, two-thirds of the United States in Congress assembled, two-thirds of

End of Inquire
```
## Best of Both Worlds
In my [final atempt](3-gram-2.py), I aimed to combine the strengths of both previous versions. This hybrid approach improved coherence while minimizing the drawbacks of repetition and abrupt stops. I also introduced trigram-bigram interpolation and a repetition ban mechanism to mitigate the common issue of n-gram loop collapse (e.g., repeated phrases like "United States in Congress assembled").

Sample Output:
```
Enter your words:
Yet neither
Yet neither would ever think of angry and hungry, clothes for the Western democratic tradition he drew on — but of simply being informative by explaining something complex. Machiavelli’s selection from the circumstances that led to abhor and the decisions in the eyes come over those of others. Why certain forms like best-sellerdom. The ending -en is today one of the United States, and to establish a dialogue between you and beasts. I do not always conscious of this painting. What does Lao-tzu think the world of neuroscience. This dialogue—an active, questioning texts that you can show all people perform. The seat

End of Inquire
```
The result was both amusing and insightful—the output often veered into the absurd, but with moments of striking coherence. This version marks a step forward in balancing structure and creativity in generated text.

## Possible Fixes

For future iterations, I plan to explore the following enhancements:

 - `Tune generation temperature`: Adjust temperature settings to better control randomness and strike a balance between coherence and diversity.
 - `Incorporate fourgram interpolation`: Experiment with fourgram models to provide additional context and reduce ambiguity in sequence prediction.
 - `Expand the training corpus`: As seen in Version 2, a limited dataset can lead to hyperfixation on common n-gram patterns. A more diverse and extensive dataset may reduce repetition and improve output variety.