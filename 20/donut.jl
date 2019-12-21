lines = readlines(open("input"))
grid = collect.(lines)

println.(join.(grid))

Point = Tuple{Int,Int}

portals = Dict{String,Array{Point}}()

neighbours(x,y) = [(x+1,y),(x,y+1),(x-1,y),(x,y-1)]

function readportal(x,y) 
    neighbour_tiles = [grid[ny][nx] for (nx,ny) in neighbours(x,y)]
    if !('.' in neighbour_tiles) return end

    if grid[y-1][x] == '.'
        portal = grid[y][x] * grid[y+1][x]
        location = (x,y-1)
    elseif grid[y+1][x] == '.'
        portal = grid[y-1][x] * grid[y][x]
        location = (x,y+1)
    elseif grid[y][x-1] == '.'
        portal = grid[y][x] * grid[y][x+1]
        location = (x-1,y)
    else # grid[y][x+1] == '.'
        portal = grid[y][x-1] * grid[y][x]
        location = (x+1,y)
    end

    if haskey(portals,portal)
        push!(portals[portal], location)
    else
        portals[portal] = [location]
    end

end

for y = 2:(length(grid)-1)
    for x = 2:(length(grid[1])-1)
        if occursin(r"[A-Z]", string(grid[y][x]))
            readportal(x,y)
        end
    end
end

println(portals)

start = portals["AA"][1]
goal  = portals["ZZ"][1]

jumps = Dict{Point, Point}()
for (portal, endpoints) in portals
    if length(endpoints) == 2
        a = endpoints[1]
        b = endpoints[2]
        jumps[a] = b
        jumps[b] = a
    end
end

# BFS from start 
q = [(start, 0)]

visited = Set{Point}()

while length(q) > 0
    loc, dist = popfirst!(q)
    push!(visited, loc)

    next_locs = [(x,y) for (x,y) in neighbours(loc...) if grid[y][x] == '.']

    if haskey(jumps, loc)
        push!(next_locs, jumps[loc])
    end

    for next in next_locs
        if next in visited
            continue
        end

        if next == goal
            println(dist + 1)
            exit()
        end

        push!(q, (next, dist + 1))

    end

end


