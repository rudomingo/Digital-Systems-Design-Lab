import spatial.dsl._

@spatial object ProjectCNNColorization extends SpatialApp {

  // Set the default height and width of the input image
  val Cmax = 224.to[Int]

  // Set the size of each weight value, can alter this for more precision
  type T = FixPt[TRUE, _5, _11]

  def convert_weights(w_2d: DRAM2[T], M: Int, D: Int, kernel_size: Int): DRAM4[T] = {
    /*
     * Takes in the 2d representation of the weights stored in the csv for a given
     * layer and converts the weights to their original 4d representation in memory
     * for easier indexing.
     *
     * Params:
     *  w_2d            2d representation of the 4d weights
     *  D               The depth of the weights file
     *  M               The number of filters
     *  kernel_size     The kernel size. Assumed the kernel is a square
     */
    val weights = DRAM[T](D, M, kernel_size, kernel_size)
    val filter_length = (M * kernel_size * kernel_size).to[Int]
    val kernel_length = (kernel_size*kernel_size).to[Int]
    val kernel = SRAM[T](kernel_length)
    Foreach (0 until M, 0 until D) { (m,d) =>
      kernel load w_2d(m, kernel_length*d::kernel_length*(d+1.to[Int]))
      Foreach (0 until kernel_size par kernel_size) { x =>
        weights(m, d, x, 0.to[Int]::kernel_size) store kernel(kernel_size*x::kernel_size*(x+1.to[Int]))
      }
    }
    weights
  }

  def ReLU(p:T): T = {
    /*
     * Implements the ReLU functionality
     *
     * Params:
     *  p           The resulting value of the convolution
     */
    mux(p > 0.to[T], p, 0)
  }

  def conv(input: DRAM3[T], input_wh: Int, D: Int, weights_dram: DRAM4[T], M: Int,
           bias_dram: DRAM1[T], S: Int, P: Int, Di: Int, K: Int): DRAM3[T] = {
    /*
     * Fused Convolution - Bias - ReLU functionality. Accelerator first converts the 2d weight file
     * to the 4d representation for easy indexing. Then the convolution is performed.
     *
     * Params:
     *  input         Input into the convolution layer
     *  input_wh      Input width and height. Always assumes square input
     *  D             The depth of the input and the file
     *  weights_2d    The weights for the particular layer read in from the csv file
     *  M             The number of filters in the weights file
     *  bias_dram     The bias to be added on to the convolution result
     *  S             Stride while iterating through the input
     *  P             0 padding added around the input
     *  Di            Kernel dilation factor
     *  K             One dimension size of the square kernel
     */

    // Define the parallelization factor for the line buffer loading
    val lb_par = 8.to[Int]

    // Define the output of the convolution layer
    val output = DRAM[T](M, input_wh/S, input_wh/S)


    val wh = ArgIn[Int]
    val depth = ArgIn[Int]
    val num_filters = ArgIn[Int]
    val stride = ArgIn[Int]
    val padding = ArgIn[Int]
    val dilation = ArgIn[Int]
    val kernel_size = ArgIn[Int]

    setArg(wh, input_wh)
    setArg(depth, D)
    setArg(num_filters, M)
    setArg(stride, S)
    setArg(padding, P)
    setArg(dilation, Di)
    setArg(kernel_size, K)


    Accel {
      // Initialize the line buffer for the convolution to sweep through
      val lb = LineBuffer[T](kernel_size, wh)

      // Convert the 2d weights into 4d weights in DRAM
      //val weights_dram = convert_weights(weights_2d, num_filters, depth, kernel_size)
      val weights = SRAM[T](depth, kernel_size, kernel_size)

      // Load the biases into SRAM
      val bias = SRAM[T](num_filters)
      bias load bias_dram

      val sr = RegFile[T](kernel_size, kernel_size)
      val lineOut = SRAM[T](num_filters)

      Foreach(0 until wh, 0 until wh by stride, 0 until num_filters) { (r,c,m) =>
        weights load weights_dram(m, 0.to[Int]::depth, 0.to[Int]::kernel_size, 0.to[Int]::kernel_size)
        val tmp = Reduce(Reg[T])(0 until depth) { d =>
          lb load input(d, r, 0.to[Int] :: wh par lb_par)
          Pipe {
            sr.reset(c.to[Int] == 0.to[Int])
          }
          Foreach(0 until kernel_size) { i => sr(i, *) <<= lb(i, c) }
          Reduce(0.to[T])(0 until kernel_size, 0 until kernel_size) { (i,j) =>
              sr(i, j) * weights(d, i, j)
          }{_+_}
        }{_+_}
        lineOut(m) = mux(r < kernel_size || c < kernel_size, 0.to[T], max(0.to[T], tmp.value + bias(m)))
        output(0.to[Int]::num_filters, r, c) store lineOut
      }
    }
    output
  }

  def main(args: Array[String]): Unit = {

    val outerPar = 1
    val midPar = 1
    val innerPar = 1

    // Importing weights and biases for all layers
    val w1_1_csv = loadCSV2D[T]("XXXXX.csv", ",")
    val b1_1_csv = loadCSV1D[T]("XXXXX.csv", ",")
    val w1_2_csv = loadCSV2D[T]("XXXXX.csv", ",")
    val b1_2_csv = loadCSV1D[T]("XXXXX.csv", ",")
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

    // Define the kernel size for the following layers
    val kernel_size_1 = 3.to[Int]

    // Initialize weights and biases in DRAM
    val image_dram = DRAM[T](1.to[Int], Cmax, Cmax)
    val w1_1_2d = DRAM[T](64, 1, kernel_size_1, kernel_size_1)
    val b1_1 = DRAM[T](64)
    setMem(image_dram, test_image)
    setMem(w1_1_2d, w1_1_csv)
    setMem(b1_1, b1_1_csv)

    // TODO: Initialize everything else...
    //val output = DRAM[T](Cmax, Cmax)

    val conv1_1_result = conv(image_dram, 224.to[Int], 1.to[Int], w1_1_2d, 64.to[Int], b1_1,
      1.to[Int], 1.to[Int], 1.to[Int], kernel_size_1)

    print(conv1_1_result)
  } 
}

