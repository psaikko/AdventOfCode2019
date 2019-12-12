
lines = readlines(open("input"))

subs = ["<" => "[", ">" => "]", r"[xyz=]" => ""]

positions = zeros(Int64, 4, 3)
velocities = zeros(Int64, 4, 3)

for (i,line) in enumerate(lines)
    for sub in subs
        line = replace(line, sub)
    end
    global positions
    positions[i,:] = eval(Meta.parse(line))
end

function periodicity(ps, vs)
    println(ps)

    seen = Set{Array{Int64,1}}()
    c = 0

    push!(seen, vcat(ps,vs))

    while true
        c += 1

        for p in ps
            vs -= ps .> p
            vs += ps .< p
        end

        ps += vs

        state = vcat(ps, vs)
        if (state in seen) break end
    end
    
    return c
end

show(stdout, "text/plain", positions)
println()

m = size(positions)[2]

println(lcm([periodicity(positions[:,i], velocities[:,i]) for i in 1:m]...))

