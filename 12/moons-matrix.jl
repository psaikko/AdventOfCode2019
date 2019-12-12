import Base.+
import Base.-
import Base.map

lines = readlines(open("input"))

subs = ["<" => "[", ">" => "]", r"[xyz=]" => ""]

positions = zeros(4, 3)
velocities = zeros(4, 3)

for (i,line) in enumerate(lines)
    for sub in subs
        line = replace(line, sub)
    end
    global positions
    positions[i,:] = eval(Meta.parse(line))
end

show(stdout, "text/plain", positions)
println()

n = size(positions)[1]

for timestep in 1:1000000
    global positions, velocities

    for i in 1:n
        velocities += sign.(positions .* -1 .+ positions[i,:]')
    end

    positions += velocities
end

potential = sum(abs.(positions),dims=2)
kinetic = sum(abs.(velocities),dims=2)
println(sum(potential .* kinetic))
