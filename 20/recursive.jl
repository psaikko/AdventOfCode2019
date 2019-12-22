import PyPlot

function main()
    lines = readlines(open("input"))
    grid = collect.(lines)

    println.(join.(grid))

    Point = Tuple{Int,Int}

    portals = Dict{String,Array{Point}}()

    W = length(grid[1])
    H = length(grid)

    outside(x,y) = (x == 3 || x == (W - 2)) || (y == 3 || y == (H - 2))

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

            if outside(a...) == outside(b...)
                println( a, " ",b)
                exit()
            end
        end
    end

    # BFS from start 
    q = [(start, 0, 0)]

    visited = Set{Tuple{Point,Int}}()

    trace = Dict()

    while length(q) > 0
        loc, dist, level = popfirst!(q)
        #println(dist," ",level)
        push!(visited, (loc, level))

        next_locs = [((x,y),level) for (x,y) in neighbours(loc...) if grid[y][x] == '.']

        if haskey(jumps, loc)
            if outside(loc...) && level > 0
                push!(next_locs, (jumps[loc], level-1))
                #println("outside, ",loc)
            elseif !outside(loc...)
                push!(next_locs, (jumps[loc], level+1))
                #println("inside, ",loc)
            end
        end

        for (next_pos, next_level)  in next_locs
            if (next_pos, next_level) in visited
                continue
            end

            trace[(next_pos, next_level)] = (loc, level)
            if next_pos == goal && next_level == 0
                println("Shortest path ",dist + 1)
                empty!(q)
            end

            push!(q, (next_pos, dist + 1, next_level))
        end
    end

    c = (goal, 0)
    path = [c]
    while haskey(trace, c)
        c = trace[c]
        pushfirst!(path, c)
    end

    bitmap = [[c == '.' ? 0 : 1 for c in line] for line in grid]
    for (p, l) in path 
        PyPlot.cla()
        x, y = p
        bitmap[y][x] = 2
        PyPlot.title(l)
        PyPlot.imshow(bitmap)
        
        for jump in jumps
            p1 = jump[1]
            p2 = jump[2]
            PyPlot.plot([p1[1]-1, p2[1]-1],[p1[2]-1, p2[2]-1])
        end

        PyPlot.pause(0.01)
        bitmap[y][x] = 0
    end
end

main()