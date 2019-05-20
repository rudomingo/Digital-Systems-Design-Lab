@spatial object ProjectCNNColorization extends SpatialApp {

  val kernel_size = 3
  val Cmax = 224

  // Can alter this for more precision
  type T = FixPt[TRUE, _5, _11]

  def main(args: Array[String]): Unit = {

    val outerPar = 1
    val midPar = 1
    val innerPar = 1

    // Importing weights and biases for all layers
    val w1_1_data = loadCSV2D[T]("XXXXX.csv", ",")
    val b1_1_data = loadCSV1D[T]("XXXXX.csv", ",")
    val w1_2_data = loadCSV2D[T]("XXXXX.csv", ",")
    val b1_2_data = loadCSV1D[T]("XXXXX.csv", ",")
    val norm_1 = loadCSV1D[T]("XXXXX.csv", ",")

    /*
    val w2_1_data = loadCSV2D[T]("XXXXX.csv", ",")
    val b2_1_data = loadCSV1D[T]("XXXXX.csv", ",")
    val w2_2_data = loadCSV2D[T]("XXXXX.csv", ",")
    val b2_2_data = loadCSV1D[T]("XXXXX.csv", ",")
    val norm_2 = loadCSV1D[T]("XXXXX.csv", ",")

    val w3_1_data = loadCSV2D[T]("XXXXX.csv", ",")
    val b3_1_data = loadCSV1D[T]("XXXXX.csv", ",")
    val w3_2_data = loadCSV2D[T]("XXXXX.csv", ",")
    val b3_2_data = loadCSV1D[T]("XXXXX.csv", ",")
    val w3_3_data = loadCSV2D[T]("XXXXX.csv", ",")
    val b3_3_data = loadCSV1D[T]("XXXXX.csv", ",")
    val norm_3 = loadCSV1D[T]("XXXXX.csv", ",")

    val w4_1_data = loadCSV2D[T]("XXXXX.csv", ",")
    val b4_1_data = loadCSV1D[T]("XXXXX.csv", ",")
    val w4_2_data = loadCSV2D[T]("XXXXX.csv", ",")
    val b4_2_data = loadCSV1D[T]("XXXXX.csv", ",")
    val w4_3_data = loadCSV2D[T]("XXXXX.csv", ",")
    val b4_3_data = loadCSV1D[T]("XXXXX.csv", ",")
    val norm_4 = loadCSV1D[T]("XXXXX.csv", ",")

    val w5_1_data = loadCSV2D[T]("XXXXX.csv", ",")
    val b5_1_data = loadCSV1D[T]("XXXXX.csv", ",")
    val w5_2_data = loadCSV2D[T]("XXXXX.csv", ",")
    val b5_2_data = loadCSV1D[T]("XXXXX.csv", ",")
    val w5_3_data = loadCSV2D[T]("XXXXX.csv", ",")
    val b5_3_data = loadCSV1D[T]("XXXXX.csv", ",")
    val norm_5 = loadCSV1D[T]("XXXXX.csv", ",")
   
    val w6_1_data = loadCSV2D[T]("XXXXX.csv", ",")
    val b6_1_data = loadCSV1D[T]("XXXXX.csv", ",")
    val w6_2_data = loadCSV2D[T]("XXXXX.csv", ",")
    val b6_2_data = loadCSV1D[T]("XXXXX.csv", ",")
    val w6_3_data = loadCSV2D[T]("XXXXX.csv", ",")
    val b6_3_data = loadCSV1D[T]("XXXXX.csv", ",")
    val norm_6 = loadCSV1D[T]("XXXXX.csv", ",")

    val w7_1_data = loadCSV2D[T]("XXXXX.csv", ",")
    val b7_1_data = loadCSV1D[T]("XXXXX.csv", ",")
    val w7_2_data = loadCSV2D[T]("XXXXX.csv", ",")
    val b7_2_data = loadCSV1D[T]("XXXXX.csv", ",")
    val w7_3_data = loadCSV2D[T]("XXXXX.csv", ",")
    val b7_3_data = loadCSV1D[T]("XXXXX.csv", ",")
    val norm_7 = loadCSV1D[T]("XXXXX.csv", ",")
    
    val w8_1_data = loadCSV2D[T]("XXXXX.csv", ",")
    val b8_1_data = loadCSV1D[T]("XXXXX.csv", ",")
    val w8_2_data = loadCSV2D[T]("XXXXX.csv", ",")
    val b8_2_data = loadCSV1D[T]("XXXXX.csv", ",")
    val w8_3_data = loadCSV2D[T]("XXXXX.csv", ",")
    val b8_3_data = loadCSV1D[T]("XXXXX.csv", ",")
    val norm_8 = loadCSV1D[T]("XXXXX.csv", ",")
  */

    val test_image = loadCSV2D[T]("XXXXX.csv", ",")
    // ground truth image?? for comparision
    // val gold = loadCSV2D[T]("XXXXX.csv, ",")
    
    // Initialize weights and biases in DRAM
    val image_dram = DRAM[T](Cmax, Cmax)
    val w1_1 = DRAM[T](64, 9)
    val b1_1 = DRAM[T](64)
    setMem(image_dram, test_image)
    setMem(w1_1, w1_1_data)
    setMem(b1_1, b1_1_data)

    // TODO: Initialize everything else...
    val output = DRAM[T](Cmax, Cmax)

    val conv1_1_result = conv1_1(image_dram)
  } 

  def conv1_1(image: Matrix[T]): Matrix[T] = {
    val num_filters = 64
    val lb_par = 8
    val conv1_1_result = DRAM[T](Cmax, num_filters*Cmax)

    Accel {
      val lb = LineBuffer[T](kernel_size, Cmax)

      val filters = LUT[T](num_filters,9)
      val bias = SRAM[T](num_filters)
      filters load w1_1
      bias load b1_1
      
      val sr = RegFile[T](kernel_size, kernel_size)
      // 14336 = 64 * 224, all kernel results for one row
      val lineOut = SRAM[T](num_filters*Cmax)

      Foreach (0 until Cmax) {r =>
        lb load img(r, 0::Cmax par lb_par)
        Foreach (0 until Cmax) {c =>
          Pipe{sr.reset(c==0)}
          Foreach (0 until kernel_size) {i => sr(i,*) <<= lb(i,c)}
          Foreach (0 until num_filters) { filter_index =>  
            val result = MemFold(bias)(kernel_size by 1) { i =>
              Reduce(0)(kernel_size by 1) { j => 
                sr(i,j) * filters(filter_index,i*3 + j)
              }{_+_}
            }{_+_} 
            lineOut(filter_index*Cmax + c) = mux( r<kernel_size || c<kernel_size, 0.to[T], max(0.to[T], result.value))
          }
        }
        conv1_1_result(r,0::num_filters*Cmax) store lineOut
      } 
    } 
    getMatrix(conv1_1_result)
  }
}

