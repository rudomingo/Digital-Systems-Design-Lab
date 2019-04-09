# Laboratory Exercise 1 Submission
Student Name 1: Ron Domingo (rdomingo)

Student Name 2: Michael Lu (mingci7)

## Part 1
Please attach your modified app in the \`\`\`scala session.
Your answer:
```scala
// Register
@spatial object Lab1Part1RegExample extends SpatialApp {

  type T = Int

  def main(args: Array[String]): Unit = {
    val N = args(0).to[T]
    val M = args(1).to[T]
    val L = args(2).to[T]
    val argRegIn0 = ArgIn[T]
    val argRegIn1 = ArgIn[T]
    val argRegIn2 = ArgIn[T]
    setArg(argRegIn0, N)
    setArg(argRegIn1, M)
    setArg(argRegIn2, L)
    val argRegOut = ArgOut[T]

    Accel {
      val argRegIn0Value = argRegIn0.value
      val argRegIn1Value = argRegIn1.value
      val argRegIn2Value = argRegIn2.value
      argRegOut := argRegIn0Value + argRegIn1Value + argRegIn2Value
    }

    val argRegOutResult = getArg(argRegOut)
    println("Result = " + argRegOutResult)

    val gold = M + N + L
    println("Gold = " + gold)
    val cksum = gold == argRegOutResult
    println("PASS = " + cksum + "(Lab1Part1RegExample)")
  }
}
```

### Part 2
* Simulate the app using Scala and VCS simulation. Report on the simulation result. 
```
The app runs in 836 cycles and uses a total of 128 bytes for each reading and writing.
```

* Synthesize the design and run on the FPGA. Report the number of cycles needed for the design. 

* Report the resource utilization of your design. 
```
According to the run.log, our implementation runs in 313 cycles on the FPGA.

1. Slice Logic
--------------

+--------------------------------------+-------+-------+-----------+-------+
|               Site Type              |  Used | Fixed | Available | Util% |
+--------------------------------------+-------+-------+-----------+-------+
| Slice LUTs                           | 20183 |     0 |    218600 |  9.23 |
|   LUT as Logic                       | 13430 |     0 |    218600 |  6.14 |
|   LUT as Memory                      |  3122 |     0 |     70400 |  4.43 |
|     LUT as Distributed RAM           |  1288 |     0 |           |       |
|     LUT as Shift Register            |  1834 |     0 |           |       |
|   LUT used exclusively as pack-thrus |  3631 |     0 |    218600 |  1.66 |
| Slice Registers                      | 21453 |     0 |    437200 |  4.91 |
|   Register as Flip Flop              | 21453 |     0 |    437200 |  4.91 |
|   Register as Latch                  |     0 |     0 |    437200 |  0.00 |
|   Register as pack-thrus             |     0 |     0 |    437200 |  0.00 |
| F7 Muxes                             |   719 |     0 |    109300 |  0.66 |
| F8 Muxes                             |   129 |     0 |     54650 |  0.24 |
+--------------------------------------+-------+-------+-----------+-------+

2. Slice Logic Distribution
---------------------------

+-------------------------------------------+-------+-------+-----------+-------+
|                 Site Type                 |  Used | Fixed | Available | Util% |
+-------------------------------------------+-------+-------+-----------+-------+
| Slice                                     |  7064 |     0 |     54650 | 12.93 |
|   SLICEL                                  |  4601 |     0 |           |       |
|   SLICEM                                  |  2463 |     0 |           |       |
| LUT as Logic                              | 13430 |     0 |    218600 |  6.14 |
|   using O5 output only                    |     0 |       |           |       |
|   using O6 output only                    | 10644 |       |           |       |
|   using O5 and O6                         |  2786 |       |           |       |
| LUT as Memory                             |  3122 |     0 |     70400 |  4.43 |
|   LUT as Distributed RAM                  |  1288 |     0 |           |       |
|     using O5 output only                  |     0 |       |           |       |
|     using O6 output only                  |     8 |       |           |       |
|     using O5 and O6                       |  1280 |       |           |       |
|   LUT as Shift Register                   |  1834 |     0 |           |       |
|     using O5 output only                  |     9 |       |           |       |
|     using O6 output only                  |  1813 |       |           |       |
|     using O5 and O6                       |    12 |       |           |       |
| LUT used exclusively as pack-thrus        |  3631 |     0 |    218600 |  1.66 |
|   Number with same-slice carry load       |  2453 |       |           |       |
|   Number with same-slice register load    |  1320 |       |           |       |
|   Number with same-slice other load       |     0 |       |           |       |
| LUT Flip Flop Pairs                       |  7499 |     0 |    218600 |  3.43 |
|   fully used LUT-FF pairs                 |  2151 |       |           |       |
|   LUT-FF pairs with one unused LUT output |  4900 |       |           |       |
|   LUT-FF pairs with one unused Flip Flop  |  4532 |       |           |       |
| Unique Control Sets                       |   783 |       |           |       |
+-------------------------------------------+-------+-------+-----------+-------+

