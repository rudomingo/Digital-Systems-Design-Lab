@spatial object ProjectCNNColorization extends SpatialApp {

  val Kh = 3
  val Kw = 3
  // Value of max column length = 512*3*3
  val Cmax = 4608

  // Can alter this for more precision
  type T = FixPt[TRUE, _5, _11]

  def main(args: Array[String]): Unit = {

    val outerPar = 1
    val midPar = 1
    val innerPar = 1

    // val B = 256

    // val R = ArgIn[Int]
    // val C = ArgIn[Int]
    val R = 224
    val C = 224
    val border = 3


    val W_data = loadCSV2D[T]("XXXXX.csv", ",")
    val b_data = loadCSV1D[T]("XXXXX.csv", ",")
    val test_image = loadCSV2D[T]("XXXXX.csv", ",")
    // ground truth image?? for comparision
    // val gold = loadCSV2D[T]("XXXXX.csv, ",")
    
    val image_dram = DRAM[T](R, C)
    val W = DRAM[T](64, 36)
    val b = DRAM[T](64)
    setMem(image_dram, test_image)
    setMem(W_data, W)
    setMem(b_data, b)
    // setArg(R, image.rows)
    // setArg(C, image.cols)
    // val lb_par = 8

    // val img = DRAM[T](R, C)
    val output = DRAM[T](R, C)

    // setMem(img, image)

    Accel {
      val lb = LineBuffer[T](Kh, Cmax)

      val kh = LUT[T](6,6)(1.to[T], 0.to[T], -1.to[T],
                           2.to[T], 0.to[T], -2.to[T],
                           2.to[T], 0.to[T], -2.to[T],
                           2.to[T], 0.to[T], -2.to[T],
                           2.to[T], 0.to[T], -2.to[T],
                           2.to[T], 0.to[T], -2.to[T],
                           2.to[T], 0.to[T], -2.to[T],
                           2.to[T], 0.to[T], -2.to[T],
                           2.to[T], 0.to[T], -2.to[T],
                           2.to[T], 0.to[T], -2.to[T],
                           2.to[T], 0.to[T], -2.to[T],
                           1.to[T], 0.to[T], -1.to[T])
      val kv = LUT[T](6,6)(1.to[T],  2.to[T],  1.to[T],                                                                                0.to[T],  0.to[T],  0.to[T],
                           -1.to[T], -2.to[T], -1.to[T],
                           -1.to[T], -2.to[T], -1.to[T],
                           -1.to[T], -2.to[T], -1.to[T],
                           -1.to[T], -2.to[T], -1.to[T],
                           -1.to[T], -2.to[T], -1.to[T],
                           -1.to[T], -2.to[T], -1.to[T],
                           -1.to[T], -2.to[T], -1.to[T],
                           -1.to[T], -2.to[T], -1.to[T],
                           -1.to[T], -2.to[T], -1.to[T],
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
          lineOut(c) = mux( r<5 || c<5, 0.to[T], abs(horz.value) + abs(vert.value)) 
        }
        imgOut(r, 0::C) store lineOut
      } 
    } 
    
    getMatrix(imgOut)
  }
}
