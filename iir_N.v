/*
    Generalized Nth Order Filter 
    Implemented Using Second Order Sections.
    Parameters: 
        1. N            : Order of the Filter
                          (Default, 2)
        2. bitwidth     : Bitwidth of Encoded Sequence (Optional)
                          (Default, 32)
    Inputs:
        1. clk          : Clock Input
        2. rst          : Reset Input
        2. x            : Encoded Input Sequence
    Output:
        1. y            : Encoded Output Sequence 
*/

module iir_N 
#(parameter N = 2, parameter bitwidth = 32, parameter sections = (N+1)/2)
(
    input clk,
    input rst,
    input [bitwidth-1:0] x,
    output [bitwidth-1:0] y
);

    // Intermediate Wires
    wire [bitwidth-1:0] t [0:sections+1];
    assign t[0] = x;
    assign y = t[sections];

    genvar i;
    generate
        for (i = 0; i < N; i = i + 2) begin
            iir_2 #(.index(i/2)) s(.clk(clk), . rst(rst), .x(t[(i/2)]), .y(t[i/2+1]));
        end
    endgenerate
endmodule