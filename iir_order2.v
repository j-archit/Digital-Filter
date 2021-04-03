/*
    Digital Filter Implementation
    Digital Signal Processing - MTE Project

    Parameters:
        1. bitwidth     : Width of the Encoded Sequence's Sample (Default, 32)
        2. coeffs_file  : File Containing 5 filter coefficients in Binary Integer Format
        
    Inputs:
        1. clk          : Clock Input
        2. x            : Input Stream (Encoded Signal Integer Stream)
    
    Outputs:
        3. y            : Output Stream (Encoded Signal Integer Stream)
    
*/

module iir_order2
#(parameter bitwidth = 32, parameter coeffs_file = "1.txt")
(
    input clk,
    input [bitwidth-1:0] x,
    output [bitwidth-1:0] y
);

    reg [bitwidth-1:0] coeffs [0:4];
    initial begin
        $readmemb(coeffs_file, coeffs);
    end
    // Filter Code Here

endmodule