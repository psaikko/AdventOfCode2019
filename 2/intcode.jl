prog = map(s->parse(Int,s),split(readline(open("input")),","))

println(prog)

mutable struct Program 
    MEM::Array{Int64,1}
    PC::Int64
    HALT::Bool
end 

function read(p::Program, addr::Int64)::Int64
    return p.MEM[addr+1]
end

function write(p::Program, addr::Int64, val::Int64)
    p.MEM[addr+1] = val
end

function get_arg(p::Program)::Int64
    v = read(p, p.PC)
    p.PC += 1
    return v
end

function put_res(p::Program, val::Int64)::Int64
    res_addr = get_arg(p)
    write(p, res_addr, val)
end

function binary_instr(p::Program, op::Function) 
    arg_a = get_arg(p)
    arg_b = get_arg(p)
    val_a = read(p, arg_a)
    val_b = read(p, arg_b)
    put_res(p, op(val_a, val_b))
end

function inst_halt(p::Program)
    p.HALT = true
end

instructions = Dict(
    1 => (p -> binary_instr(p, +)),
    2 => (p -> binary_instr(p, *)),
    99 => inst_halt,
)

p = Program(prog,0,false)

write(p,1,12)
write(p,2,2)

while !p.HALT
    op = get_arg(p)
    instructions[op](p)
end

println(read(p,0))