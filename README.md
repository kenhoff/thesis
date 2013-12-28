Senior Thesis
========================

This is the entirety of the code written for my Senior Thesis, completed Fall 2013. It's documented here for official purposes, as well as for anyone who's interested in the implementation.

It's a little bit of a mess - that's what happens when you're up against a deadline! If you'd like to find out more, feel free to reach out to me at thekenhoff@gmail.com.

Abstract
--------------

Existing educational games lack the combination of education and engagement. The objective of this thesis was to research, synthesize, and test a more effective educational design method. First, an educational game design rubric was synthesized from current literature and existing educational games. Then, players applied this rubric to known educational games. In addition, players completed a quiz on game material that accompanied some of the games, to test if the game had improved their content knowledge or skills.

Amazon's Mechanical Turk was used to find players to complete this survey. It produced a significantly large number of responses at a very small cost. Afterwards, the quizzes were scored and analyzed for statistical significance using a two-tailed t-distribution method. The game design rubric responses were analyzed for consistency using an inter-rater reliability metric.

Only one of the games (The Oregon Trail) had a statistically significant improvement in the quiz scores (~5\%), and only a few of the rubric items placed in the ``Slight Agreement'' category as measured by inter-rater reliability. There are no statistically significant conclusions that can be drawn from this research, but it provides an effective first step for future research using similar content or procedures.


Implementation
------------------
There's two main purposes of this code. The first is to generate the final LaTeX file, including graphs and up-to-date results. The second part loads, retrieves, and analyzes the data.

Just about everything is written in Python, except for the provided Mechanical Turk shell scripts. PyPlot was used for generating all of the graphs.



