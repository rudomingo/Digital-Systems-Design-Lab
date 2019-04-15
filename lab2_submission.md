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
```
The application ran for 277 cycles on the FPGA board once synthesized. Below are its
resource utilizations:

1. Slice Logic
--------------

+--------------------------------------+-------+-------+-----------+-------+
|               Site Type              |  Used | Fixed | Available | Util% |
+--------------------------------------+-------+-------+-----------+-------+
| Slice LUTs                           | 15337 |     0 |    218600 |  7.02 |
|   LUT as Logic                       |  9947 |     0 |    218600 |  4.55 |
|   LUT as Memory                      |  2187 |     0 |     70400 |  3.11 |
|     LUT as Distributed RAM           |   856 |     0 |           |       |
|     LUT as Shift Register            |  1331 |     0 |           |       |
|   LUT used exclusively as pack-thrus |  3203 |     0 |    218600 |  1.47 |
| Slice Registers                      | 17575 |     0 |    437200 |  4.02 |
|   Register as Flip Flop              | 17575 |     0 |    437200 |  4.02 |
|   Register as Latch                  |     0 |     0 |    437200 |  0.00 |
|   Register as pack-thrus             |     0 |     0 |    437200 |  0.00 |
| F7 Muxes                             |   547 |     0 |    109300 |  0.50 |
| F8 Muxes                             |     4 |     0 |     54650 | <0.01 |
+--------------------------------------+-------+-------+-----------+-------+

2. Slice Logic Distribution
---------------------------

+-------------------------------------------+------+-------+-----------+-------+
|                 Site Type                 | Used | Fixed | Available | Util% |
+-------------------------------------------+------+-------+-----------+-------+
| Slice                                     | 5751 |     0 |     54650 | 10.52 |
|   SLICEL                                  | 3681 |     0 |           |       |
|   SLICEM                                  | 2070 |     0 |           |       |
| LUT as Logic                              | 9947 |     0 |    218600 |  4.55 |
|   using O5 output only                    |    0 |       |           |       |
|   using O6 output only                    | 8027 |       |           |       |
|   using O5 and O6                         | 1920 |       |           |       |
| LUT as Memory                             | 2187 |     0 |     70400 |  3.11 |
|   LUT as Distributed RAM                  |  856 |     0 |           |       |
|     using O5 output only                  |    0 |       |           |       |
|     using O6 output only                  |    8 |       |           |       |
|     using O5 and O6                       |  848 |       |           |       |
|   LUT as Shift Register                   | 1331 |     0 |           |       |
|     using O5 output only                  |   34 |       |           |       |
|     using O6 output only                  | 1293 |       |           |       |
|     using O5 and O6                       |    4 |       |           |       |
| LUT used exclusively as pack-thrus        | 3203 |     0 |    218600 |  1.47 |
|   Number with same-slice carry load       | 1932 |       |           |       |
|   Number with same-slice register load    | 1408 |       |           |       |
|   Number with same-slice other load       |    0 |       |           |       |
| LUT Flip Flop Pairs                       | 5512 |     0 |    218600 |  2.52 |
|   fully used LUT-FF pairs                 | 1731 |       |           |       |
|   LUT-FF pairs with one unused LUT output | 3385 |       |           |       |
|   LUT-FF pairs with one unused Flip Flop  | 3137 |       |           |       |
| Unique Control Sets                       |  720 |       |           |       |
+-------------------------------------------+------+-------+-----------+-------+

3. Memory
---------

+-------------------+------+-------+-----------+-------+
|     Site Type     | Used | Fixed | Available | Util% |
+-------------------+------+-------+-----------+-------+
| Block RAM Tile    |  1.5 |     0 |       545 |  0.28 |
|   RAMB36/FIFO*    |    1 |     0 |       545 |  0.18 |
|     RAMB36E1 only |    1 |       |           |       |
|   RAMB18          |    1 |     0 |      1090 |  0.09 |
|     RAMB18E1 only |    1 |       |           |       |
+-------------------+------+-------+-----------+-------+
```

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

@spatial object Lab2Part4LUT extends SpatialApp {

