open("input") do f
    global lines = readlines(f)
end

pairs = [split(s,")") for s in lines]
planets = reduce(union, map(Set, pairs))
orbits = Dict(p[2]=>p[1] for p in pairs)

depth(planet) = if haskey(orbits, planet) 1+depth(orbits[planet]) else 0 end

println(sum(map(depth, collect(planets))))

dist = Dict{String,Int64}()
source = orbits["YOU"]
dest = orbits["SAN"]

function trace1(planet, i) 
    dist[planet] = i
    if haskey(orbits, planet)
        trace1(orbits[planet], i+1)
    end
end

function trace2(planet, i)
    if haskey(dist, planet)
        return i+dist[planet]
    elseif haskey(orbits, planet)
        trace2(orbits[planet], i+1)
    end
end

trace1(source, 0)
println(trace2(dest, 0))
