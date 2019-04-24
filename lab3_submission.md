# Laboratory Exercise 3 Submission
Student Name 1: Michael Lu (mingci7)

Student Name 2: Ron Domingo (rdomingo)

## Part 1
Given the two kernels and the input data, perform 2 2-D convolution on the image. You can add your implementation to Lab3Part1Convolution. Report the resource utilization and cycle counts of your design. 
```scala
// Copy-paste your implementation here
```
def convolve(image: Matrix[T]): Matrix[T] = {
    val B = 16

    val R = ArgIn[Int]
    val C = ArgIn[Int]
    setArg(R, image.rows)
    setArg(C, image.cols)
    val lb_par = 8

    val img = DRAM[T](R, C)
    val imgOut = DRAM[T](R, C)

    setMem(img, image)

    Accel {
      val lb = LineBuffer[T](Kh, Cmax)

      val kh = LUT[T](3,3)(1.to[T], 0.to[T], -1.to[T],
                           2.to[T], 0.to[T], -2.to[T],
                           1.to[T], 0.to[T], -1.to[T])
      val kv = LUT[T](3,3)(1.to[T],  2.to[T],  1.to[T],
                           0.to[T],  0.to[T],  0.to[T],
                          -1.to[T], -2.to[T], -1.to[T])

      val sr = RegFile[T](Kh, Kw)
      val lineOut = SRAM[T](Cmax)

      Foreach (0 until R) {r =>
        lb load img(r, 0::C par lb_par)
        Foreach (0 until C) {c =>
          Pipe{sr.reset(c==0)}
          Foreach (0 until Kh) {i => sr(i,*) <<= lb(i,c)}
          val horz = Reduce(Reg[T])(Kh by 1) { i =>
            Reduce(0)(Kw by 1) { j => 
              sr(i,j) * kh(i,j)
            }{_+_}
          }{_+_}
          val vert = Reduce(Reg[T])(Kh by 1) { i =>
            Reduce(0)(Kw by 1) { j => 
              sr(i,j) * kv(i,j)
            }{_+_}
          }{_+_}
          lineOut(c) = mux( r<2 || c<2, 0.to[T], abs(horz.value) + abs(vert.value))
        }
        imgOut(r, 0::C) store lineOut
      }   
    }

    getMatrix(imgOut)
}
```
Our implmentation ran for 25086 cycles on the FPGA with an input of 64x64.

1. Slice Logic
--------------

+--------------------------------------+-------+-------+-----------+-------+
|               Site Type              |  Used | Fixed | Available | Util% |
+--------------------------------------+-------+-------+-----------+-------+
| Slice LUTs                           | 35374 |     0 |    218600 | 16.18 |
|   LUT as Logic                       | 25519 |     0 |    218600 | 11.67 |
|   LUT as Memory                      |  3813 |     0 |     70400 |  5.42 |
|     LUT as Distributed RAM           |  1724 |     0 |           |       |
|     LUT as Shift Register            |  2089 |     0 |           |       |
|   LUT used exclusively as pack-thrus |  6042 |     0 |    218600 |  2.76 |
| Slice Registers                      | 30975 |     0 |    437200 |  7.08 |
|   Register as Flip Flop              | 30975 |     0 |    437200 |  7.08 |
|   Register as Latch                  |     0 |     0 |    437200 |  0.00 |
|   Register as pack-thrus             |     0 |     0 |    437200 |  0.00 |
| F7 Muxes                             |   687 |     0 |    109300 |  0.63 |
| F8 Muxes                             |   128 |     0 |     54650 |  0.23 |
+--------------------------------------+-------+-------+-----------+-------+

2. Slice Logic Distribution
---------------------------

+-------------------------------------------+-------+-------+-----------+-------+
|                 Site Type                 |  Used | Fixed | Available | Util% |
+-------------------------------------------+-------+-------+-----------+-------+
| Slice                                     | 11187 |     0 |     54650 | 20.47 |
|   SLICEL                                  |  7461 |     0 |           |       |
|   SLICEM                                  |  3726 |     0 |           |       |
| LUT as Logic                              | 25519 |     0 |    218600 | 11.67 |
|   using O5 output only                    |     0 |       |           |       |
|   using O6 output only                    | 20772 |       |           |       |
|   using O5 and O6                         |  4747 |       |           |       |
| LUT as Memory                             |  3813 |     0 |     70400 |  5.42 |
|   LUT as Distributed RAM                  |  1724 |     0 |           |       |
|     using O5 output only                  |     0 |       |           |       |
|     using O6 output only                  |     8 |       |           |       |
|     using O5 and O6                       |  1716 |       |           |       |
|   LUT as Shift Register                   |  2089 |     0 |           |       |
|     using O5 output only                  |   240 |       |           |       |
|     using O6 output only                  |  1813 |       |           |       |
|     using O5 and O6                       |    36 |       |           |       |
| LUT used exclusively as pack-thrus        |  6042 |     0 |    218600 |  2.76 |
|   Number with same-slice carry load       |  4335 |       |           |       |
|   Number with same-slice register load    |  1954 |       |           |       |
|   Number with same-slice other load       |     0 |       |           |       |
| LUT Flip Flop Pairs                       | 12162 |     0 |    218600 |  5.56 |
|   fully used LUT-FF pairs                 |  3021 |       |           |       |
|   LUT-FF pairs with one unused LUT output |  8307 |       |           |       |
|   LUT-FF pairs with one unused Flip Flop  |  8145 |       |           |       |
| Unique Control Sets                       |   888 |       |           |       |
+-------------------------------------------+-------+-------+-----------+-------+
* Note: Review the Control Sets Report for more information regarding control sets.


3. Memory
---------

+-------------------+------+-------+-----------+-------+
|     Site Type     | Used | Fixed | Available | Util% |
+-------------------+------+-------+-----------+-------+
| Block RAM Tile    |   10 |     0 |       545 |  1.83 |
|   RAMB36/FIFO*    |   10 |     0 |       545 |  1.83 |
|     RAMB36E1 only |   10 |       |           |       |
|   RAMB18          |    0 |     0 |      1090 |  0.00 |
+-------------------+------+-------+-----------+-------+
```