  def main(args: Array[String]): Unit = {
    type T = Int
    val M = 3
    val N = 3

    val in = ArgIn[T]
    val out = ArgOut[T]
    val i = ArgIn[T]
    val j = ArgIn[T]

    val input = args(0).to[T]
    val ind_i = args(1).to[T]
    val ind_j = args(2).to[T]

    setArg(in, input)
    setArg(i, ind_i)
    setArg(j, ind_j)

    Accel {
      val lut = LUT[T](M, N)(1.to[T], 2.to[T], 3.to[T], 4.to[T],
                            5.to[T], 6.to[T], 7.to[T], 8.to[T], 9.to[T])
      val lut_value = lut(i, j)
      out := lut_value + in
    }

    val result = getArg(out)
    val goldArray = Array.tabulate(M * N){ i => i + 1 }
    val gold = input + goldArray(i*N + j)
    val pass = gold == result
    println("PASS: " + pass + "(Lab2Part4LUT)")
  }
}


## Part 4
* In every iteration of the innermost Foreach, we bring in two SRAMs of data.
From the animation, you should have seen how we use the two SRAMs to populate a
third one, and then write it back to Matrix C. In the comment session, please
implement this design. As a little hint, you should first think of the proper
controller to use. We would first populate an SRAM using tileB_sram and
tileC_sram. Then we would coalesce the result numel_k times. You can add your implementation to Lab2Part5GEMM.
Please also attach your implementation in the report:
```scala
//GEMM
@spatial object Lab2Part5GEMM extends SpatialApp {

  def main(args: Array[String]): Unit = {
    val outerPar = 1
    val midPar = 2
    val innerPar = 2

    type T = FixPt[TRUE,_24,_8]
    val tileM = 16
    val tileN = 16
    val tileK = 16
    val single = 1

    val M = ArgIn[Int]
    val N = ArgIn[Int]
    val K = ArgIn[Int]
    setArg(M,args(0).to[Int])
    setArg(N,args(1).to[Int])
    setArg(K,args(2).to[Int])

    val a_data = (0::args(0).to[Int], 0::args(2).to[Int]){(i,j) => random[T](3)}
    val b_data = (0::args(2).to[Int], 0::args(1).to[Int]){(i,j) => random[T](3)}
    val c_init = (0::args(0).to[Int], 0::args(1).to[Int]){(i,j) => 0.to[T]}
    val a = DRAM[T](M, K)
    val b = DRAM[T](K, N)
    val c = DRAM[T](M, N)

    setMem(a, a_data)
    setMem(b, b_data)
    setMem(c, c_init)

    Accel {
      Foreach(K by tileK par outerPar){kk =>
        val numel_k = min(tileK.to[Int], K - kk)
        Foreach(M by tileM par innerPar){mm =>
          val numel_m = min(tileM.to[Int], M - mm)
          val tileA_sram = SRAM[T](tileM, tileK)
          tileA_sram load a(mm::mm+numel_m, kk::kk+numel_k)
          Foreach(N by tileN par innerPar){nn =>
            val numel_n = min(tileN.to[Int], N - nn)
            val tileB_sram = SRAM[T](tileK, tileN)
            val tileC_sram = SRAM[T](tileM, tileN).buffer
            tileB_sram load b(kk::kk+numel_k, nn::nn+numel_n)
            tileC_sram load c(mm::mm+numel_m, nn::nn+numel_n)

            MemFold(tileC_sram)(numel_k by 1 par outerPar) { k=>
              val result = SRAM[T](tileM, tileN)
              Foreach(numel_m by 1 par innerPar) { m =>
                Foreach(numel_n by 1 par innerPar) { n =>
                  result(m,n) = tileA_sram(m,k) * tileB_sram(k,n)
                }
              }
              result
            }{_+_}

            c(mm::mm+numel_m, nn::nn+numel_n) store tileC_sram
          }
        }
      }
    }

    val accel_matrix = getMatrix(c)
    val gold_matrix = (0::args(0).to[Int], 0::args(1).to[Int]){(i,j) =>
      Array.tabulate(args(2).to[Int]){k => a_data(i,k) * b_data(k,j)}.reduce{_+_}
    }

    printMatrix(accel_matrix, "Received: ")
    printMatrix(gold_matrix, "Wanted: ")
    val cksum = accel_matrix.zip(gold_matrix){_==_}.reduce{_&&_}
    println("PASS: " + cksum + "(Lab2Part5GEMM)")
  }
}
```

## Part 5: Extra Credits (5 points out of 100)
* In lecture, we covered about how to tune the parallelization factors of controllers to improve the performance of dot product. Can you do the same for GEMM? What is the fewest number of cycles you can achieve? What is the resource utilization? What is your reasoning on choosing your embedded memory size and parallelization factors? 
```scala
Our original implementation of GEMM, shown above, ran for 20617 cycles on the FPGA. 
```
