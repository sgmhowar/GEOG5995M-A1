# GEOG5995M Assignment 1 - Agent Based Modelling

## Overview

This repository contains all the content created as part of the first assignment in the module 'Programming for Social Science: Core Skills' for the academic year 21/22. (This course, and the files used at several points in the project, can be found at https://www.geog.leeds.ac.uk/courses/computing/study/core-python-phd/). An example of the model generated by the project is shown below:

![Model Example](/images/me.png)

## Model Structure

This model is comprised of three main components:

1. An environment (generated from a course supplied text file, converted for use).

2. 'Sheep' Agents - white dots - agents that roam the environment randomly, collecting data from it and sharing with one another.

3. 'Wolf' Agents - red agents - agents that chase down and 'eat' the sheep, removing them from the model.

Once all of these components are generated by the model it runs until one of two conditions have been met, either:

* All sheep agents have been eaten by wolves
* 100 full iterations have occured (i.e. all active agents have moved and if possible eaten 100 times)

From testing, at the base defined speed of the wolves (5x that of the sheep), the former condition is usually met first. This can be determined by console updates of succesful sheep kills and a concluding message when the final sheep is killed. Reducing the number of wolves or the speed that they move swings this trend however, and the wolves are more likely to be stopped before they can reach all the sheep.

The model is designed to allow for a theoretically limitless number of both sheep and wolves, but practically this is limited by computational power. The numbers of 10 sheep to 2 wolves manages to display all the features of the model sufficiently without slowing down too greatly.

All of this is rendered in a GUI that allows the user to easily begin or halt the model.

## References

Much of the code used is derived from the course content noted above. Available at: https://www.geog.leeds.ac.uk/courses/computing/study/core-python-phd/

