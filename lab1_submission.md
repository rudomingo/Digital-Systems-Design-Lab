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
