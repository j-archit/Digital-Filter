/*  Generalized Nth Order Filter 
    Implemented Using Second Order SECTIONS.
    Parameters: 
        1. N            : Order of the Filter
                          (Default, 2)
        2. BITWIDTH     : BITWIDTH of Encoded Sequence (Optional)
                          (Default, 32)
        3. FAC          : Decimal to Integer shift factor's power. Left-shifted by 2^FAC
                          (Default, 20)
        4. GAINL        : Section Wise Gain ( <1 ) adjust. Output right-shited by 2^GAINL
                          (Default, 0)
        5. GAINM        : Section Wise Gain ( >1 ) adjust. Output left-shited by 2^GAINL
                          (Default, 0)

    Inputs:
        1. clk          : Clock Input
        2. rst          : Reset Input
        2. x            : Encoded Input Sequence [BITWIDTH-1:0]
    Output:
        1. y            : Encoded Output Sequence [BITWIDTH-1:0]
*/

module iir_N 
#(  // Parameter List
    parameter N = 2, 
    parameter BITWIDTH = 32,
    parameter FAC = 20,
    parameter GAINL = 0,
    parameter GAINM = 0
)
(   // Port List
    input clk,
    input rst,
    input [BITWIDTH-1:0] x,
    output [BITWIDTH-1:0] y
);

    localparam SECTIONS = (N+1)/2;
    // Intermediate Wires
    wire [BITWIDTH-1:0] t [0:SECTIONS+1];
    assign t[0] = x;
    assign y = t[SECTIONS];

    genvar i;
    generate
        for (i = 0; i < N; i = i + 2) begin
            iir_2 #(.INDEX(i/2), .BITWIDTH(BITWIDTH), .FAC(FAC), .GAINL(GAINL), .GAINM(GAINM)) s(.clk(clk), . rst(rst), .x(t[(i/2)]), .y(t[i/2+1]));
        end
    endgenerate
endmodule