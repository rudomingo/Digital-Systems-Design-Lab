# Laboratory Exercise 2 Submission
Student Name 1: Ron Domingo (rdomingo)

Student Name 2: Michael Lu (mingci7)

## Part 1
* Synthesize the example application. Report on the resource utilization and
cycle counts.

```
After synthesizing the application, we saw that it ran for 331 cycles on the FPGA. Below are the resource
utilization information that accompanies the implementation.

1. Slice Logic
--------------

+--------------------------------------+-------+-------+-----------+-------+
|               Site Type              |  Used | Fixed | Available | Util% |
+--------------------------------------+-------+-------+-----------+-------+
| Slice LUTs                           | 16106 |     0 |    218600 |  7.37 |
|   LUT as Logic                       | 10532 |     0 |    218600 |  4.82 |
|   LUT as Memory                      |  2194 |     0 |     70400 |  3.12 |
|     LUT as Distributed RAM           |   896 |     0 |           |       |
|     LUT as Shift Register            |  1298 |     0 |           |       |
|   LUT used exclusively as pack-thrus |  3380 |     0 |    218600 |  1.55 |
| Slice Registers                      | 17857 |     0 |    437200 |  4.08 |
|   Register as Flip Flop              | 17857 |     0 |    437200 |  4.08 |
|   Register as Latch                  |     0 |     0 |    437200 |  0.00 |
|   Register as pack-thrus             |     0 |     0 |    437200 |  0.00 |
| F7 Muxes                             |   457 |     0 |    109300 |  0.42 |
| F8 Muxes                             |     1 |     0 |     54650 | <0.01 |
+--------------------------------------+-------+-------+-----------+-------+

2. Slice Logic Distribution
---------------------------

+-------------------------------------------+-------+-------+-----------+-------+
|                 Site Type                 |  Used | Fixed | Available | Util% |
+-------------------------------------------+-------+-------+-----------+-------+
| Slice                                     |  5931 |     0 |     54650 | 10.85 |
|   SLICEL                                  |  3785 |     0 |           |       |
|   SLICEM                                  |  2146 |     0 |           |       |
| LUT as Logic                              | 10532 |     0 |    218600 |  4.82 |
|   using O5 output only                    |     0 |       |           |       |
|   using O6 output only                    |  8524 |       |           |       |
|   using O5 and O6                         |  2008 |       |           |       |
| LUT as Memory                             |  2194 |     0 |     70400 |  3.12 |
|   LUT as Distributed RAM                  |   896 |     0 |           |       |
|     using O5 output only                  |     0 |       |           |       |
|     using O6 output only                  |     8 |       |           |       |
|     using O5 and O6                       |   888 |       |           |       |
|   LUT as Shift Register                   |  1298 |     0 |           |       |
|     using O5 output only                  |     1 |       |           |       |
|     using O6 output only                  |  1293 |       |           |       |
|     using O5 and O6                       |     4 |       |           |       |
| LUT used exclusively as pack-thrus        |  3380 |     0 |    218600 |  1.55 |
|   Number with same-slice carry load       |  2093 |       |           |       |
|   Number with same-slice register load    |  1415 |       |           |       |
|   Number with same-slice other load       |     0 |       |           |       |
| LUT Flip Flop Pairs                       |  5773 |     0 |    218600 |  2.64 |
|   fully used LUT-FF pairs                 |  1752 |       |           |       |
|   LUT-FF pairs with one unused LUT output |  3628 |       |           |       |
|   LUT-FF pairs with one unused Flip Flop  |  3326 |       |           |       |
| Unique Control Sets                       |   735 |       |           |       |
+-------------------------------------------+-------+-------+-----------+-------+

3. Memory
---------

+-------------------+------+-------+-----------+-------+
|     Site Type     | Used | Fixed | Available | Util% |
+-------------------+------+-------+-----------+-------+
| Block RAM Tile    |    1 |     0 |       545 |  0.18 |
|   RAMB36/FIFO*    |    1 |     0 |       545 |  0.18 |
|     RAMB36E1 only |    1 |       |           |       |
|   RAMB18          |    0 |     0 |      1090 |  0.00 |
+-------------------+------+-------+-----------+-------+
```

* We also have a MemFold controller, which operates the same way as fold but
work with memories. In this part of the exercise, we would like to reimplement
Lab2Part1SimpleMemReduce using MemFold. You can put your implementation under Lab2Part2SimpleMemFold.
Please also attach your implementation in the report: 
```scala
// MemFold
@spatial object Lab2Part2SimpleMemFold extends SpatialApp {

  val N = 16.to[Int]

  def main(args: Array[String]): Unit = {
    val initial = args(0).to[Int]
    val x = ArgIn[Int]
    setArg(x, initial)
    val out = DRAM[Int](16)
    Accel {
      val a = SRAM[Int](16)
      Foreach(16 by 1) { k => a(k) = x}
      MemFold(a)(-5 until 5 by 1){i =>
        val tmp = SRAM[Int](16)
        Foreach(16 by 1) { j => tmp(j) = 1}
        tmp
      }{_+_}
      out store a
    }

    val result = getMem(out)
    val gold = Array.tabulate(16){i => 10.to[Int] + initial}
    printArray(gold, "expected: ")
    printArray(result, "result:   ")

    val cksum = gold.zip(result){_==_}.reduce{_&&_}
    println("PASS: " + cksum + " (Lab2Part2SimpleMemFold)")
  }
}
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
// FSM Alt
@spatial object Lab2Part3BasicCondFSMAlt extends SpatialApp { // Regression (Unit) // Args: none

  def main(args: Array[String]): Unit = {
    val dram = DRAM[Int](32)
    Accel {
      val bram = SRAM[Int](32)
      FSM(0)(state => state < 32) { state =>
        if (state < 8) {
          bram(state) = state // 0:7 [0, 1, ... 7]
        } else if (state >= 8 && state < 16) {
          bram(state) = state*2 // 8:15 [16, 18, 20 ... 30]
        } else if (state >= 16 && state < 24) {
          bram(state) = state*3 // 16:24 [48, 51, 54 ... 69]
        } else {
          bram(state) = state*4 // 25:31 [96, 100, 104 ... 124]
        }
      }{state => state + 1}

      dram(0::32) store bram
    }
    val result = getMem(dram)
    val gold = Array[Int](0, 1, 2, 3, 4, 5, 6, 7, 16, 18, 20, 22, 24, 26, 28, 30,
                  48, 51, 54, 57, 60, 63, 66, 69, 96, 100, 104, 108, 112, 116, 120, 124)
    printArray(result, "Result")
    printArray(gold, "Gold")
    val cksum = gold.zip(result){_ == _}.reduce{_&&_}
    println("PASS: " + cksum + " (Lab2Part3BasicCondFSMAlt)")
  }
}
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
