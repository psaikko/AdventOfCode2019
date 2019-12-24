function main() 
    grid = collect.(readlines(open("input")))

    println(join(grid))
    println(grid)

    flatten(A) = join(join.(A))
    get_id(A) = sum([2^i for i in 0:24 if flatten(A)[i+1] == '#'])

    function adjacents(grid, x, y)
        adj = []
        if x > 1
            push!(adj, grid[y][x-1])
        end
        if y > 1
            push!(adj, grid[y-1][x])
        end
        if x < 5
            push!(adj, grid[y][x+1])
        end
        if y < 5
            push!(adj, grid[y+1][x])
        end
        return adj
    end

    function next_state(grid)
        next_grid = deepcopy(grid)

        for y in 1:5
            for x in 1:5
                adj = adjacents(grid, x, y)
                bugs = count(c->c=='#', adj)
                if grid[y][x] == '#'
                    if bugs != 1
                        next_grid[y][x] = '.'
                    else
                        next_grid[y][x] = '#'
                    end
                else #  '.'
                    if bugs < 1 || bugs > 2
                        next_grid[y][x] = '.'
                    else
                        next_grid[y][x] = '#'
                    end
                end
            end
        end
        return next_grid
    end

    seen = Set()
    push!(seen, get_id(grid))

    println.(join.(grid))
    for i in 1:1000
        grid = next_state(grid)
        println()
        println.(join.(grid))
        score = get_id(grid)
        println(score)
        if score in seen
            break
        end
        push!(seen, score)
    end
end

main()