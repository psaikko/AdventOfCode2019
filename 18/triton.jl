import Base.==

struct State
    x::Int
    y::Int
    keys::Set{Char}
end

Base.:(==)(a::State, b::State) = a.x == b.x && a.y == b.y && a.keys == b.keys

function main() 
    lines = readlines(open("test2"))
    grid = collect.(strip.(lines))
    println.(join.(grid))

    w = length(lines[1])
    h = length(lines)

    entrance_x = 0
    entrance_y = 0

    # find entrance
    for y in 1:h
        for x in 1:w
            if grid[y][x] == '@'
                entrance_x = x
                entrance_y = y
            end
        end
    end

    start = State(entrance_x, entrance_y, Set())

    moves(x,y) = [(x+1,y),(x-1,y),(x,y-1),(x,y+1)]

    function reachable(s::State)
        visited = Set()
        q = [(s.x,s.y,0)]
        targets = []

        while length(q) > 0 
            curr_x, curr_y, dist = popfirst!(q)
            push!(visited, (curr_x,curr_y))

            for next in moves(curr_x,curr_y)
                nx, ny = next
                # Already been here?
                if (next in visited) continue end
                tile = grid[ny][nx]
                # Hit a wall?
                if (tile == '#') continue end
                # Door we cant open?
                if (occursin(r"[A-Z]", string(tile)) && !(lowercase(tile) in s.keys)) continue end
                # New key?
                if (occursin(r"[a-z]", string(tile)) && !(tile in s.keys)) 
                    push!(targets, (tile, nx, ny, dist+1))
                    push!(visited, (nx,ny))
                    continue
                end
                # Move forward
                push!(q, (nx,ny,dist+1))
            end
        end
        return targets
    end

    println.(reachable(start))

    mem = Dict{State, Tuple{Int,String}}()
    calls = 0
    UB = typemax(Int64)

    function solve(s::State, traveled::Int) 
        calls += 1
        best_dist = typemax(Int32)
        best_order = ""

        if haskey(mem, s)
            return mem[s]
        end

        targets = reachable(s)
        if length(targets) == 0
            println(traveled)
            UB = min(traveled, UB)
            
            return (0, "")
        end

        for (key, x, y, dist_to_key) in targets
            
            keyset = Set(s.keys)
            push!(keyset, key)
            if dist_to_key+traveled < UB
                dist_rest, order = solve(State(x,y,keyset), dist_to_key + traveled)
                if dist_rest + dist_to_key < best_dist
                    best_dist = dist_rest + dist_to_key
                    best_order = key * order
                end
            end
        end

        mem[s] = (best_dist, best_order)
        return (best_dist, best_order)
    end

    sol = solve(start, 0)
    println(sol)
end

main()