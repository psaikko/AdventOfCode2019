line = readline(open("input"))

println(line)

numbers = map(c->parse(Int, c), collect(line))

base_pattern = [0,1,0,-1]

function pattern_at(level)
    global base_pattern
    rep_pattern = reduce(vcat, map(v -> [v for i in 1:level], base_pattern))
    iterator = Iterators.cycle(rep_pattern)
    return Iterators.drop(iterator, 1)
end

function do_phases(numbers::Array{Int}, n)
    println(length(numbers))
    for phase in 1:n
        #println(phase)
        transform_digit(position) = abs(sum(map(*, numbers, pattern_at(position)))) % 10
        numbers = transform_digit.(1:length(numbers))
    end
    return numbers
end

tostring(a) = join(map(string, a))

res = do_phases(copy(numbers), 100)
println(tostring(res[1:8]))
