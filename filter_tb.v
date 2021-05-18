`timescale 1ns / 1ps

module tb;
  integer fd,fw;
  integer i;
  reg [8*45:1] str;
    // Inputs
    reg clk, reset;
    reg signed [31:0] x;
    wire signed [31:0] t;
    wire signed [31:0] t2;
    wire signed [31:0] t3;
    wire signed [31:0] y;

    // Instantiate the Unit Under Test (UUT)
    iir_order2 DUT1(
      .clk(clk),
      .rst(reset),
      .x(x),
      .y(t)
    );
    iir_order2 DUT2(
      .clk(clk),
      .rst(reset),
      .x(t),
      .y(y)
    );

    // Generate clock with 100ns period
    initial 
		begin
			clk = 0;
			fw= $fopen("output_file.txt","w");
		end
	 always #25 clk = ~clk;
    
    always @(posedge(clk)) begin
			$display("time = %.0f,\t x = %.0f,\t y = %.0f", $time, x, y);
//			$sformat(str,"x= %.0d,y= %.0d \n",x,y);
			
		
    end
    

    initial begin
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
				$fscanf(fd, " 	x =               %.0d; #50; // Sample(%.0d)\n",x,i);
				//$fgets(str,fd);
				//$display("%.0d",x);
				#50;
				$fdisplay(fw,y,x);
				//$display("x(%.0d) = %.0d",i,x);
				end
			$fclose(fd);
			$fclose(fw);
      
    end
endmodule
