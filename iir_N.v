/*
    Generalized Nth Order Filter 
    Implemented Using Second Order SECTIONS.
    Parameters: 
        1. N            : Order of the Filter
                          (Default, 2)
        2. BITWIDTH     : BITWIDTH of Encoded Sequence (Optional)
                          (Default, 32)
    Inputs:
        1. clk          : Clock Input
        2. rst          : Reset Input
        2. x            : Encoded Input Sequence
    Output:
        1. y            : Encoded Output Sequence 
*/

module iir_N 
#(parameter N = 2, parameter BITWIDTH = 32, parameter SECTIONS = (N+1)/2, parameter FAC = 20)
(
    input clk,
    input rst,
    input [BITWIDTH-1:0] x,
    output [BITWIDTH-1:0] y
);

    // Intermediate Wires
    wire [BITWIDTH-1:0] t [0:SECTIONS+1];
    assign t[0] = x;
    assign y = t[SECTIONS];

    genvar i;
    generate
        for (i = 0; i < N; i = i + 2) begin
            iir_2 #(.INDEX(i/2), .BITWIDTH(BITWIDTH), .FAC(FAC)) s(.clk(clk), . rst(rst), .x(t[(i/2)]), .y(t[i/2+1]));
        end
    endgenerate
endmodule