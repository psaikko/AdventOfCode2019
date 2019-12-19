import Base.==
import Base.hash

struct State
    c::Char
    keys::Set{Char}
end

Base.isequal(a::State, b::State) = a.c == b.c && a.keys == b.keys
Base.hash(a::State) = hash(a.c * join(sort(collect(a.keys))))

function main() 
    lines = readlines(open("input"))
    grid = collect.(strip.(lines))
    println.(join.(grid))

    w = length(lines[1])
    h = length(lines)

    entrance_x = 0
    entrance_y = 0

    locations = Dict{Char,Tuple{Int,Int}}()

    # find entrance
    for y in 1:h
        for x in 1:w
            c = grid[y][x]
            if !occursin(r"[.#]", string(c))
                locations[c] = (x,y)
            end
        end
    end

    start = State('@', Set())

    moves(x,y) = [(x+1,y),(x-1,y),(x,y-1),(x,y+1)]

    mem_kr = Dict{Tuple{Char,Char}, Tuple{Set{Char}, Int}}()
    function keys_required(a::Char, b::Char)
        if haskey(mem_kr, (a,b)) 
            return mem_kr[(a,b)]
        end

        visited = Set()
        x, y = locations[a]
        q = [(x,y,0)]
        pred = Dict{Tuple{Int,Int}, Tuple{Int,Int}}()

        # BFS shortest a->b path
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
                
                pred[next] = (curr_x,curr_y)
                if tile == b
                    empty!(q)
                    break
                end
                # Move forward
                push!(q, (nx,ny,dist+1))
            end
        end

        reqs = Set{Char}()
        dist = 1
        
        # Backtrack to find doors on the shortest path
        # Unwritten assumption: maze is treelike, so only one sensible a->b path exists
        cx, cy = pred[locations[b]]
        while grid[cy][cx] != a 
            dist += 1
            c = grid[cy][cx]
            if occursin(r"[a-zA-Z]", string(c))
                push!(reqs, lowercase(c))
            end
            cx, cy = pred[(cx,cy)]
        end

        mem_kr[(a,b)] = (reqs, dist)
        println(a," ",b," ",reqs," ",dist)
        return (reqs, dist)
    end

    allkeys = Set([k for k in keys(locations) if occursin(r"[a-z]", string(k))])
    println("Keys: ",allkeys)

    UB = typemax(Int64)

    mem = Dict{State, Tuple{Int,String}}()
    function solve(s::State, LB::Int) 

        best_dist = typemax(Int32)
        best_order = ""

        if haskey(mem, s)
            return mem[s]
        end

        remaining_keys = setdiff(allkeys, s.keys)

        #targets = reachable(s)

        targets = [(nextkey, keys_required(s.c, nextkey)) for nextkey in remaining_keys]
        targets = [(k, dist) for (k, (reqs, dist)) in targets if length(setdiff(reqs, s.keys)) == 0]

        if length(targets) == 0
            println(LB)
            UB = min(LB, UB)       
            return (0, "")
        end

        for (key, dist_to_key) in targets
            keyset = Set(s.keys)
            push!(keyset, key)
            if dist_to_key+LB < UB
                dist_rest, order = solve(State(key,keyset), dist_to_key + LB)
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