3. Memory
---------

+-------------------+------+-------+-----------+-------+
|     Site Type     | Used | Fixed | Available | Util% |
+-------------------+------+-------+-----------+-------+
| Block RAM Tile    |    2 |     0 |       545 |  0.37 |
|   RAMB36/FIFO*    |    2 |     0 |       545 |  0.37 |
|     RAMB36E1 only |    2 |       |           |       |
|   RAMB18          |    0 |     0 |      1090 |  0.00 |
+-------------------+------+-------+-----------+-------+

Overall the application has very low resource utilization for both memory and logic as shown through the low percentages.
```


### Part 3
* Reimplement the example in Part 2 using FIFO / FILO. You can leave your implementation under Lab1Part4FIFOExample and Lab1Part5FILOExample. 
Your implementation: 
```scala
// FIFO
@spatial object Lab1Part4FIFOExample extends SpatialApp {
  val N = 32
  type T = Int

  def simpleLoadStore(srcHost: Array[T], value: T) = {
    val tileSize = 16
    val srcFPGA = DRAM[T](N)
    val dstFPGA = DRAM[T](N)
    setMem(srcFPGA, srcHost)

    val x = ArgIn[T]
    setArg(x, value)
    Accel {
      Sequential.Foreach(N by tileSize) { i =>
        val b1 = FIFO[T](tileSize)

        b1 load srcFPGA(i::i+tileSize)

        val b2 = FIFO[T](tileSize)
        Foreach(tileSize by 1) { ii =>
          b2.enq(b1.deq() * x)
        }

        dstFPGA(i::i+tileSize) store b2
      }
    }
    getMem(dstFPGA)
  }

  def main(args: Array[String]): Unit = {
    val arraySize = N
    val value = args(0).to[Int]

    val src = Array.tabulate[Int](arraySize) { i => i % 256 }
    val dst = simpleLoadStore(src, value)

    val gold = src.map { _ * value }

    println("Sent in: ")
    (0 until arraySize) foreach { i => print(gold(i) + " ") }
    println("Got out: ")
    (0 until arraySize) foreach { i => print(dst(i) + " ") }
    println("")

    val cksum = dst.zip(gold){_ == _}.reduce{_&&_}
    println("PASS: " + cksum + "(Lab1Part4FIFOExample)")
  }
}
```

* Run Scala simulation and VCS simulation. Report the results of VCS simulation.
```
The app ran with the same performance compared to the sans FIFO implementation. The simulation ran for 836 cycles and the total read/write bytes is 128.
```

* Synthesize the design and run it on the board. Report the number of cycles for running the design. 

* Check the utilization report. Report the resource utilization of your design.
```

According to the run.log, our implementation ran in 299 cycles on the FPGA board.

1. Slice Logic
--------------

+--------------------------------------+-------+-------+-----------+-------+
|               Site Type              |  Used | Fixed | Available | Util% |
+--------------------------------------+-------+-------+-----------+-------+
| Slice LUTs                           | 20377 |     0 |    218600 |  9.32 |
|   LUT as Logic                       | 13471 |     0 |    218600 |  6.16 |
|   LUT as Memory                      |  3118 |     0 |     70400 |  4.43 |
|     LUT as Distributed RAM           |  1288 |     0 |           |       |
|     LUT as Shift Register            |  1830 |     0 |           |       |
|   LUT used exclusively as pack-thrus |  3788 |     0 |    218600 |  1.73 |
| Slice Registers                      | 21583 |     0 |    437200 |  4.94 |
|   Register as Flip Flop              | 21583 |     0 |    437200 |  4.94 |
|   Register as Latch                  |     0 |     0 |    437200 |  0.00 |
|   Register as pack-thrus             |     0 |     0 |    437200 |  0.00 |
| F7 Muxes                             |   719 |     0 |    109300 |  0.66 |
| F8 Muxes                             |   129 |     0 |     54650 |  0.24 |
+--------------------------------------+-------+-------+-----------+-------+

