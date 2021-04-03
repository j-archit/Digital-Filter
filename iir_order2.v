/*
    Digital Filter Implementation
    Digital Signal Processing - MTE Project

    Parameters:
        1. bitwidth     : Width of the Encoded Sequence's Sample (Default, 32)
        2. coeffs_file  : File Containing 5 filter coefficients in Binary Integer Format
            (0-5 Index corresponds to b0->b2, a1, a2 respectively)

    Inputs:
        1. clk          : Clock Input
        2. x            : Input Stream (Encoded Signal Integer Stream)
    
    Outputs:
        3. y            : Output Stream (Encoded Signal Integer Stream)

    Architecture:
        x ----> + ---w1----- ----b0---- + w2----> y
                ^           |           ^
                |           v           |
                |           z1          |
                |           |           |
                |           |           |
                + <--(-a1)-------b1---> +
                ^           |           ^
                |           v           |
                |           z2          |
                |           |           |
                |           |           |
                |----(-a2)-------b2-----| 

*/

module iir_order2
#(parameter bitwidth = 32, parameter coeffs_file = "1.txt")
(
    input clk,
    input signed [bitwidth-1:0] x,
    output signed [bitwidth-1:0] y
);

    reg signed [bitwidth-1:0] C [0:4];
    initial begin
        $readmemb(coeffs_file, C);
    end

    reg signed [bitwidth-1:0] z [1:2];
    
    wire signed [bitwidth-1:0] w1, w2;

    // Filter Code
    assign w1 = -C[3]*z[1] + -C[4]*z[2];
    assign w2 = C[0]*w1 + C[1]*z[1] + C[2]*z[2];
    assign y = w2 << 20;

    always @(posedge(clk)) begin
        z[1] <= w1;
        z[2] <= z[1];
    end
    
endmodule