## Part 2
Write the code that will traverse the matrix from top-left to bottom-right and update each entry of the score matrix.
```scala
// Step 1: Build score matrix
      Foreach(length+1 by 1 par row_par) { r =>
        Foreach(length+1 by 1) { c =>
        val first_col = c<1
        val first_row = r<1
        val top_score = mux(first_row, 0.to[Int16], score_matrix(r-1, c).score + GAP_SCORE)
        val left_score = mux(first_col, 0.to[Int16], score_matrix(r, c-1).score + GAP_SCORE)
        val diag_score = mux(first_row || first_col, 0.to[Int16], 
                          mux(seqa_sram_raw(c) == seqb_sram_raw(r), // Checks if the letter from string A and that from string B match
                            score_matrix(r-1, c-1).score + MATCH_SCORE, score_matrix(r-1, c-1).score + MISMATCH_SCORE))
        val cur_score = mux(first_col || first_row, // Checks if leftmost column/ uppermost row
                          mux(first_col, top_score, left_score), // Leftmost column automatically assigned top_score, uppermost row assigned left_score
                            mux((top_score >= left_score) && (top_score >= diag_score), // Comparisons to find maximum score from three paths
                              top_score, mux((left_score >= top_score) && (left_score >= diag_score),
                                left_score, diag_score)))
        val cur_direction = mux(cur_score == left_score, SKIPB, mux(cur_score == top_score, SKIPA, ALIGN))                           
        val cur = nw_tuple(cur_score.to[Int16], cur_direction.to[Int16])
        score_matrix(r, c) = cur
        }
      }
```

## Part 3
Write the code that can traceback from the bottom-right to the top-left of the score matrix. You can add your implementation in Lab3Part2NW. Report the resource utilization and cycle counts of your NW implementation.
```scala
// Step 2: Reconstruct the path
      val b_addr = Reg[Int](0) // Index of the current position in sequence b
      val a_addr = Reg[Int](0) // Index of the current position in sequence a
      Parallel{b_addr := length; a_addr := length} // Set the position to start from bottom right
      val done_backtrack = Reg[Bit](false) // A flag to tell if traceback is done
      FSM(0)(state => state != doneState) { state =>
        if (state == traverseState) {
          if (score_matrix(b_addr,a_addr).ptr == ALIGN) {
            seqa_fifo_aligned.enq(seqa_sram_raw(a_addr-1), !done_backtrack)
            seqb_fifo_aligned.enq(seqb_sram_raw(b_addr-1), !done_backtrack)
            done_backtrack := a_addr == 1.to[Int] || b_addr == 1.to[Int]
            a_addr :-= 1
            b_addr :-= 1
          } else if (score_matrix(b_addr,a_addr).ptr == SKIPB) {
            seqa_fifo_aligned.enq(seqa_sram_raw(a_addr-1), !done_backtrack)
            seqb_fifo_aligned.enq(dash, !done_backtrack)
            done_backtrack := a_addr == 1.to[Int]
            a_addr :-= 1
          } else {
            seqa_fifo_aligned.enq(dash, !done_backtrack)
            seqb_fifo_aligned.enq(seqb_sram_raw(b_addr-1), !done_backtrack)
            done_backtrack := b_addr == 1.to[Int]
            b_addr :-= 1
          }
        } else if (state == padBothState) {
          seqa_fifo_aligned.enq(underscore, !seqa_fifo_aligned.isFull)
          seqb_fifo_aligned.enq(underscore, !seqb_fifo_aligned.isFull)
        } else {}
      } { state =>
        mux(state == traverseState && ((b_addr == 0.to[Int]) || (a_addr == 0.to[Int])), padBothState, 
                    mux(seqa_fifo_aligned.isFull || seqb_fifo_aligned.isFull, doneState, state))
      }

```