In comparison with the DRAM/SRAM implementation of the app, the FIFO implementation utilized 0.02% more logic LUTs as well as a slightly higher percentage of registers. 

2. Slice Logic Distribution
---------------------------

+-------------------------------------------+-------+-------+-----------+-------+
|                 Site Type                 |  Used | Fixed | Available | Util% |
+-------------------------------------------+-------+-------+-----------+-------+
| Slice                                     |  7199 |     0 |     54650 | 13.17 |
|   SLICEL                                  |  4590 |     0 |           |       |
|   SLICEM                                  |  2609 |     0 |           |       |
| LUT as Logic                              | 13471 |     0 |    218600 |  6.16 |
|   using O5 output only                    |     0 |       |           |       |
|   using O6 output only                    | 10667 |       |           |       |
|   using O5 and O6                         |  2804 |       |           |       |
| LUT as Memory                             |  3118 |     0 |     70400 |  4.43 |
|   LUT as Distributed RAM                  |  1288 |     0 |           |       |
|     using O5 output only                  |     0 |       |           |       |
|     using O6 output only                  |     8 |       |           |       |
|     using O5 and O6                       |  1280 |       |           |       |
|   LUT as Shift Register                   |  1830 |     0 |           |       |
|     using O5 output only                  |     5 |       |           |       |
|     using O6 output only                  |  1813 |       |           |       |
|     using O5 and O6                       |    12 |       |           |       |
| LUT used exclusively as pack-thrus        |  3788 |     0 |    218600 |  1.73 |
|   Number with same-slice carry load       |  2526 |       |           |       |
|   Number with same-slice register load    |  1426 |       |           |       |
|   Number with same-slice other load       |     0 |       |           |       |
| LUT Flip Flop Pairs                       |  7535 |     0 |    218600 |  3.45 |
|   fully used LUT-FF pairs                 |  2155 |       |           |       |
|   LUT-FF pairs with one unused LUT output |  4942 |       |           |       |
|   LUT-FF pairs with one unused Flip Flop  |  4626 |       |           |       |
| Unique Control Sets                       |   791 |       |           |       |
+-------------------------------------------+-------+-------+-----------+-------+

The greater logic footprint of the FIFO implementation is also displayed here in the logic distribution as this implementation uses slightly greater resources than the SRAM/DRAM counterpart.

3. Memory
---------

+-------------------+------+-------+-----------+-------+
|     Site Type     | Used | Fixed | Available | Util% |
+-------------------+------+-------+-----------+-------+
| Block RAM Tile    |    2 |     0 |       545 |  0.37 |
|   RAMB36/FIFO*    |    2 |     0 |       545 |  0.37 |
|     RAMB36E1 only |    2 |       |           |       |
|   RAMB18          |    0 |     0 |      1090 |  0.00 |
+-------------------+------+-------+-----------+-------+

In terms of memory, both implementations are equivalent.
```


### Part 4
* Use Fold controller to calculate the sum of an element. You can leave your implementation in Lab1Part7FoldExample.  
Your implementation
```scala
// Fold
@spatial object Lab1Part6FoldExample extends SpatialApp {
  val N = 32
  val tileSize = 16
  type T = Int


  def main(args: Array[String]): Unit = {
    val initial = args(0).to[Int]
    val arraySize = N
    val srcFPGA = DRAM[T](N)
    val src = Array.tabulate[Int](arraySize) { i => i % 256 }
    setMem(srcFPGA, src)
    val destArg = ArgOut[T]

    val x = ArgIn[T]
    setArg(x, initial)
    Accel {
      val accum = Reg[T](0)
      accum := x
      Sequential.Fold(accum)(N by tileSize) { i =>
        val b1 = SRAM[T](tileSize)
        b1 load srcFPGA(i::i+tileSize)
        Reduce(0)(tileSize by 1) { ii => b1(ii) }{_+_}
      }{_+_}


      destArg := accum.value
    }

    val result = getArg(destArg)
    val gold = src.reduce{_+_} + initial
    println("Gold: " + gold)
    println("Result: : " + result)
    println("")

    val cksum = gold == result
    println("PASS: " + cksum + "(Lab1Part6FoldExample)")
  }
}
```

### Part 5
* Please tell us what works and what doesn't for this lab:

Overall, the instructions and assignments were rather straightforward, so we didn't encounter too much
difficulty going through the steps and using the tools. For things that were not explicitly given to
us in the lab handout, it did take some digging through of the Spatial documentation, and it was not
completely clear how the various commands were implemented, though the lecture on Monday provided 
clarification on any remaining questions we had on Spatial syntax.
