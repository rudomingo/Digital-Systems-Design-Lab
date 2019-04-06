# Laboratory Exercise 2 Submission
Student Name 1: Ron Domingo (rdomingo)

Student Name 2: Michael Lu (mingci7)

## Part 1
* Synthesize the example application. Report on the resource utilization and
cycle counts.

* We also have a MemFold controller, which operates the same way as fold but
work with memories. In this part of the exercise, we would like to reimplement
Lab2Part1SimpleMemReduce using MemFold. You can put your implementation under Lab2Part2SimpleMemFold.
Please also attach your implementation in the report: 
```scala
// Copy-paste your implementation here
```

## Part 2
* Synthesize the example application. Report on the resource utilization and
cycle counts. The example application is stored as Lab2Part3BasicCondFSM.
* Let's try a different example. Here is the description: 

Example: Fill an SRAM of size 32 using the following rules: 
* If the index of the SRAM is smaller than 8
  * Set the element at index to be index
* If the index of the SRAM is within \[8, 16\)
  * Set the element at index to be index * 2
* If the index of the SRAM is within \[16, 24\)
  * Set the element at index to be index * 3
* Otherwise
  * Set the element at index to be index * 4

You can modify Lab2Part3BasicCondFSM to implement this new example. Please save
this new example as Lab2Part3BasicCondFSMAlt. 
```scala
// Copy-paste your implementation here
```

## Part 3
* Please use the LUT syntax to implement the app in Lab2Part4LUT. What we want
to do here is that given a LUT, the user will provide a base value, index i and
index j. The output should be base + LUT(i,j).

## Part 4
* In every iteration of the innermost Foreach, we bring in two SRAMs of data.
From the animation, you should have seen how we use the two SRAMs to populate a
third one, and then write it back to Matrix C. In the comment session, please
implement this design. As a little hint, you should first think of the proper
controller to use. We would first populate an SRAM using tileB_sram and
tileC_sram. Then we would coalesce the result numel_k times. You can add your implementation to Lab2Part5GEMM.
Please also attach your implementation in the report:
```scala
// Copy-paste your implementation here
```

## Part 5: Extra Credits (5 points out of 100)
* In lecture, we covered about how to tune the parallelization factors of controllers to improve the performance of dot product. Can you do the same for GEMM? What is the fewest number of cycles you can achieve? What is the resource utilization? What is your reasoning on choosing your embedded memory size and parallelization factors? 
```scala
// Copy-paste your implementation here
```
