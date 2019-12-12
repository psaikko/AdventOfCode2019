import Base.+
import Base.-
import Base.map

lines = readlines(open("input"))

subs = ["<" => "(", ">" => ")"]

moons = []

Coord = NamedTuple{(:x,:y,:z)}

for line in lines
    for sub in subs
        line = replace(line, sub)
    end
    global moons
    push!(moons, [eval(Meta.parse(line)), Coord((0,0,0))])
end

(+)(a::Coord, b::Coord) = Coord(map(+,a,b))
(-)(a::Coord, b::Coord) = Coord(map(-,a,b))
map(f, c::Coord) = Coord(map(f, collect(c)))

function sign(x)
    if x < 0 return -1
    elseif x > 0 return 1
    else return 0
    end
end

function pull(a, b) 
    diff = b[1] - a[1]
    change = map(sign,diff)
    return change
end

function energy(moon)
    potential = sum(map(abs, moon[1]))
    kinetic = sum(map(abs, moon[2]))
    return potential * kinetic
end

map(println, moons)

for timestep in 1:1000
    vdiffs = [Coord((0,0,0)) for moon in moons]

    for i in 1:length(moons)
        for j in 1:length(moons)
            if i != j
                vdiffs[i] += pull(moons[i], moons[j])
            end
        end
    end

    for (moon,diff) in zip(moons, vdiffs)
        moon[2] += diff
    end

    for moon in moons 
        moon[1] += moon[2]
    end
    
    # println(timestep)
    # map(println, moons)
end

println(sum(map(energy, moons)))