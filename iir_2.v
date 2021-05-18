/*
    Digital Filter Implementation
    Digital Signal Processing - MTE Project
    Parameters:
        1. index        : Section Index in Nth order Filter.
            (Default, 0)
            
            If module is used as Stand Alone, default value is to be used.
            This Index is used to get Coefficients into Memory using the file with the name "<index>"
            Index should be in the format "xx" (two digits only)
        2. bitwidth     : Width of the Encoded Sequence's Sample (Optional)
            (Default, 32)
    Inputs:
        1. clk          : Clock Input
        3. rst          : Synchronous Reset
        2. x            : Input Stream (Encoded Signal Integer Stream)
    
    Outputs:
        3. y            : Output Stream (Encoded Signal Integer Stream)
    Architecture:
        x ----> + ---w1---------(b0)--- + w2----> y
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
    Internal Wires/Registers:
        (0-4 Index corresponds to b0->b2, a1, a2 respectively)
*/

module iir_2
#(parameter index = 0,  parameter bitwidth = 32, parameter fac = 20, parameter gain = 6)
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

    // For Coeff File derived from Index value
    reg [2*8:1] cfile = "xx";
    integer t0, t1;
    initial begin
        t0 = index % 10;
        t1 = index / 10;
        cfile[8:1] = "0" + t0;
        cfile[16:9] = "0" + t1;
        $readmemb(cfile, C);
        //$display("Index = %d,\nb[0] = %d, \nb[1] = %d, \nb[2] = %d, \na[1] = %d, \na[2] = %d\n", index, C[0], C[1], C[2], C[3], C[4]);
    end

    // Filter Code
    assign w[1] = ((x <<< fac) - C[3]*z[1] - C[4]*z[2]) >>> fac;
    assign w[2] = (C[0]*w[1] + C[1]*z[1] + C[2]*z[2]) >>> fac;
    assign y = w[2] <<< gain;

    always @(posedge(clk)) begin
        if(rst == 1) begin
            z[1] = {2*bitwidth{1'b0}};
            z[2] = {2*bitwidth{1'b0}};
        end
        else begin
            z[1] <= w[1];
            z[2] <= z[1];
        end;
    end
endmodule