lines = readlines(open("input"))

rules = Dict()

for line in lines
    inputs_s, output_s = strip.(split(line, "=>"))

    reagents = Dict{String,BigInt}()

    for token in strip.(split(inputs_s, ","))
        n, id = split(token)
        reagents[id] = parse(Int, n)
    end

    n, id = split(output_s)
    rules[id] = (amount=parse(Int, n), inputs=reagents)
end

inputs_of(name) = keys(rules[name].inputs)
recipe_amount(target, ingredient) = rules[target].inputs[ingredient]
batch_size(name) = rules[name].amount

depth_cache = Dict{String,BigInt}(["ORE" => 0])

function depth_of(ingredient)
    if haskey(depth_cache, ingredient)
        return depth_cache[ingredient]
    else 
        d = 1 + max(depth_of.(inputs_of(ingredient))...)
        depth_cache[ingredient] = d
        return d
    end
end

println(rules)

import DataStructures

function ore_required(fuel)
    frontier = DataStructures.DefaultDict{String,BigInt}(0)
    for (x, k) in rules["FUEL"].inputs
        frontier[x] = k * fuel
    end
    while length(keys(frontier)) > 1 || !haskey(frontier, "ORE")
        by_depth = sort(collect(keys(frontier)), by=depth_of)
        most_complex = by_depth[end]

        req = frontier[most_complex]
        batches = BigInt(ceil(req / batch_size(most_complex)))

        for (x, k) in rules[most_complex].inputs 
            frontier[x] += k * batches
        end

        delete!(frontier, most_complex)
    end
    return frontier["ORE"]
end

println(ore_required(1))

N = 1000000000000
lb = div(N, ore_required(1))
ub = 2*lb

while lb < ub
    global lb, ub, N
    m = div((lb + ub + 1), 2)

    req = ore_required(m)
    println("$m $req")

    if req > N
        ub = m
    else
        lb = m+1
    end
end

# println(depth_of("FUEL"))