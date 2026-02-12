---
title: "How I work with AI"
icon: "puzzle"
---

I don't write code anymore. AI writes the code — and AI should, because AI will maintain it. My job is to design, architect, and know what to ask for.

I learned this the hard way. My first AI project, I forced it to write clean, manageable code — code I'd never actually read. That was wrong. If AI is the one reading and writing the code, why force it to write for a human audience? Now I give AI full control over implementation. I focus on the outcome: does the product work? Do the tests pass? Is the architecture sound?

What 20 years of experience gives you isn't memorized APIs — I couldn't write an Elasticsearch query from memory, even though I built production infrastructure on it. What experience gives you is **knowing how software behaves**. Recognizing when AI takes a shortcut that'll break in production. Knowing that a design decision made today will cause problems six months from now. Asking the right follow-up question because you've seen how systems fail.

AI has the syntax and the breadth of knowledge. I have the judgment and the pattern recognition. We work as equals — I design, I push back, I ask hard questions. AI implements, proposes alternatives, and catches things I'd miss. Speed doesn't matter. Correctness does. Hours of discussion are worth more than minutes of wrong implementation.

The other thing that matters: tell AI the big picture. When I told AI that NN-RAG's core would become a language-agnostic library, it started making different decisions — separating Croatian-specific features from the generic RAG engine. AI can't think ahead unless you give it the long-term vision.

And working software comes first. Get something testable as fast as possible, even if it's rough. NN-RAG runs as a systemd service instead of a Kubernetes pod — not because that's the right architecture, but because it was faster to deploy and iterate on. The important part: that trade-off is documented. What needs to change for production is written down. You can refactor anything once it works, but spending weeks on perfect architecture for something that doesn't solve the problem yet is wasted time.

*There is no instant software. It's a growing, changing thing that takes time to understand what you actually want.*
