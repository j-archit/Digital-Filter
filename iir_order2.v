/*
    Digital Filter Implementation
    Digital Signal Processing - MTE Project

    Parameters:
        1. bitwidth     : Width of the Encoded Sequence's Sample (Default, 32)
        2. coeffs_file  : File Containing 5 filter coefficients in Binary Integer Format
            (0-4 Index corresponds to b0->b2, a1, a2 respectively)

    Inputs:
        1. clk          : Clock Input
        3. rst          : Synchronous Reset
        2. x            : Input Stream (Encoded Signal Integer Stream)
    
    Outputs:
        3. y            : Output Stream (Encoded Signal Integer Stream)

    Architecture:
        x ----> + ---w1----z0---(b0)--- + w2----> y
                ^           |           ^
                |           v           |
                |           z1          |
                |           |           |
                |           |           |
                + <--(-a1)------(b1)--> +
                ^           |           ^
                |           v           |
                |           z2          |
                |           |           |
                |           |           |
                |----(-a2)------(b2)----| 

*/

module iir_order2
#(parameter bitwidth = 32, parameter coeffs_file = "1.txt")
(
    input clk,
    input rst,
    input signed [bitwidth-1:0] x,
    output signed [bitwidth-1:0] y
);

    // Filter Structure Wires and Registers
    reg signed [bitwidth-1:0] C [0:4];
    reg signed [2*bitwidth-1:0] z [1:2];
    wire signed [2*bitwidth-1:0] w [1:2];

    initial begin
        $readmemb(coeffs_file, C);
        z[1] = 64'b0;
        z[2] = 64'b0;
        //$display("0:b[0] = %d, \n1:b[1] = %d, \n2:b[2] = %d, \n3:a[1] = %d, \n4:a[2] = %d\n", C[0], C[1], C[2], C[3], C[4]);
    end

    // Filter Code
    assign w[1] = ((x <<< 20) - C[3]*z[1] - C[4]*z[2]) >>> 20;
    assign w[2] = (C[0]*w[1] + C[1]*z[1] + C[2]*z[2]) >>> 20;
    assign yw1 = w[1];
    assign y = w[2] >>> 4;

    always @(posedge(clk)) begin
        if(rst == 1) begin
            z[1] = 64'b0;
            z[2] = 64'b0;
        end
        else begin
            z[1] <= w[1];
            z[2] <= z[1];
        end;
    end
endmodule