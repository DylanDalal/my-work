Undergraduate Research: Department of Psychology
PSY4910
Ongoing

In order to determine whether or not the different properties of addition and multiplication
have an impact on the way the brain solves math problems, I'm writing a number of functions
that analyze responses to a simple prompt: using 'these' numbers and 'these' operators, reach
'this' result.

8/2021:
I started off implementing the commutative properties of multiplication and addition using
an *-ary Expression Tree. These were originally Binary Expression Trees, but I needed to make
some accomodations for parentheses and negatives that required single leaves.

12/2021:
After completing this, I proposed using string logic to implement the decomposition properties
of multiplication and addition. Though it was a much more straightforward process, I quickly
learned about the difficulties of using strings during this section of the project. At this point,
my research mentor and I were able to discuss and decide on what seemed to us to be "deliberate" 
actions by the participants; 5+1 is a clear additive decomposition of 6, yes, but is replacing
6-1 an additive decomposition of 5? What about 6 and 6*1? If we accept that, do we accept 6 and 
6/1? We decided to have multiple columns for all of these different possibilities, but ultimately 
believe that division and multiplication are simply inverse operations that should be counted. 

3/2022:
The last relation I implemented was "multiplication as repeated addition." For example, 4*2 and
2+2+2+2. At this point, I was more comfortable working with Python, but I still insisted on using
lists for this relation- though I definitely shouldn't have. It went more smoothly than the last
one but still had its fair share of problems.

6/2022
Summer delayed me from working on this project very much, but the next step was to analyze the 
prevalence of these properties against participants' scores on a Math Fluency exam. I learned
Pandas and edited the initial data generation function.

10/2022
The current assignment is to compare the results to the results based on chance. This will be
done by comparing participant data to participant data taken from an average of 4,000 permutations.
This is done in the new file, `chance_comparison.py`, which- by the way- has some code I'm
actually happy with, as opposed to the entirety of `create_data.py`.
