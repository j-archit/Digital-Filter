`timescale 1ns / 1ps

module testbench;

  // Parameters and Inputs
  parameter ORDER = 4;
  parameter SAMPLE_DELAY = 50;
  parameter BITWIDTH = 32;
  parameter SHIFT_FAC = 20;
  parameter HTP = 10; // Half Time Period of Clock
  
  reg clk, reset;
  reg signed [BITWIDTH-1:0] x;
  wire signed [BITWIDTH-1:0] y;

  integer fd,fw;
  reg [8*45:1] str;
  
  // Instantiate the Unit Under Test (DUT)
  iir_N #(.N(ORDER), .BITWIDTH(BITWIDTH), .FAC(SHIFT_FAC)) DUT(
    .clk(clk),
    .rst(reset),
    .x(x),
    .y(y)
  );

  // Generate clock with 2*htp period
  initial clk = 0;
  always #HTP clk = ~clk;

  initial fw= $fopen("io_samples","w");

  always @(posedge(clk)) begin
    $display("time = %.0f,\t x = %.0f,\t y = %.0f", $time, x, y);
  end

  initial begin
    // Begin Init Sequence
    x = 32'd0;
    reset = 1;
    clk = 0;
    clk = 1;
    #10;
    reset = 0;
    #20;

    fd = $fopen("input_file.txt","r");
    while(!$feof(fd))
      begin
      $fscanf(fd, "%.0d\n", x);
      #SAMPLE_DELAY;
      
      $fdisplay(fw,y,x);
      end
    
    $fclose(fd);
    $fclose(fw);    
  end
endmodule