```
Our implementation ran for 16929 cycles on the FPGA with the two example sequences:

# Sequence A
tcgacgaaataggatgacagcacgttctcgt 
# Sequence B
ttcgagggcgcgtgtcgcggtccatcgacat

These are the resource utilization specs for our implementation:

1. Slice Logic
--------------

+--------------------------------------+-------+-------+-----------+-------+
|               Site Type              |  Used | Fixed | Available | Util% |
+--------------------------------------+-------+-------+-----------+-------+
| Slice LUTs                           | 39254 |     0 |    218600 | 17.96 |
|   LUT as Logic                       | 29900 |     0 |    218600 | 13.68 |
|   LUT as Memory                      |  2117 |     0 |     70400 |  3.01 |
|     LUT as Distributed RAM           |   352 |     0 |           |       |
|     LUT as Shift Register            |  1765 |     0 |           |       |
|   LUT used exclusively as pack-thrus |  7237 |     0 |    218600 |  3.31 |
| Slice Registers                      | 38839 |     0 |    437200 |  8.88 |
|   Register as Flip Flop              | 38838 |     0 |    437200 |  8.88 |
|   Register as Latch                  |     0 |     0 |    437200 |  0.00 |
|   Register as pack-thrus             |     1 |     0 |    437200 | <0.01 |
| F7 Muxes                             |   840 |     0 |    109300 |  0.77 |
| F8 Muxes                             |   304 |     0 |     54650 |  0.56 |
+--------------------------------------+-------+-------+-----------+-------+

2. Slice Logic Distribution
---------------------------

+-------------------------------------------+-------+-------+-----------+-------+
|                 Site Type                 |  Used | Fixed | Available | Util% |
+-------------------------------------------+-------+-------+-----------+-------+
| Slice                                     | 13244 |     0 |     54650 | 24.23 |
|   SLICEL                                  |  8964 |     0 |           |       |
|   SLICEM                                  |  4280 |     0 |           |       |
| LUT as Logic                              | 29900 |     0 |    218600 | 13.68 |
|   using O5 output only                    |     0 |       |           |       |
|   using O6 output only                    | 26686 |       |           |       |
|   using O5 and O6                         |  3214 |       |           |       |
| LUT as Memory                             |  2117 |     0 |     70400 |  3.01 |
|   LUT as Distributed RAM                  |   352 |     0 |           |       |
|     using O5 output only                  |     0 |       |           |       |
|     using O6 output only                  |    80 |       |           |       |
|     using O5 and O6                       |   272 |       |           |       |
|   LUT as Shift Register                   |  1765 |     0 |           |       |
|     using O5 output only                  |   155 |       |           |       |
|     using O6 output only                  |  1576 |       |           |       |
|     using O5 and O6                       |    34 |       |           |       |
| LUT used exclusively as pack-thrus        |  7237 |     0 |    218600 |  3.31 |
|   Number with same-slice carry load       |  4938 |       |           |       |
|   Number with same-slice register load    |  2527 |       |           |       |
|   Number with same-slice other load       |     0 |       |           |       |
| LUT Flip Flop Pairs                       | 16204 |     0 |    218600 |  7.41 |
|   fully used LUT-FF pairs                 |  1402 |       |           |       |
|   LUT-FF pairs with one unused LUT output | 13188 |       |           |       |
|   LUT-FF pairs with one unused Flip Flop  | 13130 |       |           |       |
| Unique Control Sets                       |  1120 |       |           |       |
+-------------------------------------------+-------+-------+-----------+-------+
* Note: Review the Control Sets Report for more information regarding control sets.


3. Memory
---------

+-------------------+------+-------+-----------+-------+
|     Site Type     | Used | Fixed | Available | Util% |
+-------------------+------+-------+-----------+-------+
| Block RAM Tile    |   13 |     0 |       545 |  2.39 |
|   RAMB36/FIFO*    |   12 |     0 |       545 |  2.20 |
|     RAMB36E1 only |   12 |       |           |       |
|   RAMB18          |    2 |     0 |      1090 |  0.18 |
|     RAMB18E1 only |    2 |       |           |       |
+-------------------+------+-------+-----------+-------+
```

