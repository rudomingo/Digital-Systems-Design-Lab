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
// Copy-paste your implementation here
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
// Copy-paste your implementation here
```

### Part 5
* Please tell us what works and what doesn't for this lab:
