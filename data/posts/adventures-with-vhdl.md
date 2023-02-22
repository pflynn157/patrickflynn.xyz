---
title: "Adventures with VHDL"
date: "2021-11-07"
categories: 
  - "hardware"
---

As part of one of my classes I took for my minor, I learned some basic VHDL. Actually, I think VHDL is the optional part (so far, I've been learning it pretty much on my own, though the introduction came from the class). I've wanted to learn a hardware descriptor language for some time. I tried Verilog, but I had a hard time finding good tutorials on how to use it, and for some reason I never really looked at VHDL (maybe Verilog scared me away). This may be a slightly unpopular opinion, but I really like VHDL. The reason is the reason why most people dislike it: its basically a subset of Ada, which is a language I'm familiar with and admire.

Anyway, I finally managed to get a simple circuit to run: a full adder, which I eventually made into an 8-bit adder. It is signed, meaning you can use it as either an adder or a subtractor. I'll come back to this in a minute. Here's what it looks like:

```
library IEEE;
use IEEE.std_logic_1164.all;

-- A single bit full adder
entity full_adder is
    port (
        a, b, ci : in std_logic;
        s, co : out std_logic
    );
end full_adder;

library IEEE;
use IEEE.std_logic_1164.all;

-- An 8-bit adder
entity adder is
    port (
        vec1 : in std_logic_vector(7 downto 0);
        vec2 : in std_logic_vector(7 downto 0);
        out_vec : out std_logic_vector(7 downto 0);
        co : out std_logic
    );
end adder;

-- The logic for the single-bit adder
architecture rtl_full_adder of full_adder is
begin
    s <= (a xor b) xor ci;
    co <= ((a xor b) and ci) or (a and b);
end rtl_full_adder;

-- The logic for the 8-bit adder
architecture rtl_adder of adder is
    component full_adder
        port (
            a, b, ci : in std_logic;
            s, co : out std_logic
        );
    end component;

    signal c : std_logic_vector(8 downto 0);
begin
    op1 : full_adder port map(a => vec1(0), b => vec2(0), ci => '0', s => out_vec(0), co => c(1));
    op2 : full_adder port map(a => vec1(1), b => vec2(1), ci => c(1), s => out_vec(1), co => c(2));
    op3 : full_adder port map(a => vec1(2), b => vec2(2), ci => c(2), s => out_vec(2), co => c(3));
    op4 : full_adder port map(a => vec1(3), b => vec2(3), ci => c(3), s => out_vec(3), co => c(4));
    op5 : full_adder port map(a => vec1(4), b => vec2(4), ci => c(4), s => out_vec(4), co => c(5));
    op6 : full_adder port map(a => vec1(5), b => vec2(5), ci => c(5), s => out_vec(5), co => c(6));
    op7 : full_adder port map(a => vec1(6), b => vec2(6), ci => c(6), s => out_vec(6), co => c(7));
    op8 : full_adder port map(a => vec1(7), b => vec2(7), ci => c(7), s => out_vec(7), co => c(8));
    co <= c(8);
end rtl_adder;
```

Its actually not as scary as it looks; even without the background, it should be pretty easy to understand how it works. Binary addition works the same way we humans add numbers- we start with the digit on the right, and work left. The full adder is the smaller circuit that performs the logic operation to add two bits (three if you have carry). In base-2, 0+0 = 0, 0 + 1 = 1, 1 + 0 = 1, 1 + 1 = 0 carry 1, and 1 + 1 + 1 = 1 carry 1 (that extra 1 would be the carry; in all other cases, you can assume its zero). In the 8-bit adder, we simply use the full adder on each bit.

As I mentioned earlier, this implements a signed adder. That means the first bit will be treated as the sign bit. Like all other adders, this uses the 2's complement representation of negative numbers. Because it is a signed adder, it also works as a subtractor. Although we often think of subtraction as a separate operation, to a computer there is no such thing. Computers perform addition on signed numbers. So if you wanted to do 10 - 5, to a computer it would be 10 + (-5). For our use, it is a complicated way to do it, but it yields the same result.

I think the idea with VHDL testbenches is to test all values, but I wanted to try something once I found VHDL had text IO like other languages. If you use the IEEE standard logic types, you can convert integers to and from the bit vectors. Connect this with some input and output, and you have a simple calculator:

![](images/vhdl_calc.png)

And below is the code if you want to try it out. I am using GHDL to build and run this, so I also included the commands I used. Also note, because its 8-bit, you can add numbers until their sum is less than or equal to 127 (binary: 01111111). Anything greater will invert the most significant bit, which will result in a negative number.

```
ghdl -a adder.vhdl

ghdl -a --ieee=synopsys test.vhdl
ghdl -e --ieee=synopsys adder_tb
ghdl -r --ieee=synopsys adder_tb --ieee-asserts=disable
```
```
library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.std_logic_signed.all;
use IEEE.std_logic_arith.all;
use IEEE.numeric_std.all;
use std.textio.all;

-- A testbench has no ports.
entity adder_tb is
end adder_tb;

architecture behav of adder_tb is
    constant WIDTH : integer := 8;

    -- Declaration of the component that will be instantiated.
    component adder
        port (
            vec1 : in std_logic_vector(WIDTH-1 downto 0);
            vec2 : in std_logic_vector(WIDTH-1 downto 0);
            out_vec : out std_logic_vector(WIDTH-1 downto 0);
            co : out std_logic
        );
    end component;

    -- Specifies which entity is bound with the component.
    for add0: adder use entity work.adder;
    signal vec1, vec2, out_vec : std_logic_vector(WIDTH-1 downto 0);
    signal co : std_logic;

begin
    -- Component instantiation.
    add0: adder port map (vec1 => vec1, vec2 => vec2, out_vec => out_vec, co => co);

    -- This process does the real job.
    process

        -- For input
        variable in_buf1 : line;
        variable in_buf2 : line;
        variable in_num1 : integer;
        variable in_num2 : integer;

        variable val1 : std_logic_vector(WIDTH-1 downto 0);
        variable val2 : std_logic_vector(WIDTH-1 downto 0);

        -- For output
        variable l : line;
        variable out_num : integer;
    begin

        -- Get all the input
        write(l, String'("Enter two numbers"));
        writeline(output, l);

        readline(input, in_buf1);
        read(in_buf1, in_num1);

        readline(input, in_buf2);
        read(in_buf2, in_num2);

        val1 := conv_std_logic_vector(in_num1, WIDTH);
        val2 := conv_std_logic_vector(in_num2, WIDTH);

        wait for 50 ns;

        -- Do the calculations
        vec1 <= val1;
        vec2 <= val2;
        wait for 50 ns;

        -- Output everything
        write(l, String'("Num1: "));
        write(l, to_bitvector(val1));
        write(l, String'(" | Num2: "));
        write(l, to_bitvector(val2));
        writeline(output, l);

        out_num := conv_integer(out_vec);

        write(l, String'(""));
        writeline(output, l);
        write(l, String'("Result: "));
        write(l, out_num);
        writeline(output, l);

        write(l, String'("Output: "));
        write(l, to_bitvector(out_vec));
        writeline(output, l);

        wait;
    end process;

end behav;
```

